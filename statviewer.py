import os
import requests
from dotenv import load_dotenv

load_dotenv()

# A function to find champions by their key bc when you ask for champions with high mastery it gives you only their key
def find_champion_by_key(champ_data, search_key):
    for champ in champ_data.values():
        if champ["key"] == str(search_key):
            return champ
    return None

api_key = os.getenv("RIOT_API_KEY")

if not api_key:
    print("Error: RIOT_API_KEY not found in .env file.")
else:
    region = input("Region that you play in (ex: ru, euw1, na1): ") # Your region
    gameName = input("Your IGN (In Game Name): ") # Your nickname
    tagLine = input("Your Tag (ex: #1111): ") # Your Tag

    # Getting champions to show mastery 
    url = f"https://ddragon.leagueoflegends.com/cdn/16.3.1/data/en_US/champion.json"
    response = requests.get(url)
    championData = response.json()
    champions = championData["data"]

    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        puuid = data['puuid']
        print(f"Summoner: {data['gameName']}#{data['tagLine']}") 

        # Getting ranked stats
        url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}?api_key={api_key}" 
        response = requests.get(url)
        data = response.json()

        if len(data) > 0:
        # Making a new variable to save solo/flex queue stats
            RankedSoloStats = data[0] 
            RankedFlexStats = data[1]

            print("SOLO QUEUE:")
            print(f"Rank: {RankedSoloStats['tier']} {RankedSoloStats['rank']} {RankedSoloStats['leaguePoints']}LP")
            print(f"Wins: {RankedSoloStats['wins']} Losses: {RankedSoloStats['losses']}")
            print("FLEX QUEUE:")
            print(f"Rank: {RankedFlexStats['tier']} {RankedFlexStats['rank']} {RankedFlexStats['leaguePoints']}LP")
            print(f"Wins: {RankedFlexStats['wins']} Losses: {RankedFlexStats['losses']}")
        else:
            print("No ranked stats (Is ranked available?/Have you played ranked before?)")
        url = f"https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top?count=1&api_key={api_key}"
        response = requests.get(url)
        data = response.json()
        bestChamp = data[0]
        searchkey = bestChamp['championId']
        result = find_champion_by_key(champions, searchkey)
        
        print(f"Highest Mastery level on {result['name']}: Level {bestChamp['championLevel']}, {bestChamp['championPoints']} Mastery points ") 
    else:
        print(f"Failed to fetch data: {response.status_code}")
