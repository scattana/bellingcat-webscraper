import requests
from requests_html import HTMLSession
from datetime import datetime
import smtplib
from retrieve import access_secret_version


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
    

from_email = 'scattanach1@gmail.com'
to_email = 'aleah@umich.edu'
smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
message_raw = 'New Bellingcat events found:\n\n' + '\n\n'.join(event_candidates) + '\n\n---------\nBEE-DOO-BEE-DOO hi hope you are having a wonderful day, Bean!'
subject = 'Bellingcat Web Scraper - New Events Found'
message = 'Subject: {}\n\n{}'.format(subject, message_raw)
smtpobj.starttls()

# retrieve API key
access_secret_version(PROJECT_ID, SECRET_ID, VERSION_ID)

smtpobj.login('scattanach1@gmail.com','')
smtpobj.sendmail(from_email, to_email, message)
smtpobj.quit()
