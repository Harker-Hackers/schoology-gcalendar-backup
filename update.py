import datetime
from json import loads
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import schoolopy

sc_conf = loads(open('schoology.json', 'r').read())
sc = schoolopy.Schoology(schoolopy.Auth(sc_conf['key'], sc_conf['secret']))
me = sc.get_me()
assignments = sc.get_assignments(section_id=2692851162)

today=datetime.datetime.today()

recentAssignments=[]
for i in assignments:
    assignmentTime = datetime.datetime.strptime(i.due, "%Y-%m-%d %H:%M:%S")
    tDelta=(assignmentTime-today).days
    if (0<=tDelta<=6):
        recentAssignments.append(i)
        print("Assignment: " + str(i))

me['tz_offset'] = str(me['tz_offset'])
if len(me['tz_offset'].replace('-', '')) == 1:
    place = me['tz_offset'].index('-') + 1
    me['tz_offset'] = me['tz_offset'][:place] + '0'  + me['tz_offset'][place:]
me['tz_offset'] = me['tz_offset'] + ':00'

##########################

    
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