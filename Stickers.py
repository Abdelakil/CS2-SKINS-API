import requests
import json

def compress_url(original_url):
    """Wraps the URL with Weserv for WebP compression and transparency."""
    if not original_url:
        return ""
    # Remove https:// to keep the Weserv URL clean
    clean_url = original_url.replace("https://", "")
    return f"https://images.weserv.nl/?url={clean_url}&output=webp&q=80"

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

        # Get the original image and wrap it with Weserv
        original_image = item.get("image")
        compressed_image = compress_url(original_image)

        clean_item = {
            "id": sticker_id,
            "name": item.get("name"),
            "image": compressed_image
        }
        stickers_output.append(clean_item)
    
    # Sort numerically for a clean file
    stickers_output.sort(key=lambda x: int(x["id"]) if x["id"].isdigit() else 0)

    with open("stickers_en.json", "w", encoding="utf-8") as f:
        json.dump(stickers_output, f, indent=4, ensure_ascii=False)
    
    print(f"Successfully processed {len(stickers_output)} stickers with compressed images.")

if __name__ == "__main__":
    fetch_stickers()