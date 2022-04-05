import requests
from requests_html import HTMLSession
from datetime import datetime

current_date = datetime.now()

url = "https://www.bellingcat.com/workshops"
session = HTMLSession()
response = session.get(url)

events = response.html.find('.event__content')
event_candidates = []
for event in events:
    candidate = event.text
    if "FULL" in candidate:
        continue
    candidate_date_range = ' '.join(candidate.split(' ')[:2])[:-1]
    candidate_date_start = ''.join(candidate_date_range.split('-')[0:1])
    candidate_date_start = candidate_date_start.split(' ')
    if len(candidate_date_start[1]) < 2:
        candidate_date_start[1] = '0' + candidate_date_start[1]
    candidate_date_start = ' '.join(candidate_date_start) + ' 2022'
    cds_stamp = datetime.strptime(candidate_date_start, '%B %d %Y')
    
    if cds_stamp > current_date:
        event_candidates.append(candidate)
    
print('\n'.join(event_candidates))
