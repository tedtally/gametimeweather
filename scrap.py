import arrow as ar
from datetime import datetime, timedelta
import json

startdate = ar.utcnow().to('local').format('YYYY-MM-DD')

#startdate = '2022-09-08'
weekday = 5
"""
@startdate: given date, in format '2013-05-25'
@weekday: week day as a integer, between 0 (Monday) to 6 (Sunday)
"""
d = datetime.strptime(startdate, '%Y-%m-%d')
t = timedelta((7 + weekday - d.weekday()) % 7)
print((d + t).strftime('%Y-%m-%d'))

with open('venues.json', 'r') as f:
    venues = json.load(f)

citystate = [{"city": c['city'], "state": c['state']} for c in venues if c["name"] == "Abbott Memorial Alumni Stadium"]

print(citystate[0]['city'])

with open('cfb_calendar.json', 'r') as f:
    schedule = json.load(f)

print(startdate[0:4])
year = startdate[0:4]
week = [w for w in schedule if startdate < w["firstGameStart"]][0]
print(year)
print(week)