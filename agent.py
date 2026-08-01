 
import os
import json
from anthropic import Anthropic
from pantry import format_ingredient_list
 
MODEL = "claude-sonnet-4-5"   # swap for whichever Claude model you have access to
 
 
def _client() -> Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Set your ANTHROPIC_API_KEY environment variable before running this."
        )
    return Anthropic(api_key=api_key)
 
 
def _call_llm(client: Anthropic, prompt: str) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
 
 
def _propose_dish(client: Anthropic, ingredients_text: str) -> dict:
    """
    Ask the LLM to propose ONE dish and self-report whether it's fully
    feasible with what's available. Returns parsed JSON so the agent can
    make a real decision on the next step, rather than just printing text.
    """
    prompt = f"""You are a practical home cook. Here is what's available:
{ingredients_text}
 
Propose ONE simple dish that could be made mostly from this. Respond with
ONLY valid JSON in this exact shape, no other text:
 
{{
  "dish_name": "...",
  "feasible": true or false,
  "missing_key_ingredient": "name of the one missing item, or null if feasible is true",
  "reasoning": "one short sentence explaining the feasibility call"
}}"""
    raw = _call_llm(client, prompt)
    return _safe_json_parse(raw)
 
 
def _suggest_substitute(client: Anthropic, missing_ingredient: str, ingredients_text: str) -> str:
    """Asks the LLM to pick the closest substitute from common pantry items."""
    prompt = f"""A recipe needs "{missing_ingredient}" but it's not available.
Available ingredients are:
{ingredients_text}
 
Suggest the single closest substitute for "{missing_ingredient}" — either
something commonly on hand that isn't listed above, or a way to work
around it using only what's listed. One or two sentences, be specific."""
    return _call_llm(client, prompt)
 
 
def _write_full_recipe(client: Anthropic, dish_name: str, ingredients_text: str, substitution_note: str | None) -> str:
    """Generates the final step-by-step recipe."""
    sub_line = f"\nNote: use this substitution where needed: {substitution_note}" if substitution_note else ""
    prompt = f"""Write a simple, numbered step-by-step recipe for "{dish_name}"
using mainly these ingredients:
{ingredients_text}{sub_line}
 
Keep it to 5-8 steps. Include rough quantities and cook times where relevant."""
    return _call_llm(client, prompt)
 
 
def _safe_json_parse(raw: str) -> dict:
    """LLMs sometimes wrap JSON in markdown fences — strip those before parsing."""
    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())
 
 
def plan_meal(ingredients: list[str]) -> dict:
    """
    The main agentic entry point.
    Returns: {
        "dish_name": str,
        "was_substitution_needed": bool,
        "substitution_note": str | None,
        "recipe": str,
    }
    """
    client = _client()
    ingredients_text = format_ingredient_list(ingredients)
 
    proposal = _propose_dish(client, ingredients_text)
 
    # --- DECISION POINT: this is the "agentic" branch ---
    if proposal["feasible"]:
        substitution_note = None
    else:
        missing = proposal["missing_key_ingredient"]
        substitution_note = _suggest_substitute(client, missing, ingredients_text)
 
    recipe = _write_full_recipe(
        client,
        proposal["dish_name"],
        ingredients_text,
        substitution_note,
    )
 
    return {
        "dish_name": proposal["dish_name"],
        "was_substitution_needed": not proposal["feasible"],
        "missing_ingredient": proposal.get("missing_key_ingredient"),
        "substitution_note": substitution_note,
        "recipe": recipe,
    }
