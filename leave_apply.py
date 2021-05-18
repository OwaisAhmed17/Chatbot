import datefinder
from datetime import datetime, timedelta
from cal_auth import cal_id
from send_email import send_mail

def apply_leave(date, reason):
    
    date = str(date)
    matches = list(datefinder.find_dates(date))
    
    if len(matches):
        tstart = matches[0]

    dates = tstart.strftime("%d %B , %Y")
    send_mail(dates,reason)

    

