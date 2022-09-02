import json
###
### grab CFB games on the selected date
###
from dotenv import load_dotenv
import requests
import os
import arrow as ar

load_dotenv()

url = "https://sportspage-feeds.p.rapidapi.com/games"
test = 1

if test == 1:
	with open("game.json", 'r') as file:
		games = json.load(file)

else:
	querystring = {"league":"NCAAF","date":"2022-09-03"}

	headers = {
		"X-RapidAPI-Key": "9a8920ea2cmsh411e3c80ba9253dp1d7d7cjsn86dc326be333",
		"X-RapidAPI-Host": "sportspage-feeds.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)
	games = json.loads(response.text)
#print(response.text)


###
### Get Weather Key info based on City and State
###

#test_loc = games['results'][0]['venue']
#print(test_loc)

for g in games['results']:
	gametime_base = ar.get(g['schedule']['date'], 'YYYY-MM-DDTHH:mm:ss.000Z')
	gametime = gametime_base.to('local').format()
	print(g['summary'] , " - " , gametime, "--------------")
	test_loc = g['venue']
	#url = "https://accuweatherstefan-skliarovv1.p.rapidapi.com/searchLocation"
	url = "http://dataservice.accuweather.com/locations/v1/search"
	#payload = f"query={test_loc['city']}%20{test_loc['state']}&apiKey={os.getenv('ACCU_API_KEY')}"
	payload = f"{url}?apikey={os.getenv('ACCU_API_KEY')}&q={test_loc['city']}%20{test_loc['state']}"
	print(payload)

	headers = {
		"content-type": "application/json",
		"Accept": "application/json"
		#"X-RapidAPI-Key": "9a8920ea2cmsh411e3c80ba9253dp1d7d7cjsn86dc326be333",
		#"X-RapidAPI-Host": "AccuWeatherstefan-skliarovV1.p.rapidapi.com"
	}

	#response = requests.request("POST", url, data=payload, headers=headers)
	response = requests.request("GET", payload, headers=headers, data={})
	print(response.status_code)
	#print(response.text)
	if response.status_code == 200:
		accu = json.loads(response.text)
		loc_key = accu[0]["Key"]
		#329302
		weather_url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{loc_key}?apikey={os.getenv('ACCU_API_KEY')}"

		#print(weather_url)
		headers = {
			"content-type": "application/json",
			"Accept": "application/json"
			#"X-RapidAPI-Key": "9a8920ea2cmsh411e3c80ba9253dp1d7d7cjsn86dc326be333",
			#"X-RapidAPI-Host": "AccuWeatherstefan-skliarovV1.p.rapidapi.com"
		}

		#response = requests.request("POST", url, data=payload, headers=headers)
		response = requests.request("GET", weather_url, headers=headers, data={})
		if response.status_code == 200:
			forecast = json.loads(response.text)

			print(response.status_code)
			#print(response.text)
			# grab ['DailyForecasts'][0] if ['Date'] == 'YYYY-MM-DDTHH:MM:SS-04:00' (desired date)
			print(forecast['DailyForecasts'][0]['Date'][:10])
			saturday =  [s for s in forecast['DailyForecasts'] if s['Date'][:10] == gametime[:10]] #'YYYY-MM-DDTHH:MM:SS-04:00'
			print(saturday)
			# get saturday[0]['Day']['HasPrecipitation'] & saturday[0]['Day']['IconPhrase']
			sat_day_rain = saturday[0]['Day']['HasPrecipitation']
			sat_day_icon = saturday[0]['Day']['IconPhrase']

			if sat_day_rain == True: 
				print(saturday[0]['Day']['PrecipitationType'], " - " , saturday[0]['Day']['PrecipitationIntensity']) # "Rain",
			else:
				print("no rain for: ", g["summary"])
			
			# get saturday[0]['Night']['HasPrecipitation'] & saturday[0]['Night']['IconPhrase'] 
			sat_night_rain = saturday[0]['Night']['HasPrecipitation']
			sat_night_icon = saturday[0]['Night']['IconPhrase']

			if sat_night_rain == True: 
				print(saturday[0]['Night']['PrecipitationType'], " - ", saturday[0]['Night']['PrecipitationIntensity'])  #"Moderate"
			else:
				print("no rain for: ", g["summary"])

		else:
			print("bad request - ", response.text)

else:
	print("No location found")


