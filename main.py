 from dotenv import load_dotenv
from pantry import parse_ingredients
from agent import plan_meal
 
load_dotenv()  # loads ANTHROPIC_API_KEY from a .env file if present
 
 
def run(raw_ingredients: str) -> None:
    ingredients = parse_ingredients(raw_ingredients)
    print(f"\nParsed {len(ingredients)} ingredients.")
 
    print("Running meal-planning agent...\n")
    result = plan_meal(ingredients)
 
    print("=" * 60)
    print(f"Dish: {result['dish_name']}")
    print("=" * 60)
 
    if result["was_substitution_needed"]:
        print(f"\nMissing: {result['missing_ingredient']}")
        print(f"Substitution suggested: {result['substitution_note']}")
    else:
        print("\nFully feasible with what you have — no substitutions needed.")
 
    print("\nRECIPE:\n")
    print(result["recipe"])
    print()
 
 
if __name__ == "__main__":
    user_input = input("List what's in your fridge/pantry (comma-separated): ").strip()
    run(user_input)
 
