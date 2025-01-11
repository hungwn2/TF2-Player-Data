import requests
import pandas as pd
from django.shortcuts import render

API_KEY = "your_steam_api_key"
TF2_APP_ID = 440

def index(request):
    return render(request, "players/index.html")

def stats(request):
    steam_id = request.GET.get("steam_id")  # get steam ID from query parameters
    if not steam_id:
        return render(request, "players/index.html", {"error": "Steam ID is required."})

    # get data from the TF2 API
    url = f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/"
    params = {"appid": TF2_APP_ID, "key": API_KEY, "steamid": steam_id}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return render(request, "players/index.html", {"error": "Failed to fetch data from TF2 API."})

    data = response.json().get("playerstats", {}).get("stats", [])
    df = pd.DataFrame(data)
#get values
    stats = {
        "kills": int(df.loc[df["name"] == "kill_count", "value"].values[0]),
        "deaths": int(df.loc[df["name"] == "death_count", "value"].values[0]),
        "headshots": int(df.loc[df["name"] == "headshots", "value"].values[0]),
    }
    #add kd rat
    stats["kd_ratio"] = stats["kills"] / stats["deaths"]

    return render(request, "players/stats.html", {"stats": stats})
