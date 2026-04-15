import requests
import json

def compress_url(original_url):
    """Wraps the URL with Weserv for WebP compression and transparency."""
    if not original_url:
        return ""
    # Remove https:// to keep the Weserv URL clean
    clean_url = original_url.replace("https://", "")
    return f"https://images.weserv.nl/?url={clean_url}&output=webp&q=80"

def sync_agents():
    url = "https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/en/agents.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Process each agent to compress the image URL
        for agent in data:
            if "image" in agent:
                agent["image"] = compress_url(agent.get("image"))

        # Save the modified JSON
        with open("agents_en.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        print("Successfully synced and compressed agents.json")
    except Exception as e:
        print(f"Error syncing agents: {e}")

if __name__ == "__main__":
    sync_agents()