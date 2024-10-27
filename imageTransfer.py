import smtplib
import imghdr
from email.message import EmailMessage

from project_config import EXTDEF_EMAIL_TOADDR, EXTDEF_EMAIL_FROMADDR, EXTDEF_EMAIL_BODY, EXTDEF_EMAIL_SUBJECT, EXTDEF_EMAIL_GMAIL_KEY

def send_email_attach(img_name):
    newMessage = EmailMessage()
    newMessage['Subject'] = EXTDEF_EMAIL_SUBJECT
    newMessage['From'] = EXTDEF_EMAIL_FROMADDR
    newMessage['To'] = EXTDEF_EMAIL_TOADDR
    newMessage.set_content(EXTDEF_EMAIL_BODY)
    with open(img_name, 'rb') as f:
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name = f.name
    newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EXTDEF_EMAIL_FROMADDR, EXTDEF_EMAIL_GMAIL_KEY)
        smtp.send_message(newMessage)