# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"





from cal_auth import cal_id
from create_event import Create_event 
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from del_event import delete_event
from update_event import add_member
from rasa_sdk.events import SlotSet
from rasa_sdk.events import FollowupAction
from check_free import free_times
from cal_auth import manager
from leave_apply import apply_leave
from assign_task import assign
from check_avail import check_availability
from rasa_sdk import Tracker, FormValidationAction
import datefinder
from datetime import datetime, timedelta

#
#
class RoleCheck(Action):
    def name(self) -> Text:
        return "action_role_check"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text,Any]]:
        if manager == True:
            role = 'manager'
        else:
            role = 'employee'
        dispatcher.utter_message("hey {0}".format(cal_id))
        return[SlotSet('role',role)]

class AssignTask(Action):
    def name(self) -> Text:
        return "action_assign_task"
    
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text,Any]]:
        if manager == True:
            ppl = tracker.get_slot('email1')
            time = tracker.get_slot('deadline')
            description = tracker.latest_message['text']
            assign(time,"Task",ppl,description)
            dispatcher.utter_message("Task has been assigned.")
            return [SlotSet("email1",None),SlotSet("deadline",None)]
        else:
            dispatcher.utter_message("You are not authorized to assign tasks.")
            return [SlotSet("email1",None),SlotSet("deadline",None)]



class ActionScheduleMeet(Action):

    def name(self) -> Text:
        return "action_schedule_meet"

    async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: "DomainDict") -> List[Dict[Text, Any]]:
        attendee = tracker.get_slot("email")
        timing = tracker.get_slot("time")
        status = Create_event(timing, 'Meet' ,attendee)
        if status == True:  
            
            dispatcher.utter_message("The meeting has been scheduled")
        return[SlotSet("email",None),SlotSet("time",None)]
            
class ValidateAssignForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_assign_task_form"

    def validate_email1(self,slot_value: Any,dispatcher: CollectingDispatcher,tracker: Tracker,domain: "DomainDict") -> Dict[Text, Any]:      
        attendees = tracker.get_slot('email1')
        a=[]
        if type(attendees) is str:
            a.append(attendees)
            return {'email1':a}
        else :
            return {'email1' : attendees}    

class ValidateScheduleForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_schedule_form"

    def validate_email(self,slot_value: Any,dispatcher: CollectingDispatcher,tracker: Tracker,domain: "DomainDict") -> Dict[Text, Any]:
        attendees = tracker.get_slot('email')
        a=[]
        if type(attendees) is str:
            a.append(attendees)
            return {'email':a}
        else :
            return {'email' : attendees}

        

    
    def validate_time(self,slot_value: Any,dispatcher: CollectingDispatcher,tracker: Tracker,domain: "DomainDict") -> Dict[Text, Any]:
        attendees = tracker.get_slot('email')
        timing = tracker.get_slot('time')
        matches = list(datefinder.find_dates(timing))
        if len(matches):
            start_time = matches[0]
            end_time = start_time + timedelta(hours=1)

        
        for i in attendees:
            a=check_availability(start_time.strftime("%Y-%m-%dT%H:%M:%S+05:30"),end_time.strftime("%Y-%m-%dT%H:%M:%S+05:30"),i)
            if a==[]:
                avail=True
            
            else:
                avail=False
                break
        
        non_work = [19,20,21,22,23,0,1,2,3,4,5,6,7]
        if start_time.hour in non_work:
            avail=False

        if avail == True:
            return {"time": timing}
        else:
            str = "Not all members are free during the time you provided. Do not select a time between 7PM and 8AM. \n"
            for i in attendees:
                a = free_times(timing,i)
                str = str + "{0} is free during the below mentioned times \n".format(i)
                for j in a:
                    str = str+ "{t1} to {t2} \n".format(t1=j[0],t2=j[1])
            str = str + "Please choose a time which lies in the free times of all the attendees \n"
            dispatcher.utter_message(text="{0}".format(str))
            return {"time" : None}
        


class ScheduleMeetForm(Action):
    def name(self) -> Text:
            return "schedule_form"

    async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: "DomainDict") -> List[Dict[Text, Any]]:
        
        required_slots = ["email", "time"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]

class AssignTaskForm(Action):
    def name(self) -> Text:
            return "assign_task_form"

    async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: "DomainDict") -> List[Dict[Text, Any]]:
        
        required_slots = ["email1", "deadline"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]

class ApplyLeaveForm(Action):
    def name(self) -> Text:
            return "leave_form"

    async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: "DomainDict") -> List[Dict[Text, Any]]:
        
        required_slots = [ "leavedate"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]

class CancelMeetForm(Action):
    def name(self) -> Text:
            return "cancel_form"

    async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: "DomainDict") -> List[Dict[Text, Any]]:
        
        required_slots = [ "canceltime"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]

class AddMemberForm(Action):
    def name(self) -> Text:
        return "invite_form"

    async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: "DomainDict") -> List[Dict[Text, Any]]:
        
        required_slots = [ "invitetime","emailadd"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]

class ValidateInviteForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_invite_form"

    def validate_emailadd(self,slot_value: Any,dispatcher: CollectingDispatcher,tracker: Tracker,domain: "DomainDict") -> Dict[Text, Any]:
        attendees = tracker.get_slot('emailadd')
        a=[]
        if type(attendees) is str:
            a.append(attendees)
            return {'emailadd':a}
        else :
            return {'emailadd' : attendees}


    

class CancelMeeting(Action):
    def name(self) -> Text:
        return "action_cancel_meet"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        timing = tracker.get_slot('canceltime')
        status = delete_event(timing)
        if status == True:
            dispatcher.utter_message(" Meeting has been cancelled and attendees have been notified ")
            return [SlotSet('canceltime',None)]
        else:
            dispatcher.utter_message(" There is no meeting to cancel at the above mentioned time ")
            return [SlotSet('canceltime',None)]

class AddMembers(Action):
    def name(self) -> Text:
        return "action_add_member"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        timing = tracker.get_slot("invitetime")
        attendee = tracker.get_slot("emailadd")
        status = add_member(timing , attendee)
        if status == 0:
            dispatcher.utter_message(" The members have been invited to the meeting ")
        elif status == 1:
            dispatcher.utter_message(" There is no meeting during the above mentioned time ")
        elif status == 2:
            dispatcher.utter_message(" Not all the members you want to add to the meeting are free during the above mentioned time ")

class ApplyForLeave(Action):
    def name(self) -> Text:
        return "action_apply_leave"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        date = tracker.get_slot("leavedate")
        reason = tracker.latest_message['text']
        apply_leave(date, reason)
        dispatcher.utter_message("Your leave request has been sent. Currently Pending, waiting for approval.")
        return [SlotSet("leavedate", None)]
                 
