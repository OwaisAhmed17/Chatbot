import datefinder
from datetime import datetime, timedelta
from check_avail import check_availability
from cal_auth import service, service_mail
from cal_auth import cal_id
from send_email import notify_task


def assign(start_time_str, summary, attendee, description):
    
    attendees = [{'email': cal_id , 'responseStatus': 'accepted'}]
    for i in attendee:
        attendees.append({'email':i,'resposnseStatus':'accepted'})
    matches = list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + timedelta(hours=1)
    
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
        'status':'confirmed',
        'transparency':'transparent',
        
        'location' : 'Bangalore, KA',
        'attendees': attendees,
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 3*60},
            ],
        },
    }
    maxAttendees = 5
    sendUpdates = 'none'
    service.events().insert(calendarId='primary', maxAttendees=maxAttendees, sendUpdates=sendUpdates, body=event).execute()
    st = ''
    j=1
    for i in attendee:
        if j != len(attendee):
            st = st + i + ','
            j+=1
        else:
            st = st + i
    notify_task(description , start_time.strftime("%I:%M %p on %d %B, %Y"), st)



