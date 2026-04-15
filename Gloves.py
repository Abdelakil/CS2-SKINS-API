import requests
import json
import os

def fetch_and_filter():
    url = "https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/en/skins.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        new_data = response.json()
    except Exception as e:
        print(f"Error fetching: {e}")
        return

    # Filter logic
    filtered_output = []
    for item in new_data:
        if item.get("category", {}).get("name") == "Gloves":
            filtered_output.append({
                "weapon_defindex": item.get("weapon", {}).get("weapon_id"),
                "paint": item.get("paint_index"),
                "image": item.get("image"),
                "paint_name": item.get("name")
            })

    # Check if the file already exists and if data is identical
    if os.path.exists("gloves.json"):
        with open("gloves.json", "r", encoding="utf-8") as f:
            existing_data = json.load(f)
        
        if existing_data == filtered_output:
            print("No changes detected in the source. Skipping update.")
            return # Exit script without writing file

    # Save only if there are changes
    with open("gloves.json", "w", encoding="utf-8") as f:
        json.dump(filtered_output, f, indent=4, ensure_ascii=False)
    print("New data found! gloves.json has been updated.")

if __name__ == "__main__":
    fetch_and_filter()