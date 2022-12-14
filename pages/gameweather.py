import json
import requests
import os
import arrow as ar
from dotenv import load_dotenv

def main():
	load_dotenv()

def load_venues():
	if os.path.exists('venues.json'):
		# read file
		with open('venues.json', 'r') as f:
			venues = json.load(f)
			citystates = [{"city": c['city'], "state": c['state']} for c in venues]
			return citystates
	else:
		return None


def get_forecast(locations,gametime):
	for g in locations:
    	#get locationkey
		url = "http://dataservice.accuweather.com/locations/v1/search"
		#payload = f"query={test_loc['city']}%20{test_loc['state']}&apiKey={os.getenv('ACCU_API_KEY')}"
		payload = f"{url}?apikey={os.getenv('ACCU_API_KEY')}&q={g['city']}%20{g['state']}"
		print(payload)

		headers = {
			"content-type": "application/json",
			"Accept": "application/json"
		}

		response = requests.request("GET", payload, headers=headers, data={})
		print(response.status_code)
		#print(response.text)
		if response.status_code == 200:
			accu = json.loads(response.text)
			loc_key = accu[0]["Key"]
			weather_url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{loc_key}?apikey={os.getenv('ACCU_API_KEY')}"
			headers = {
				"content-type": "application/json",
				"Accept": "application/json"
			}

			response = requests.request("GET", weather_url, headers=headers, data={})
			if response.status_code == 200:
				forecast = json.loads(response.text)
				saturday =  [s for s in forecast['DailyForecasts'] if s['Date'][:10] == gametime[:10]] #'YYYY-MM-DDTHH:MM:SS-04:00'
				print(saturday)
				with open(f"{away}_vs_{home}.json", 'w+') as file:
					file.write(json.dumps(saturday))	
						
				if len(saturday) >0:
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


if __name__ == "__main__":
	main()
