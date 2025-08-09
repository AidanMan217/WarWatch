import pandas as pd
import os

def add_win_margin_for_basic_data():
    """
    Adds a 'WinMargin' target variable specifically to the CSV files for
    the "basic data" wars (20-62 and 112-125).
    """
    # Define the input and a new, specific output folder
    input_folder = 'final_cleaned_data'
    output_folder = 'data_with_win_margin_basic'

    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, input_folder)
    output_path_folder = os.path.join(script_dir, output_folder)
    
    os.makedirs(output_path_folder, exist_ok=True)
    
    if not os.path.isdir(input_path):
        print(f"❌ Error: Input folder '{input_folder}' not found.")
        print("Please ensure the previous data cleaning scripts have been run successfully.")
        return

    # Define the two separate ranges of wars to process
    war_ranges = list(range(20, 63)) + list(range(112, 126))

    print("Searching for 'basic data' war files (20-62 & 112-125) to process...\n")

    # Loop through the specified war numbers
    for war_number in war_ranges:
        base_filename = f"war_data_WC{war_number}.csv"
        filename = os.path.join(input_path, base_filename)
        
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

    print(f"\n--- Win margin processing complete for basic data wars. ---")

if __name__ == "__main__":
    add_win_margin_for_basic_data()