import requests
import json

def fetch_skins():
    # URL 1: Your primary source
    primary_url = "https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/en/skins.json"
    # URL 2: Your source for default skins (replace with your actual second URL)
    defaults_url = "https://raw.githubusercontent.com/LielXD/CS2-WeaponPaints-Website/refs/heads/main/src/data/skins.json"
    
    try:
        # Fetch primary
        res1 = requests.get(primary_url)
        data = res1.json()
        
        # Fetch defaults
        res2 = requests.get(defaults_url)
        defaults_data = res2.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    skins_output = []

    # 1. Process Main Skins
    for item in data:
        category_name = item.get("category", {}).get("name", "")
        if category_name not in ["Gloves", "Agents"] and "weapon" in item:
            skins_output.append({
                "weapon_defindex": item.get("weapon", {}).get("weapon_id"),
                "weapon_name": item.get("weapon", {}).get("id"),
                "paint": item.get("paint_index"),
                "image": item.get("image"),
                "paint_name": item.get("name"),
                "legacy_model": item.get("legacy_model", False)
            })

    # 2. Process and Inject Defaults (Paint 0)
    # This logic assumes your second JSON has a similar structure or weapon list
    for item in defaults_data:
        # Check if it's a paint 0 skin we don't already have
        if str(item.get("paint")) == "0" or item.get("paint_index") == "0":
            # Add mapping logic here to match your required format
            skins_output.append({
                "weapon_defindex": item.get("weapon_id") or item.get("weapon", {}).get("weapon_id"),
                "weapon_name": item.get("weapon_name") or item.get("weapon", {}).get("id"),
                "paint": "0",
                "image": item.get("image"),
                "paint_name": item.get("paint_name") or f"{item.get('name')} | Default",
                "legacy_model": item.get("legacy_model", False)
            })

    # 3. Sort and Save
    # Sort by weapon_defindex first, then paint
    skins_output.sort(key=lambda x: (int(x["weapon_defindex"]), int(x["paint"])))

    with open("skins_en.json", "w", encoding="utf-8") as f:
        json.dump(skins_output, f, indent=4, ensure_ascii=False)
    
    print(f"Successfully processed {len(skins_output)} skins (including defaults).")

if __name__ == "__main__":
    fetch_skins()