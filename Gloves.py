import requests
import json

def fetch_and_filter():
    url = "https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/en/skins.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    filtered_output = []

    for item in data:
        # Navigate the nested JSON to check the category name
        category = item.get("category", {})
        if category.get("name") == "Gloves":
            
            # Map the complex structure to your specific requirements
            clean_item = {
                "weapon_defindex": item.get("weapon", {}).get("weapon_id"),
                "paint": item.get("paint_index"),
                "image": item.get("image"),
                "paint_name": item.get("name")
            }
            filtered_output.append(clean_item)
    
    # Save the simplified list to gloves.json
    with open("gloves.json", "w", encoding="utf-8") as f:
        json.dump(filtered_output, f, indent=4)
    
    print(f"Successfully processed {len(filtered_output)} items.")

if __name__ == "__main__":
    fetch_and_filter()