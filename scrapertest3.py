import requests
import csv
import re
import time
from datetime import datetime

def scrape_and_process_war(war_number):
    """
    Scrapes data for a single war, applies the correct conditional headers,
    and saves the result to a CSV file.
    """
    param = f"WC{war_number}"
    page_url = f"https://foxholestats.com/index.php?map=Conquest_Total&days={param}"
    csv_filename = f"war_data_{param}.csv"

    print(f"--- Processing War {war_number} ---")
    print(f"Fetching data from: {page_url}")

    # Define the 3 different header structures as provided
    headers_pop_16_19 = [
        "Timestamp", "WardenPlayers", "ColonialPlayers", "WardenCaptures", "ColonialCaptures", "WardenCasualties",
        "ColonialCasualties", "WardenCasualtyRate", "WardenCasualtyRateHr", "ColonialCasualityRate",
        "ColonialCasualityRateHr", "SteamPlayers", "WardenPlayHours", "ColonialPlayHours", "Column_14",
        "Column_15", "WardenPlayersMore", "ColonialPlayersMore", "Column_18", "Column_19"
    ]
    headers_pop_ext_63_111 = [
        "Timestamp", "WardenPlayers", "ColonialPlayers", "WardenCaptures", "ColonialCaptures", "WardenCasualties",
        "ColonialCasualties", "WardenCasualtyRate", "WardenCasualtyRateHr", "ColonialCasualtyRate",
        "ColonialCasualtyRateHr", "SteamPlayers", "WardenPlayHours", "ColonialPlayHours", "WardenQueued",
        "ColonialQueued", "WardenPlayersMore", "ColonialPlayersMore", "WardenQueueWarning", "ColonialQueueWarning", "Column_20"
    ]
    headers_basic = [
        "Timestamp", "Column_1", "Column_2", "WardenCaptures", "ColonialCaptures", "WardenCasualties",
        "ColonialCasualties", "WardenCasualtyRate", "WardenCasualtyRateHr", "ColonialCasualityRate",
        "ColonialCasualityRateHr", "SteamPlayers", "Column_12", "Column_13", "Column_14", "Column_15",
        "Column_16", "Column_17", "Column_18", "Column_19", "Column_20"
    ]

    # Determine which header structure to use based on the war number
    if 16 <= war_number <= 19:
        active_headers = headers_pop_16_19
        print("Applying structure: Population Data (16-19)")
    elif 63 <= war_number <= 111:
        # Correcting user-provided headers for consistency
        headers_pop_ext_63_111 = [h.replace(' ', '').replace('/hr', 'Hr') for h in headers_pop_ext_63_111]
        active_headers = headers_pop_ext_63_111
        print("Applying structure: Population Data Extended (63-111)")
    else:  # This covers wars 20-62 and 112-126
        active_headers = headers_basic
        print("Applying structure: Basic Data")

    try:
        response = requests.get(page_url)
        response.raise_for_status()
        html_content = response.text

        pattern = re.compile(r"data1\.addRow\(\[(.*?)\]\);")
        matches = pattern.findall(html_content)

        if not matches:
            print(f"❌ No data found for War {war_number}. Skipping.")
            return

        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write the selected header row
            writer.writerow(active_headers)

            # Process and write each data row
            for row_string in matches:
                try:
                    parts = row_string.split(',')
                    timestamp_ms = int(re.search(r'\d+', parts[0]).group())
                    timestamp = datetime.fromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Extract all data columns and clean them up
                    data_columns = [p.strip().replace("'", "") for p in parts[1:]]
                    
                    # Combine timestamp with data columns and write to file
                    full_row = [timestamp] + data_columns
                    writer.writerow(full_row)
                except (IndexError, AttributeError, ValueError):
                    continue
        
        print(f"✅ Success! Data for War {war_number} saved to {csv_filename}\n")

    except requests.exceptions.RequestException as e:
        print(f"❌ A network error occurred for War {war_number}: {e}\n")

# --- Main loop to iterate through all specified wars ---
if __name__ == "__main__":
    # Scrape all wars from 16 to 126 inclusive
    for i in range(16, 127):
        scrape_and_process_war(i)
        # Add a short delay to be respectful to the server
        time.sleep(1)
    
    print("--- All wars processed. ---")