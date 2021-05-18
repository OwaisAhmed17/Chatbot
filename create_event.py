
import datefinder
from datetime import datetime, timedelta
from check_avail import check_availability
from cal_auth import service
from cal_auth import cal_id


def Create_event(start_time_str, summary, attendee, duration=1, description=None, location=None):
    
    attendees = [{'email': cal_id , 'responseStatus': 'accepted'}]
    for i in attendee:
        attendees.append({'email':i,'resposnseStatus':'needsAction'})
    matches = list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + timedelta(hours=duration)
    
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S+05:30"),
            'timeZone': 'Asia/Kolkata'
            
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S+05:30"),
            'timeZone': 'Asia/Kolkata'
            
        },
        "conferenceData": {
            "createRequest": {
                "conferenceSolutionKey": {
                "type": "hangoutsMeet"
                },
            "requestId": "tnc-ihrx-uyk"
            }
        },
        'status':'confirmed',
        
        
        'location' : 'Bangalore, KA',
        'attendees': attendees,
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    
    
    # for i in attendees:
    #     a=check_availability(start_time.strftime("%Y-%m-%dT%H:%M:%S+05:30"),end_time.strftime("%Y-%m-%dT%H:%M:%S+05:30"),i['email'])
    #     if a==[]:
    #         avail=True
            
    #     else:
    #         avail=False
    #         break

    maxAttendees = 5
    sendNotifications = True
    sendUpdates = 'all'
    # if avail==True:
    service.events().insert(calendarId='primary', maxAttendees=maxAttendees, sendNotifications=sendNotifications, sendUpdates=sendUpdates, body=event, conferenceDataVersion=1).execute()
    return True
    # else:
    #     return False

