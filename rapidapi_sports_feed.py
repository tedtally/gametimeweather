import json
from dotenv import load_dotenv
import requests
import sys, os
import arrow as ar



def main():
    load_dotenv()

def get_games(gamedate):
    url = "https://sportspage-feeds.p.rapidapi.com/games"

    # if file "game_{gamedate}.json exists
    if os.path.exists(f'game_{gamedate}.json'):
        # read file
        with open(f'game_{gamedate}.json', 'r') as f:
            games = json.load(f)
    else:
        # get games from rapidapi
        querystring = {"league":"NCAAF","date": gamedate}
        headers = {
            "X-RapidAPI-Key": os.getenv('X-RapidAPI-Key'),
            "X-RapidAPI-Host": "sportspage-feeds.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        games = json.loads(response.text)
        # write games to file
        with open(f'game_{gamedate}.json', 'w+') as f:
            json.dump(games, f, indent=4)
    
    games_results = []

    for g in games['results']:
        game_data = {}
        gametime_base = ar.get(g['schedule']['date'], 'YYYY-MM-DDTHH:mm:ss.000Z')
        gametime = gametime_base.to('local').format()        
        game_data['game_date'] = gametime[:10]
        game_data['game_time'] = gametime[11:]
        game_data['summary'] = g['summary']
        game_data['venue_name'] = g['venue']['name']
        game_data['venue_city'] = g['venue']['city']
        game_data['venue_state'] = g['venue']['state']
        game_data['neutral_site'] = g['venue']['neutralSite']
        game_data['away_team'] = g['teams']["away"]["team"]
        if "conference" in g['teams']["away"]:
            game_data['away_team_conference'] = g['teams']["away"]["conference"]
        else:
            game_data['away_team_conference'] = 'Independent'

        game_data['home_team'] = g['teams']["home"]["team"]
        if "conference" in g['teams']["home"]:
            game_data['home_team_conference'] = g['teams']["home"]["conference"]
        else:
            game_data['home_team_conference'] = 'Independent'
        
        game_data['game_id'] = g['gameId']
        game_data['conference_game'] = g['details']['conferenceGame']
        games_results.append(game_data)
        #print(g['summary'] , " - " , gametime, "--------------")
        #test_loc = g['venue']
    return games_results

if __name__ == "__main__":
    main() 
