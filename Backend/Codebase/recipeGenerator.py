import os
import pandas as pd
import random
import re

def extract_plant_info(detail):
    """
    Given a plant detail string like:
    "Orange (Spicy: True, Keto: False, GlutenFree: False)" or with ProteinInfo,
    return a tuple (name, attributes) where attributes is a list of special attributes.
    """
    match = re.match(r"([^()]+)\s*\(", detail)
    name = match.group(1).strip() if match else detail.strip()
    attributes = []
    if "Spicy: True" in detail:
        attributes.append("Spicy")
    if "Keto: True" in detail:
        attributes.append("Keto")
    if "GlutenFree: True" in detail:
        attributes.append("GlutenFree")
    if "ProteinInfo: High Protein" in detail:
        attributes.append("High Protein")
    return name, attributes

def add_recipe(recipes, location, recipe_name, ingredients, seen, special_flags=None):
    # Create a canonical representation (order-independent) for uniqueness.
    canonical = tuple(sorted(ing.strip() for ing in ingredients.split(";") if ing.strip()))
    if canonical not in seen:
        seen.add(canonical)
        # Set default flags if none provided.
        if special_flags is None:
            special_flags = {"Spicy": False, "Keto": False, "High Protein": False, "GlutenFree": False}
        recipes.append({
            "Location": location,
            "Recipe": recipe_name,
            "Ingredients": ingredients,
            "Spicy": special_flags.get("Spicy", False),
            "Keto": special_flags.get("Keto", False),
            "High Protein": special_flags.get("High Protein", False),
            "GlutenFree": special_flags.get("GlutenFree", False)
        })

def default_special_flags(special_name):
    flags = {"Spicy": False, "Keto": False, "High Protein": False, "GlutenFree": False}
    if special_name in flags:
         flags[special_name] = True
    return flags

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Data'))
    clean_data_csv = os.path.join(base_dir, "cleanData.csv")
    output_csv = os.path.join(base_dir, "recipes.csv")
    
    clean_df = pd.read_csv(clean_data_csv)
    recipes = []
    
    for _, row in clean_df.iterrows():
        location = row['Location']
        plants_detail_str = row['Plants']
        if not isinstance(plants_detail_str, str) or not plants_detail_str.strip():
            continue
        
        # Split the cleanData plants string to get each plant detail.
        plant_details = [p.strip() for p in plants_detail_str.split(';') if p.strip()]
        
        # Parse details: create a list of ingredient strings with special attribute info.
        all_plants = []
        for detail in plant_details:
            name, attrs = extract_plant_info(detail)
            representation = name
            if attrs:
                representation += " (" + ", ".join(attrs) + ")"
            all_plants.append(representation)
        
        # Only generate recipes if we have at least 4 ingredients.
        if len(all_plants) < 4:
            continue
        
        # Maintain a set to keep track of unique ingredient combinations per location.
        seen_recipes = set()

        # Recipe 1: Generic Hearty Stew using all plants (all special flags false).
        generic_recipe_1 = f"{location} Hearty Stew"
        generic_ingredients_1 = "; ".join(all_plants)
        add_recipe(recipes, location, generic_recipe_1, generic_ingredients_1, seen_recipes)

        # Recipe 2: Generic Fusion Medley using the first 4 plants.
        generic_recipe_2 = f"{location} Fusion Medley"
        generic_ingredients_2 = "; ".join(all_plants[:4])
        add_recipe(recipes, location, generic_recipe_2, generic_ingredients_2, seen_recipes)

        # Now create the 4 special recipes: one each for Spicy, High Protein, Keto, and GlutenFree.
        special_types = ["Spicy", "High Protein", "Keto", "GlutenFree"]

        for attr in special_types:
            # Filter the ingredients that include the given attribute.
            candidate = [plant for plant in all_plants if attr in plant]
            if len(candidate) >= 4:
                # Try to sample a unique combination (up to 5 attempts).
                unique_found = False
                for _ in range(5):
                    chosen = random.sample(candidate, 4)
                    candidate_ingredients = "; ".join(chosen)
                    canonical = tuple(sorted(chosen))
                    if canonical not in seen_recipes:
                        special_recipe_name = f"{location} Special {attr}"
                        add_recipe(recipes, location, special_recipe_name, candidate_ingredients, seen_recipes, default_special_flags(attr))
                        unique_found = True
                        break
                if not unique_found:
                    # Fallback to generic if unable to get a unique combination.
                    fallback_recipe_name = f"{location} Generic {attr} Quartet"
                    fallback_ingredients = "; ".join(all_plants[:4])
                    add_recipe(recipes, location, fallback_recipe_name, fallback_ingredients, seen_recipes)
            else:
                # Fall back to a generic recipe if there aren't enough special candidates.
                fallback_recipe_name = f"{location} Generic {attr} Quartet"
                fallback_ingredients = "; ".join(all_plants[:4])
                add_recipe(recipes, location, fallback_recipe_name, fallback_ingredients, seen_recipes)
    
    recipes_df = pd.DataFrame(recipes)
    recipes_df.to_csv(output_csv, index=False)
    print(f"recipes.csv generated at {output_csv}")

if __name__ == "__main__":
    main()