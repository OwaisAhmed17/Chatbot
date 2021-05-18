from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cal_auth import service_mail, manager

def send_mail(dates,reason):
    emailMsg = """Hello, 
I would like to request a paid leave on {0}. 
Reason : {1}.
Please approve my request. 
Regards """.format(dates,reason)
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = 'owaisahmed29@gmail.com'
    mimeMessage['subject'] = 'Leave Request'
    mimeMessage.attach(MIMEText(emailMsg,'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
    message = service_mail.users().messages().send(userId='me', body={'raw':raw_string}).execute()
    message = service_mail.users().messages().modify(userId='me', id=message['id'],body={"addLabelIds":["IMPORTANT"]}).execute()
    
def notify_task(email_msg , dates, recipient):
    mail = """The following task has been assigned to you :
{0}
The deadline for the above task is : {1}.""".format(email_msg , dates)
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = recipient
    mimeMessage['subject'] = 'Task Assignment'
    mimeMessage.attach(MIMEText(mail,'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
    message = service_mail.users().messages().send(userId='me', body={'raw':raw_string}).execute()
    message = service_mail.users().messages().modify(userId='me', id=message['id'],body={"addLabelIds":["IMPORTANT"]}).execute()
