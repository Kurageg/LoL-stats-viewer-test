import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("RIOT_API_KEY")

if not api_key:
    print("Error: RIOT_API_KEY not found in .env file.")
else:
    region = "ru" # Your region
    gameName = "kur4ga" # Your nickname
    tagLine = "1111"
    
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={api_key}"
    headers = {
        "X-Riot-Token": api_key
    }
    
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f"Summoner Name: {data['gameName']}")
    else:
        print(f"Failed to fetch data: {response.status_code}")
