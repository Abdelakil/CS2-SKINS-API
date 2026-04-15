import requests
import json

def compress_url(original_url):
    """Wraps the URL with Weserv for WebP compression and transparency."""
    if not original_url:
        return ""
    # Remove https:// to keep the Weserv URL clean
    clean_url = original_url.replace("https://", "")
    return f"https://images.weserv.nl/?url={clean_url}&output=webp&q=80"

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

    merged_skins = {}

    # 1. Process Primary Source (ByMykel)
    for item in data_a:
        category_name = item.get("category", {}).get("name", "")
        if category_name not in ["Gloves", "Agents"] and "weapon" in item:
            defindex = item.get("weapon", {}).get("weapon_id")
            paint = item.get("paint_index")
            
            if defindex is not None and paint is not None:
                key = f"{defindex}-{paint}"
                merged_skins[key] = {
                    "weapon_defindex": defindex,
                    "weapon_name": item.get("weapon", {}).get("id"),
                    "paint": str(paint),
                    "image": compress_url(item.get("image")), # Applied here
                    "paint_name": item.get("name"),
                    "legacy_model": item.get("legacy_model", False)
                }

    # 2. Process Secondary Source (Nereziel)
    for item in data_b:
        defindex = item.get("weapon_defindex")
        paint = item.get("paint")
        
        if defindex is not None and paint is not None:
            key = f"{defindex}-{paint}"
            
            if key not in merged_skins:
                merged_skins[key] = {
                    "weapon_defindex": defindex,
                    "weapon_name": item.get("weapon_name"),
                    "paint": str(paint),
                    "image": compress_url(item.get("image")), # Applied here
                    "paint_name": item.get("paint_name"),
                    "legacy_model": item.get("legacy_model", False)
                }

    # 3. Convert dictionary back to a sorted list
    final_list = list(merged_skins.values())
    
    # Sort by Defindex first, then Paint ID
    final_list.sort(key=lambda x: (int(x["weapon_defindex"]), int(x["paint"])))

    with open("skins_en.json", "w", encoding="utf-8") as f:
        json.dump(final_list, f, indent=4, ensure_ascii=False)
    
    print(f"Combined total: {len(final_list)} skins successfully compressed and saved.")

if __name__ == "__main__":
    fetch_skins()