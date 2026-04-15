import requests
import json

def fetch_stickers():
    url = "https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/en/stickers.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching stickers: {e}")
        return

    stickers_output = []

    for item in data:
        # Get the numeric ID as a string from def_index
        sticker_id = str(item.get("def_index", ""))
        
        # We only process if there is a valid ID
        if not sticker_id:
            continue

        # Construct the custom image URL as per your requirement
        image_url = f"https://raw.githubusercontent.com/Nereziel/cs2-WeaponPaints/main/website/img/skins/sticker-{sticker_id}.png"

        clean_item = {
            "id": sticker_id,
            "name": item.get("name"),
            "image": image_url
        }
        stickers_output.append(clean_item)
    
    # Sort numerically for a clean file
    stickers_output.sort(key=lambda x: int(x["id"]) if x["id"].isdigit() else 0)

    with open("stickers_en.json", "w", encoding="utf-8") as f:
        json.dump(stickers_output, f, indent=4, ensure_ascii=False)
    
    print(f"Successfully processed {len(stickers_output)} stickers.")

if __name__ == "__main__":
    fetch_stickers()