import pandas as pd
import os

def add_win_margin_for_extended_data():
    """
    Adds a 'WinMargin' target variable specifically to the CSV files for
    the "extended data" wars (63-111).
    """
    input_folder = 'model_ready_data'
    output_folder = 'data_with_win_margin'

    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, input_folder)
    output_path_folder = os.path.join(script_dir, output_folder)
    
    os.makedirs(output_path_folder, exist_ok=True)
    
    if not os.path.isdir(input_path):
        print(f"❌ Error: Input folder '{input_folder}' not found.")
        print("Please ensure the previous data cleaning scripts have been run successfully.")
        return

    print("Searching for 'extended data' war files (63-111) to process...\n")

    # Loop specifically through the extended data war range
    for war_number in range(63, 112):
        base_filename = f"war_data_WC{war_number}.csv"
        filename = os.path.join(input_path, base_filename)
        
        # Check if the specific war file exists before processing
        if os.path.exists(filename):
            print(f"Processing: {base_filename}")
            try:
                df = pd.read_csv(filename)
                
                if df.empty or 'WardenCaptures' not in df.columns or 'ColonialCaptures' not in df.columns:
                    print("  - ⚠️ File is empty or missing 'Captures' columns. Skipping.")
                    continue

                last_row = df.iloc[-1]
                warden_captures = pd.to_numeric(last_row['WardenCaptures'], errors='coerce')
                colonial_captures = pd.to_numeric(last_row['ColonialCaptures'], errors='coerce')

                # Calculate the win margin
                win_margin = warden_captures - colonial_captures
                print(f"  - Final capture difference is {win_margin}. Creating 'WinMargin' column.")

                # Add the new column and fill it with the calculated value
                df['WinMargin'] = win_margin
                
                output_file_path = os.path.join(output_path_folder, base_filename)
                df.to_csv(output_file_path, index=False)
                
                print(f"  - ✅ Saved file with WinMargin to '{output_folder}'.")

            except Exception as e:
                print(f"  - ❌ An error occurred while processing {base_filename}: {e}")
        # This else block is optional but provides feedback if a file in the range is missing
        # else:
        #     print(f"Info: File for War {war_number} not found. Skipping.")
    
    print(f"\n--- Win margin processing complete for extended data wars. ---")

if __name__ == "__main__":
    add_win_margin_for_extended_data()