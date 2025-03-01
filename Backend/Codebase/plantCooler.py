import os
import pandas as pd
import random

def add_special_info():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Data'))
    edible_csv = os.path.join(base_dir, "dataset_edible_plants.csv")
    output_csv = os.path.join(base_dir, "plants_better.csv")
    
    df = pd.read_csv(edible_csv)
    
    # Initialize new columns for special attributes
    df['Spicy'] = False
    df['Keto'] = False
    df['GlutenFree'] = False
    df['ProteinInfo'] = ""  # Will store special protein info if assigned

    # For 20% of the plants, randomly assign one special attribute
    special_attributes = ['Spicy', 'Keto', 'GlutenFree', 'Protein']
    # Iterate over each plant record
    for index in df.index:
        if random.random() < 0.2:
            attr = random.choice(special_attributes)
            if attr == 'Protein':
                # You can customize the criteria as needed; here we flag it as "High Protein"
                df.at[index, 'ProteinInfo'] = "High Protein"
            else:
                df.at[index, attr] = True
    
    df.to_csv(output_csv, index=False)
    print(f"plants_better.csv generated at {output_csv}")

if __name__ == "__main__":
    add_special_info()