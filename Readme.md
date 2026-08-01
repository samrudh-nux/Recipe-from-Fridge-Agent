# Recipe-from-Fridge Agent

A simple agentic Python project: list what's in your fridge/pantry, and it
proposes a dish, checks whether it's actually feasible with what you have,
and — if something key is missing — decides on the closest substitute
instead of just failing.

## Why this counts as "agentic" (not just a script)

The core decision point is this: after proposing a dish, the agent checks
its own proposal for feasibility. If a key ingredient is missing, it
doesn't just stop or error out — it takes a second action: asking for the
closest substitute, then re-generating the recipe using that substitution.

That's the observe → decide → act loop:
- **Observe:** what's actually in the ingredient list
- **Decide:** is the proposed dish feasible as-is, or not?
- **Act:** either write the recipe directly, or fetch a substitute first
  and *then* write the recipe

A non-agentic version of this would just generate one recipe and hope for
the best, with no self-check and no fallback path.

## Files

| File | Purpose |
|---|---|
| `pantry.py` | Parses the user's raw ingredient input into a clean list |
| `agent.py` | The agent: proposes a dish, checks feasibility, decides on substitutions |
| `main.py` | CLI entry point — run this |
| `requirements.txt` | Dependencies |
| `.env.example` | Copy to `.env` and add your API key |

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# edit .env and paste in your Anthropic API key
```

## Run

```bash
python main.py
```

Type your ingredients comma-separated when prompted, e.g.:
`2 eggs, half an onion, some rice, garlic, soy sauce`

## Ideas to extend it (good next commits)

- Add a second feasibility check on the *final* recipe (not just the
  initial proposal) — a small self-verification loop, similar in spirit
  to the safety-eval idea from the medical-agent project.
- Support dietary constraints (vegetarian, allergies) as an input the
  agent must respect when proposing dishes.
- Swap the CLI for a small FastAPI endpoint + simple frontend, deployable
  on Vercel, so it's a shareable web app.
- Let the agent propose 2-3 dish options and pick the most feasible one
  itself, instead of committing to the first idea.

## Notes

- Model name in `agent.py` (`MODEL = "claude-sonnet-4-5"`) — change it to
  whichever Claude model your API key has access to.
- The dish-proposal step asks the LLM to return JSON — `_safe_json_parse`
  in `agent.py` strips markdown code fences in case the model wraps its
  JSON output, which happens occasionally.
