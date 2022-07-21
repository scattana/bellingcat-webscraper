import requests
from requests_html import HTMLSession
from datetime import datetime
import smtplib
from retrieve import access_secret_version
import os


current_date = datetime.now()

url = "https://www.bellingcat.com/workshops"
session = HTMLSession()
response = session.get(url)

fnot = open("/home/scattanach1/bellingcat-webscraper/events/notifications.txt", "r")
contents = fnot.readlines()

events = response.html.find('.event__content')
event_candidates = []
for event in events:
    candidate = event.text

    candidate_found = False

    # read list of events for which notifications have already been sent
    # if notification was already sent, skip
    for line in contents:
        if line.strip() == candidate.split('\n')[0].strip():
            candidate_found = True
            break

    if candidate_found:
        print("notification already sent - skipping")
        continue

    if "FULL" in candidate:
        print("event full - skipping")
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
    else:
        print("event date in the past - skipping")
    
# if email should be sent, retrieve credentials
if len(event_candidates) > 0:
    PROJECT_ID = os.getenv("PROJECT_ID")
    SECRET_ID = os.getenv("SECRET_ID")
    VERSION_ID = os.getenv("VERSION_ID")
    from_email = os.getenv("APP_EMAIL_OUTGOING")
    to_email = os.getenv("APP_EMAIL_RECIPIENT")

    # use ID values to retrieve email API key from secret manager
    key = access_secret_version(PROJECT_ID, SECRET_ID, VERSION_ID)

    # compose message and start SMTP job
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    message_raw = 'New Bellingcat events found:\n\n' + '\n\n'.join(event_candidates) + '\n\n---------\nBEE-DOO-BEE-DOO hi hope you are having a wonderful day, Bean!'
    subject = 'Bellingcat Web Scraper - New Events Found'
    message = 'Subject: {}\n\n{}'.format(subject, message_raw)
    smtpobj.starttls()

    message = message.encode("utf-8")
    
    smtpobj.login(from_email,key)
    smtpobj.sendmail(from_email, to_email, message)
    smtpobj.quit()

    # append to the "already notified" file
    with open("/home/scattanach1/bellingcat-webscraper/events/notifications.txt", "a") as f2:
        lines_to_write = [candidate.split('\n')[0] + '\n' for candidate in event_candidates]
        f2.writelines(lines_to_write)
        


