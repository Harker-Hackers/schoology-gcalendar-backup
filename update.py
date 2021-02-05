import click
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

try:
    creds = pickle.load(open('token.pickle', 'rb'))
except FileNotFoundError:
    raise Exception('Not authorized. Run "python3 sc-calendar login --help".')

service = build('calendar', 'v3', credentials=creds)
event = {
    'summary': 'Yeet',
    'description': '',
    'start': {
        'dateTime': '2021-02-05T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles'
    },
    'end': {
        'dateTime': '2021-02-05T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles'
    },
    'reminders': {
        'useDefault': True,
    },
}

service.events().insert(calendarId='primary', body=event).execute()