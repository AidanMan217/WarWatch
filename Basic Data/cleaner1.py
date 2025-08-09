import pandas as pd
import glob
import os

def clean_war_data_files():
    """
    Processes all war CSVs in a folder to find and remove "mini wars"
    by truncating the data after a major casualty reset.
    This version correctly finds files relative to its own location.
    """
    # --- The Fix: Find files in the same directory as the script ---
    # Get the absolute path to the directory where this script is located
    script_dir = os.path.dirname(__file__)
    
    # Create the search pattern based on the script's directory
    search_pattern = os.path.join(script_dir, "war_data_WC*.csv")
    
    # Create the output folder path based on the script's directory
    output_folder = os.path.join(script_dir, 'cleaned_data')
    os.makedirs(output_folder, exist_ok=True)
    
    # Use the new pattern to find all the war data CSV files
    csv_files = glob.glob(search_pattern)

    if not csv_files:
        print("❌ No 'war_data_WC...' CSV files found. Please ensure CSV files are in the same folder as the script.")
        return

    print(f"Found {len(csv_files)} war data files to process...\n")

    # --- Loop through each file ---
    for filename in csv_files:
        # os.path.basename gets just the filename (e.g., "war_data_WC20.csv")
        base_filename = os.path.basename(filename)
        print(f"Processing: {base_filename}")
        
        try:
            df = pd.read_csv(filename)

            if df.empty or 'WardenCasualties' not in df.columns:
                print("  - File is empty or missing 'WardenCasualties' column. Copying as-is.")
                df.to_csv(os.path.join(output_folder, base_filename), index=False)
                continue

            df['WardenCasualties'] = pd.to_numeric(df['WardenCasualties'], errors='coerce')
            df.dropna(subset=['WardenCasualties'], inplace=True)
            df['WardenCasualties'] = df['WardenCasualties'].astype(int)

            if df.empty:
                print("  - No valid casualty data found after cleaning. Skipping.")
                continue

            peak_index = df['WardenCasualties'].idxmax()

            if peak_index == df.index[-1]:
                print("  - Peak casualties at the end of the war. No reset detected.")
                df.to_csv(os.path.join(output_folder, base_filename), index=False)
            else:
                max_casualties = df.loc[peak_index, 'WardenCasualties']
                next_row_casualties = df.loc[peak_index + 1, 'WardenCasualties']

                if next_row_casualties < max_casualties:
                    cleaned_df = df.loc[:peak_index]
                    cleaned_df.to_csv(os.path.join(output_folder, base_filename), index=False)
                    print(f"  - Reset detected! Truncated file and saved to '{output_folder}'.")
                else:
                    print("  - No casualty reset detected after peak.")
                    df.to_csv(os.path.join(output_folder, base_filename), index=False)

        except Exception as e:
            print(f"  - An error occurred while processing {base_filename}: {e}")
    
    print("\n--- All files processed. Check the 'cleaned_data' folder for the results. ---")

# --- Run the script ---
if __name__ == "__main__":
    clean_war_data_files()