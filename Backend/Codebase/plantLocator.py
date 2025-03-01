import os
import pandas as pd

def main():
    # Set paths relative to the current script
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Data'))
    plants_csv = os.path.join(base_dir, "plants_better.csv")
    weather_csv = os.path.join(base_dir, "dataset_weather.csv")
    output_csv = os.path.join(base_dir, "cleanData.csv")
    
    # Load datasets
    plants_df = pd.read_csv(plants_csv)
    weather_df = pd.read_csv(weather_csv)
    
    # Get unique locations and their recorded climate from the weather dataset
    locations = weather_df[['Location', 'Climate']].drop_duplicates()
    
    result = []
    for _, loc_row in locations.iterrows():
        location = loc_row['Location']
        climate = loc_row['Climate']
        
        # Get plants matching the climate
        matching_plants_df = plants_df[plants_df['Growth Climate'] == climate]
        
        # For each matching plant, build a detail string that includes its special attributes
        plant_details = []
        for _, plant_row in matching_plants_df.iterrows():
            detail = (
                f"{plant_row['Name']} "
                f"(Spicy: {plant_row['Spicy']}, Keto: {plant_row['Keto']}, "
                f"GlutenFree: {plant_row['GlutenFree']}"
            )
            if pd.notnull(plant_row['ProteinInfo']) and plant_row['ProteinInfo']:
                detail += f", ProteinInfo: {plant_row['ProteinInfo']}"
            detail += ")"
            plant_details.append(detail)
        
        # Join details for all matching plants using a semicolon as separator
        plants_str = "; ".join(plant_details) if plant_details else ""
        result.append({"Location": location, "Plants": plants_str})
    
    # Save the compiled location and plant details into cleanData.csv
    result_df = pd.DataFrame(result)
    result_df.to_csv(output_csv, index=False)
    print(f"cleanData.csv generated at {output_csv}")

if __name__ == "__main__":
    main()