import json
from dotenv import load_dotenv
import requests
import os
import arrow as ar

def main():
    load_dotenv()

def get_lines(year, gameId):

    # betting lines
    # https://api.collegefootballdata.com/lines?gameId=401420807&year=2022&week=2&seasonType=regular

        url = os.getenv("CFBD_API_BASE_URL")
        test = 1
    
        #get weekly schedule
        headers = {
            "accept": "application/json",
            "Authorization": os.getenv("CFBD_API_KEY")
        }
        #year = 2022
        #week = 2
        querystring = f'gameId={gameId}&year={year}'
        lineurl = f'{url}lines?{querystring}'
        #print(lineurl)
    
        #fcs
        response = requests.request("GET", lineurl, headers=headers)
        lines = json.loads(response.text)
        print(lines)
    
        if len(lines) == 0:
            return None
        elif len(lines[0]['lines']) == 0:
            return None
        else:
            return lines[0]['lines'][0]

def get_venue_location(venue):
    if os.path.exists('venues.json'):
        # read file
        with open('venues.json', 'r') as f:
            venues = json.load(f)
        citystate = [{"city": c['city'], "state": c['state']} for c in venues if c["name"] == venue]
        if len(citystate) > 0:
            return citystate[0]
        else:
            return {"city": "N/A", "state": "N/A"}
    else:
        return {"city": "N/A", "state": "N/A"}

def build_list(games, division):
    games_results = []
    for g in games:
        print(g)
        game_data = {}
        gametime_base = ar.get(g['start_date'], 'YYYY-MM-DDTHH:mm:ss.000Z')
        gametime = gametime_base.to('local').format()     
        game_data["division"] = division
        lines = get_lines(gametime[0:4],g["id"])
        print(lines)
        if lines is not None:
            game_data["lines_spread"] = lines["formattedSpread"]
            game_data["lines_open_thread"] = lines["spreadOpen"]
            game_data["lines_OU"] = lines["overUnder"]
            game_data["lines_open_OU"] = lines["overUnderOpen"]
            game_data["lines_homeML"] = lines["homeMoneyline"]
            game_data["lines_awayML"] = lines["awayMoneyline"]
        else:
            game_data["lines_spread"] = None
            game_data["lines_open_thread"] = None
            game_data["lines_OU"] = None
            game_data["lines_open_OU"] = None
            game_data["lines_homeML"] = None
            game_data["lines_awayML"] = None
        game_data['game_date'] = gametime[:10]
        game_data['game_time'] = gametime[11:]
        game_data['summary'] = f"{g['away_team']} @ {g['home_team']}"
        game_data['venue_name'] = g['venue']
        game_data['venue_city'] = get_venue_location(g['venue'])['city']
        game_data['venue_state'] = get_venue_location(g['venue'])['state']
        game_data['neutral_site'] = g['neutral_site']
        game_data['away_team'] = g["away_team"]
        if "away_conference" in g:
            game_data['away_team_conference'] = g["away_conference"]
        else:
            game_data['away_team_conference'] = 'Independent'

        game_data['home_team'] = g["home_team"]
        if "home_conference" in g:
            game_data['home_team_conference'] = g["home_conference"]
        else:
            game_data['home_team_conference'] = 'Independent'
        
        game_data['game_id'] = g['id']
        game_data['conference_game'] = g['conference_game']
        games_results.append(game_data)
    return games_results

def get_games(startdate):
    #https://api.collegefootballdata.com/games?year=2022&week=2&seasonType=regular&division=fcs or fbs"
    url = os.getenv("CFBD_API_BASE_URL")
    test = 1

    #get weekly schedule
    headers = {
        "accept": "application/json",
        "Authorization": os.getenv("CFBD_API_KEY")
    }
    with open('cfb_calendar.json', 'r') as f:
        schedule = json.load(f)
    
    year = startdate[0:4]
    week = [w for w in schedule if startdate < w["firstGameStart"]][0]
    division= 'fbs'
    querystring = f'year={year}&week={week["week"]}&seasonType=regular&division={division}'
    gameurl = f'{url}games?{querystring}'
    print(gameurl)

    #fbs
    response = requests.request("GET", gameurl, headers=headers)
    games = json.loads(response.text)
    games_results = build_list(games, division)


    division= 'fcs'
    querystring = f'year={year}&week={week["week"]}&seasonType=regular&division={division}'
    gameurl = f'{url}games?{querystring}'
    print(gameurl)
    response = requests.request("GET", gameurl, headers=headers)
    games = json.loads(response.text)
    games_results.append(build_list(games, division)[0])
    with open(f'cfb_games_asof_week{week["week"]}.json', 'w+') as f:
        json.dump(games_results, f, indent=4)

    return games_results

def get_stats(year, team, conference=None):
    pass

if __name__ == "__main__":
    main()
