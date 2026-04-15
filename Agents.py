import requests

def sync_agents():
    url = "https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/en/agents.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Save the content exactly as it is
        with open("agents_en.json", "wb") as f:
            f.write(response.content)
            
        print("Successfully synced agents.json")
    except Exception as e:
        print(f"Error syncing agents: {e}")

if __name__ == "__main__":
    sync_agents()