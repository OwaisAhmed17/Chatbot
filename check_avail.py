from cal_auth import service
import datefinder
from datetime import datetime, timedelta

def check_availability(start,end, ID):
    body = {
      "timeMin": start,
      "timeMax": end,
      "timeZone": 'Asia/Kolkata',
      "items": [{"id":ID}]
    }

    eventsResult = service.freebusy().query(body=body).execute()
    
    a=list(eventsResult.items())
    b=list(a[3][1].items())
    out=[]
    for i in b:
      for j in i:
        out.append(j)
    return(out[1]['busy'])







    


