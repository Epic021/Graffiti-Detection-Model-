import requests
from datetime import datetime

from project_config import EXTDEF_SMS_APIKEY, EXTDEF_SMS_BODY, EXTDEF_SMS_TONUMBER


def send_trigger_sms():
    SMS_URL = "https://www.fast2sms.com/dev/bulkV2"
    SMS_APIKEY = EXTDEF_SMS_APIKEY
    SMS_MESSAGE = "T_" + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + " " + str(EXTDEF_SMS_BODY)

    payload = "sender_id=FSTSMS&message="+ SMS_MESSAGE +"&language=english&route=q&numbers=" + str(EXTDEF_SMS_TONUMBER)
    headers = {
    'authorization': SMS_APIKEY,
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    }

    smsResponse = requests.request("POST", SMS_URL, data=payload, headers=headers)

    if "SMS sent successfully." in smsResponse.text:
        print("SMS: Success")
    else:
        print("SMS: Failed")
