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
        raw_id = item.get("id", "")
        
        # SKIP if the ID contains '_st'
        if "_st" in raw_id:
            continue
            
        try:
            # Extract number: "music_kit-3" -> "3"
            clean_id = raw_id.split("-")[1]
            final_id = int(clean_id)
        except (IndexError, ValueError):
            continue

        clean_item = {
            "id": final_id,
            "name": item.get("name"),
            "image": item.get("image")
        }
        music_output.append(clean_item)
    
    # Sort by ID so the list is organized
    music_output.sort(key=lambda x: x["id"])

    with open("music_en.json", "w", encoding="utf-8") as f:
        json.dump(music_output, f, indent=4, ensure_ascii=False)
    
    print(f"Successfully processed {len(music_output)} unique music kits.")

if __name__ == "__main__":
    fetch_music()