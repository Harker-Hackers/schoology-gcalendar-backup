import datetime
from json import loads
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import schoolopy

days = [datetime.date.today()]
for i in [1, 2, 3, 4, 5, 6]:
    days.append(str(datetime.date.today() + datetime.timedelta(days=i)))

sc_conf = loads(open('schoology.json', 'r').read())
sc = schoolopy.Schoology(schoolopy.Auth(sc_conf['key'], sc_conf['secret']))
me = sc.get_me()
assignments = sc.get_assignments(2692876554)

me['tz_offset'] = str(me['tz_offset'])
if len(me['tz_offset'].replace('-', '')) == 1:
    place = me['tz_offset'].index('-') + 1
    me['tz_offset'] = me['tz_offset'][:place] + '0'  + me['tz_offset'][place:]
me['tz_offset'] = me['tz_offset'] + ':00'

##########################
assignment = assignments[0]
if str(assignment['due'][:assignment['due'].index(' ')]) in days:
    print(assignment['title'])
    
exit()

due = assignment['due'].replace(' ', 'T') + '-' + me['tz_offset']

try:
    creds = pickle.load(open('token.pickle', 'rb'))
except FileNotFoundError:
    raise Exception('Not authorized. Run "python3 sc-calendar login --help".')

service = build('calendar', 'v3', credentials=creds)
event = {
    'summary': assignment['title'],
    'description': assignment['description'] + '\n\nYou can view this assignment at ' + assignment['web_url'],
    'start': {
        'dateTime': due,
        'timeZone': me['tz_name']
    },
    'end': {
        'dateTime': due,
        'timeZone': me['tz_name']
    },
    'reminders': {
        'useDefault': True,
    }
}

service.events().insert(calendarId='primary', body=event).execute()