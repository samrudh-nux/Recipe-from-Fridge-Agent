 def parse_ingredients(raw_input: str) -> list[str]:
    """
    Splits a comma or newline separated string into a clean list.
    "2 eggs, some rice, half an onion" -> ["2 eggs", "some rice", "half an onion"]
    """
    # allow either commas or newlines as separators
    if "\n" in raw_input:
        parts = raw_input.split("\n")
    else:
        parts = raw_input.split(",")
 
    cleaned = [p.strip() for p in parts if p.strip()]
    return cleaned
 
 
def format_ingredient_list(ingredients: list[str]) -> str:
    """Turns the list back into a readable bullet list for prompts/printing."""
    return "\n".join(f"- {item}" for item in ingredients)
 
 
if __name__ == "__main__":
    # quick manual test
    test = input("Type some ingredients (comma-separated) to test parsing: ")
    result = parse_ingredients(test)
    print(f"\nParsed {len(result)} ingredients:")
    print(format_ingredient_list(result))
 
