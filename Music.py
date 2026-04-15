import requests
import json

def compress_url(original_url):
    """Wraps the URL with Weserv for WebP compression and transparency."""
    if not original_url:
        return ""
    # Remove https:// to keep the Weserv URL clean
    clean_url = original_url.replace("https://", "")
    return f"https://images.weserv.nl/?url={clean_url}&output=webp&q=80"

def fetch_music():
    url = "https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/en/music_kits.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching music kits: {e}")
        return

    music_output = []

    for item in data:
        raw_id = item.get("id", "")
        
        # Skip StatTrak versions
        if "_st" in raw_id:
            continue
            
        try:
            # Extract number: "music_kit-3" -> "3"
            clean_id_str = raw_id.split("-")[1]
        except IndexError:
            continue

        clean_item = {
            "id": clean_id_str,
            "name": item.get("name"),
            "image": compress_url(item.get("image")) # Compression applied here
        }
        music_output.append(clean_item)
    
    # Sort numerically based on the ID string
    music_output.sort(key=lambda x: int(x["id"]))

    with open("music_en.json", "w", encoding="utf-8") as f:
        json.dump(music_output, f, indent=4, ensure_ascii=False)
    
    print(f"Successfully processed {len(music_output)} kits with compressed image URLs.")

if __name__ == "__main__":
    fetch_music()