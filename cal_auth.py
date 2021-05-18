
from Google import Create_Service
import datefinder
from datetime import datetime, timedelta
import pytz


service = []

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

CLIENT = 'client_secret.json'
API = 'gmail'
VERSION = 'v1'
SCOPE = ['https://mail.google.com/']
service_mail = Create_Service(CLIENT,API,VERSION,SCOPE)

manager = False
calendar_list_entry = service.calendarList().get(calendarId='primary').execute()
cal_id = calendar_list_entry['id']
if cal_id == 'owaisahmed29@gmail.com':
    manager = True

rule = {
    'scope': {
        'type': 'default',
        
    },
    'role': 'freeBusyReader'
}

created_rule = service.acl().insert(calendarId='primary', body=rule).execute()


