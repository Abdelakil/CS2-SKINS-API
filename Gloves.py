import requests
import json
import os

def compress_url(original_url):
    """Wraps the URL with Weserv for WebP compression and transparency."""
    if not original_url:
        return ""
    # Remove https:// to keep the Weserv URL clean
    clean_url = original_url.replace("https://", "")
    return f"https://images.weserv.nl/?url={clean_url}&output=webp&q=80"

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
                "image": compress_url(item.get("image")), # Compression applied here
                "paint_name": item.get("name")
            })

    # Check if the file already exists and if data is identical
    if os.path.exists("gloves_en.json"):
        with open("gloves_en.json", "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
                if existing_data == filtered_output:
                    print("No changes detected in the source. Skipping update.")
                    return 
            except json.JSONDecodeError:
                pass # If file is corrupted, overwrite it

    # Save only if there are changes
    with open("gloves_en.json", "w", encoding="utf-8") as f:
        json.dump(filtered_output, f, indent=4, ensure_ascii=False)
    print("New data found! gloves_en.json has been updated with compressed image URLs.")

if __name__ == "__main__":
    fetch_and_filter()