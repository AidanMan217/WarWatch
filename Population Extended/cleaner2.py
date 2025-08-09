import pandas as pd
import glob
import os
from datetime import datetime

def advanced_clean_war_data():
    """
    Applies a three-step advanced cleaning process to all war data CSVs.
    This version includes the bug fix for the file path issue.
    """
    # Create a new subfolder for the advanced cleaned output
    script_dir = os.path.dirname(__file__)
    output_folder = os.path.join(script_dir, 'cleaned_data_advanced')
    os.makedirs(output_folder, exist_ok=True)
    
    search_pattern = os.path.join(script_dir, "war_data_WC*.csv")
    csv_files = glob.glob(search_pattern)

    if not csv_files:
        print("❌ No 'war_data_WC...' CSV files found. Make sure this script is in the same folder as the script.")
        return

    print(f"Found {len(csv_files)} war data files to process with advanced cleaning...\n")

    for filename in csv_files:
        base_filename = os.path.basename(filename)
        print(f"Processing: {base_filename}")
        
        try:
            df = pd.read_csv(filename)

            if df.empty or 'WardenCasualties' not in df.columns or 'ColonialCasualties' not in df.columns:
                print("  - File is empty or missing required casualty columns. Skipping.")
                continue

            for col in ['WardenCasualties', 'ColonialCasualties']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            df.dropna(subset=['WardenCasualties', 'ColonialCasualties'], inplace=True)
            df = df.astype({'WardenCasualties': int, 'ColonialCasualties': int})

            last_reset_index = -1
            if len(df) > 1:
                for i in range(1, len(df)):
                    if df.iloc[i]['WardenCasualties'] < df.iloc[i-1]['WardenCasualties'] and \
                       df.iloc[i]['ColonialCasualties'] < df.iloc[i-1]['ColonialCasualties']:
                        last_reset_index = i
            
            if last_reset_index != -1:
                df = df.iloc[last_reset_index:].copy()
                print(f"  - Pre-war data reset found. Truncating {last_reset_index} early rows.")
            
            df.reset_index(drop=True, inplace=True)

            if not df.empty:
                first_action_index = (df['WardenCasualties'] > 0) | (df['ColonialCasualties'] > 0)
                if first_action_index.any():
                    first_action_index = first_action_index.idxmax()
                    rows_to_remove = df[(df.index > first_action_index) & (df['WardenCasualties'] == 0) & (df['ColonialCasualties'] == 0)]
                    if not rows_to_remove.empty:
                        print(f"  - Removing {len(rows_to_remove)} mid-war rows with zero casualties.")
                        df.drop(rows_to_remove.index, inplace=True)

            cols_before = len(df.columns)
            cols_to_keep = [col for col in df.columns if not str(col).startswith('Column_')]
            df = df[cols_to_keep]
            cols_after = len(df.columns)
            if cols_before > cols_after:
                print(f"  - Removed {cols_before - cols_after} unnamed columns.")
            
            # --- THIS IS THE CORRECTED LINE ---
            # It now correctly joins the output folder path with the filename.
            output_path = os.path.join(output_folder, base_filename)
            
            df.to_csv(output_path, index=False)
            print(f"  - ✅ Saved cleaned file to '{output_folder}'.")

        except Exception as e:
            print(f"  - ❌ An error occurred while processing {base_filename}: {e}")
    
    print("\n--- All files processed. Check the 'cleaned_data_advanced' folder for the results. ---")

# --- Run the script ---
if __name__ == "__main__":
    advanced_clean_war_data()