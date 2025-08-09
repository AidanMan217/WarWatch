import pandas as pd
import glob
import os

def remove_queue_columns():
    """
    A standalone script to remove the final set of specified columns
    from the already-cleaned dataset.
    """
    # Define the input and output folders for this final step
    input_folder = 'final_cleaned_data'
    output_folder = 'model_ready_data'

    # Get the path to the directory where the script is running
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    input_path = os.path.join(script_dir, input_folder)
    output_path_folder = os.path.join(script_dir, output_folder)
    
    # Create the final output folder if it doesn't exist
    os.makedirs(output_path_folder, exist_ok=True)
    
    if not os.path.isdir(input_path):
        print(f"❌ Error: Input folder '{input_folder}' not found.")
        print("Please run the previous cleaning script first to generate the required folder.")
        return

    # Find all CSV files within the input folder
    search_pattern = os.path.join(input_path, "*.csv")
    csv_files = glob.glob(search_pattern)

    if not csv_files:
        print(f"❌ No CSV files found inside the '{input_folder}' folder.")
        return

    print(f"Found {len(csv_files)} files to process in '{input_folder}'...\n")

    # List of the six columns to be removed
    columns_to_drop = [
        'WardenQueued', 'ColonialQueued', 'WardenPlayersMore', 
        'ColonialPlayersMore', 'WardenQueueWarning', 'ColonialQueueWarning'
    ]

    for filename in csv_files:
        base_filename = os.path.basename(filename)
        print(f"Processing: {base_filename}")
        
        try:
            # Read the CSV file
            df = pd.read_csv(filename)
            
            # Drop the specified columns. 'errors='ignore'' is essential here.
            df.drop(columns=columns_to_drop, inplace=True, errors='ignore')
            
            # Define the full path for the new output file
            output_file_path = os.path.join(output_path_folder, base_filename)
            
            # Save the modified DataFrame to the final location
            df.to_csv(output_file_path, index=False)
            
            print(f"  - ✅ Removed columns and saved to '{output_folder}'.")

        except Exception as e:
            print(f"  - ❌ An error occurred while processing {base_filename}: {e}")
    
    print(f"\n--- Final processing complete. Your model-ready data is in the '{output_folder}' folder. ---")

# --- Run the script ---
if __name__ == "__main__":
    remove_queue_columns()