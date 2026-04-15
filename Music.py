import requests
import json

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
        # Extracting exactly what you requested
        clean_item = {
            "id": str(item.get("id")), # Ensure ID is a string as per your example
            "name": item.get("name"),
            "image": item.get("image")
        }
        music_output.append(clean_item)
    
    with open("music_en.json", "w", encoding="utf-8") as f:
        json.dump(music_output, f, indent=4, ensure_ascii=False)
    
    print(f"Successfully processed {len(music_output)} music kits.")

if __name__ == "__main__":
    fetch_music()