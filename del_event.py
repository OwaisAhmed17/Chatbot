from cal_auth import service
import datefinder
from datetime import datetime, timedelta
from check_avail import check_availability
from cal_auth import cal_id


def delete_event(start):
    result = service.events().list(calendarId=cal_id, timeZone="Asia/Kolkata").execute()
    matches = list(datefinder.find_dates(start))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + timedelta(hours=1)
        start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S+05:30")
        end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S+05:30")
    
    
    event_exist = False
    for i in result['items']:
        if i['start']['dateTime']==start_time and i['summary']=='Meet':
            event_exist = True
            event=i
            eventId=event['id']
    
    
            
    if event_exist==True:
        service.events().delete(calendarId='primary', eventId=eventId , sendUpdates='all').execute()
        return True
    else:
        return False





