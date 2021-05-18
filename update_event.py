from cal_auth import service
import datefinder
from datetime import datetime, timedelta
from check_avail import check_availability
from cal_auth import cal_id


def reschedule_event(start):
    result = service.events().list(calendarId=cal_id, timeZone="Asia/Kolkata").execute()
    matches = list(datefinder.find_dates(start))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + timedelta(hours=1)
        start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S+05:30")
    
    
    event_exist = False
    for i in result['items']:
        if i['start']['dateTime']==start_time:
            event_exist = True
            event=i
            eventId=event['id']
            attendee=event['attendees']
            new_time=input("Enter the new date and time")
            matches = list(datefinder.find_dates(new_time))
            if len(matches):
                start_time = matches[0]
                end_time = start_time + timedelta(hours=1)
                start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S+05:30")
                end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S+05:30")
            for i in attendee:
                a=check_availability(start_time,end_time,i['email'])
                if a==[]:
                    avail=True
                else:
                    avail=False
                    break
            
            
    if event_exist==True and avail==True:
        event['start']['dateTime']=start_time
        event['end']['dateTime']=end_time
        service.events().update(calendarId='primary', eventId=eventId, body=event , conferenceDataVersion=1).execute()
        return print("Meeting rescheduled to ",start)
    elif event_exist==False:
        return print("There is no event during ",start)  

    if avail==False:
        return print("Few of the attendees aren't available during ", start)





def add_member(start , attendees):
    result = service.events().list(calendarId=cal_id, timeZone="Asia/Kolkata").execute()
    matches = list(datefinder.find_dates(start))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + timedelta(hours=1)
        start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S+05:30")
        end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S+05:30")
    attendee=[]
    event_exist=False
    for i in result['items']:
        if i['start']['dateTime']==start_time:
            event=i
            eventId=event['id']
            attendee=event['attendees']
            event_exist=True
            
            for i in attendees:
                attendee.append({'email': i, 'responseStatus':'needsAction'})
            
            for i in attendees:
                a=check_availability(start_time,end_time,i)
                if a==[]:
                    avail=True
                else:
                    avail=False
                    break
            event['attendees']=attendee
    if event_exist==True and avail==True:
        service.events().update(calendarId='primary', eventId=eventId, body=event , sendUpdates='all' , conferenceDataVersion=1).execute()
        return 0
    elif event_exist == False:
        return 1

    if avail==False:
        return 2




        
    

