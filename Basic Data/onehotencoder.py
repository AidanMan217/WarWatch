import pandas as pd
import glob
import os

def add_target_variable():
    """
    A standalone script that adds a binary target variable to each CSV file
    based on the capture count in the final row.
    """
    # Define the input and final output folders
    input_folder = 'final_cleaned_data'
    output_folder = 'final_data_with_target'

    # Get the path to the directory where the script is running
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    input_path = os.path.join(script_dir, input_folder)
    output_path_folder = os.path.join(script_dir, output_folder)
    
    # Create the final output folder if it doesn't exist
    os.makedirs(output_path_folder, exist_ok=True)
    
    if not os.path.isdir(input_path):
        print(f"❌ Error: Input folder '{input_folder}' not found.")
        print("Please run the previous cleaning scripts first to generate the required folder.")
        return

    # Find all CSV files within the input folder
    search_pattern = os.path.join(input_path, "*.csv")
    csv_files = glob.glob(search_pattern)

    if not csv_files:
        print(f"❌ No CSV files found inside the '{input_folder}' folder.")
        return

    print(f"Found {len(csv_files)} files to process for target variable creation...\n")

    for filename in csv_files:
        base_filename = os.path.basename(filename)
        print(f"Processing: {base_filename}")
        
        try:
            df = pd.read_csv(filename)
            
            # Check if file is empty or missing required columns
            if df.empty or 'WardenCaptures' not in df.columns or 'ColonialCaptures' not in df.columns:
                print("  - ⚠️ File is empty or missing 'Captures' columns. Skipping.")
                continue

            # --- Core Logic to Determine Winner ---
            # Get the very last row of data
            last_row = df.iloc[-1]
            
            # Get the capture counts from the last row
            warden_captures = pd.to_numeric(last_row['WardenCaptures'], errors='coerce')
            colonial_captures = pd.to_numeric(last_row['ColonialCaptures'], errors='coerce')

            # Determine the target value (1 for Warden win, 0 for Colonial win or tie)
            if warden_captures > colonial_captures:
                target_value = 1
                print("  - Warden final capture lead. Target = 1")
            else:
                target_value = 0
                print("  - Colonial final capture lead or tie. Target = 0")

            # Add the new column and fill it with the target value
            df['Target'] = target_value
            
            # Define the full path for the new output file
            output_file_path = os.path.join(output_path_folder, base_filename)
            
            # Save the modified DataFrame to the final location
            df.to_csv(output_file_path, index=False)
            
            print(f"  - ✅ Added target variable and saved to '{output_folder}'.")

        except Exception as e:
            print(f"  - ❌ An error occurred while processing {base_filename}: {e}")
    
    print(f"\n--- Final processing complete. Your final dataset with target variables is in the '{output_folder}' folder. ---")

# --- Run the script ---
if __name__ == "__main__":
    add_target_variable()