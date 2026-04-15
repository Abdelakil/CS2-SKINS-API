import requests
import json

def fetch_skins():
    url = "https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/en/skins.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error: {e}")
        return

    skins_output = []

    for item in data:
        category_name = item.get("category", {}).get("name", "")
        
        # We only want weapons, so we exclude Gloves and Agents
        # Most weapon skins have category names like 'Rifles', 'Pistols', etc.
        if category_name not in ["Gloves", "Agents"] and "weapon" in item:
            
            clean_item = {
                "weapon_defindex": item.get("weapon", {}).get("weapon_id"),
                "weapon_name": item.get("weapon", {}).get("id"),
                "paint": item.get("paint_index"),
                "image": item.get("image"),
                "paint_name": item.get("name"),
                "legacy_model": item.get("legacy_model", False)
            }
            skins_output.append(clean_item)
    
    with open("skins_en.json", "w", encoding="utf-8") as f:
        json.dump(skins_output, f, indent=4, ensure_ascii=False)
    
    print(f"Successfully processed {len(skins_output)} weapon skins.")

if __name__ == "__main__":
    fetch_skins()