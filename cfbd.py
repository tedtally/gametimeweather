import json
###
### grab CFB games on the selected date
###
from dotenv import load_dotenv
import requests
import os
import arrow as ar

load_dotenv()

url = os.getenv("CFBD_API_BASE_URL")
test = 1

#get weekly schedule

year = 2022
week = 2
querystring = f'year={year}&week={week}&seasonType=regular'

gameurl = f'{url}games?{querystring}'
headers = {
    "accept": "application/json",
    "Authorization": os.getenv("CFBD_API_KEY")
}

print(gameurl)

response = requests.request("GET", gameurl, headers=headers)
games = json.loads(response.text)
print(response.text)
