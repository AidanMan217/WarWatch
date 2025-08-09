import pandas as pd
import os

def combine_extended_data():
    """
    Combines the cleaned CSVs for the "extended data" wars (63-111)
    into a single file with a specific column structure.
    """
    # Define the input folder and the final output filename
    input_folder = 'data_with_win_margin'
    output_filename = 'DataWithPopulationRegr.csv'

    # Get the path to the directory where the script is running
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, input_folder)

    # Check if the input directory exists
    if not os.path.isdir(input_path):
        print(f"❌ Error: Input folder '{input_folder}' not found.")
        print("Please run the previous scripts first to generate the required folder.")
        return

    # Define the specific columns you want in the final output
    # The 'Target' column will be renamed from 'WardenWin_by_Captures'
    final_columns = [
        "WarNumber", "Timestamp", "WardenPlayers", "ColonialPlayers", "WardenCaptures", "ColonialCaptures",
        "WardenCasualties", "ColonialCasualties", "WardenCasualtyRate", "ColonialCasualtyRate",
        "SteamPlayers", "WardenPlayHours", "ColonialPlayHours", "WinMargin"
    ]

    # Create a list to hold the DataFrame from each war file
    list_of_dataframes = []
    
    print("Starting to combine 'extended data' wars (63-111)...")

    # Loop through the specified war range in order
    for war_number in range(63, 112):
        filename = os.path.join(input_path, f"war_data_WC{war_number}.csv")
        
        if os.path.exists(filename):
            print(f"  - Reading War {war_number}...")
            df = pd.read_csv(filename)
            
            # Add a 'WarNumber' column to keep track of the source
            df['WarNumber'] = war_number
            list_of_dataframes.append(df)
        else:
            print(f"  - Warning: Could not find data for War {war_number}. Skipping.")

    if not list_of_dataframes:
        print("❌ No data files found for the specified war range (63-111).")
        return

    # Combine all DataFrames into one
    print("\nCombining all found files...")
    combined_df = pd.concat(list_of_dataframes, ignore_index=True)

    # Rename the target column as requested
    if 'WardenWin_by_Captures' in combined_df.columns:
        combined_df.rename(columns={'WardenWin_by_Captures': 'Target'}, inplace=True)
    else:
        print("  - Warning: 'WardenWin_by_Captures' column not found to rename.")

    # Ensure all required final columns exist before trying to select them
    # This prevents errors if a file was missing a column for some reason
    columns_to_select = [col for col in final_columns if col in combined_df.columns]
    
    # Select and reorder the columns for the final dataset
    final_df = combined_df[columns_to_select]

    # Save the final combined dataset to a new CSV file
    output_file_path = os.path.join(script_dir, output_filename)
    final_df.to_csv(output_file_path, index=False)
    
    print(f"\n✅ Success! Combined data saved to '{output_filename}'.")

# --- Run the script ---
if __name__ == "__main__":
    combine_extended_data()