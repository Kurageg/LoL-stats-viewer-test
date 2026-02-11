import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.geten("RIOT_API_KEY")

if not api_key:
    print("Error: RIOT_API_KEY not found in .env file.")
else:
    region = "ru1" # Your region
    summoner_name = "Doublelift" # Your nickname
    
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    headers = {
        "X-Riot-Token": api_key
    }
    
    response = requests.get(url, headers=headers)

    if response.status_status == 200:
        data = response.json()
        print(f"Summoner Level: {data['summonerLevel']}")
    else:
        print(f"Failed to fetch data: {response.status_code}")
