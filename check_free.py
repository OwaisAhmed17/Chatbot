from datetime import datetime, timedelta
import datetime
import datefinder
import pprint
from dateutil.tz import tzoffset
from check_avail import check_availability 
from cal_auth import cal_id


def free_times(start , email):
    matches = list(datefinder.find_dates(start))
    
    if len(matches):
        tstart = matches[0]
        
        tstop = tstart + timedelta(minutes=1439)
    
    tstart1 = tstart.strftime("%Y-%m-%dT%H:%M:%S+05:30")
    tstop1 = tstop.strftime("%Y-%m-%dT%H:%M:%S+05:30")
    non_work_start = tstart.strftime("%Y-%m-%dT19:00:00+05:30")
    non_work_end = tstop.strftime("%Y-%m-%dT08:00:00+05:30")
    appointments = check_availability( tstart1, tstop1, email )
    appointments.append({'start':non_work_start,'end':non_work_end})
    
    
    
    
    for i in appointments:
        a = list(datefinder.find_dates(i['start']))
        i['start'] = a[0]
        a = list(datefinder.find_dates(i['end']))
        i['end'] = a[0]
    
    appointments = tuple(appointments)
    
    tstart = tstart.replace(tzinfo=tzoffset(None,19800))
    tstop = tstop.replace(tzinfo=tzoffset(None,19800))

    tp = [(tstart , tstart)]
    free_time = []
    for t in appointments:
        tp.append( ( t['start'] , t['end'] ) )
    tp.append( (tstop , tstop) )
    for i,v in enumerate(tp):
        if i > 0:
            if (tp[i][0] - tp[i-1][1]) > timedelta(seconds=0):
                tf_start = tp[i-1][1]
                delta = tp[i][0] - tp[i-1][1]
                tf_end = tf_start + delta
                free_time.append( [tf_start.strftime("%H:%M on %d-%m") ,tf_end.strftime("%H:%M on %d-%m") ] )

    return free_time




