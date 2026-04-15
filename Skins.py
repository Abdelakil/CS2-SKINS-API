import requests
import json

def fetch_skins():
    # Source A: Primary list (Large, but missing defaults)
    url_primary = "https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/en/skins.json"
    # Source B: Secondary list (Used to get Paint 0 / Default skins)
    url_defaults = "https://raw.githubusercontent.com/Nereziel/cs2-WeaponPaints/refs/heads/main/website/data/skins_en.json"
    
    try:
        res_a = requests.get(url_primary)
        res_b = requests.get(url_defaults)
        res_a.raise_for_status()
        res_b.raise_for_status()
        
        data_a = res_a.json()
        data_b = res_b.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    # Use a dictionary to store unique skins. 
    # Key format: "defindex-paint" (e.g., "7-0" or "7-1207")
    merged_skins = {}

    # 1. Process Primary Source (ByMykel)
    for item in data_a:
        category_name = item.get("category", {}).get("name", "")
        # Exclude non-weapons
        if category_name not in ["Gloves", "Agents"] and "weapon" in item:
            defindex = item.get("weapon", {}).get("weapon_id")
            paint = item.get("paint_index")
            
            if defindex is not None and paint is not None:
                key = f"{defindex}-{paint}"
                merged_skins[key] = {
                    "weapon_defindex": defindex,
                    "weapon_name": item.get("weapon", {}).get("id"),
                    "paint": str(paint),
                    "image": item.get("image"),
                    "paint_name": item.get("name"),
                    "legacy_model": item.get("legacy_model", False)
                }

    # 2. Process Secondary Source (Nereziel) to fill in gaps (especially Paint 0)
    for item in data_b:
        defindex = item.get("weapon_defindex")
        paint = item.get("paint")
        
        if defindex is not None and paint is not None:
            key = f"{defindex}-{paint}"
            
            # Only add if it's NOT already in our dictionary (like Paint 0)
            if key not in merged_skins:
                merged_skins[key] = {
                    "weapon_defindex": defindex,
                    "weapon_name": item.get("weapon_name"),
                    "paint": str(paint),
                    "image": item.get("image"),
                    "paint_name": item.get("paint_name"),
                    "legacy_model": item.get("legacy_model", False)
                }

    # 3. Convert dictionary back to a sorted list
    final_list = list(merged_skins.values())
    
    # Sort by Defindex first, then Paint ID
    final_list.sort(key=lambda x: (int(x["weapon_defindex"]), int(x["paint"])))

    with open("skins_en.json", "w", encoding="utf-8") as f:
        json.dump(final_list, f, indent=4, ensure_ascii=False)
    
    print(f"Combined total: {len(final_list)} skins successfully saved.")

if __name__ == "__main__":
    fetch_skins()