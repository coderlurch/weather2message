import os
from twilio.rest import Client
import smtplib

TWILIO_ACOOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')
MY_EMAIL = os.environ.get('MY_EMAIL')
MY_EMAIL_PW = os.environ.get('MY_EMAIL_PW')


def send_message(text, number):
    client = Client(TWILIO_ACOOUNT_SID, TWILIO_AUTH_TOKEN)

    try:
        message = client.api.account.messages.create(
            from_=TWILIO_NUMBER,
            to=number,
            body=text)
    except Exception as e:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL,
                             password=MY_EMAIL_PW)
            msg = f"Subject: Twilio message failed to {number} \n\n " \
                  f"exception: {e}" \
                  "message text: \n\n" + text
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=MY_EMAIL,
                                msg=msg.encode("utf8"))
    else:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL,
                             password=MY_EMAIL_PW)
            msg = f"Subject: Twilio message sent to {number} \n\n " \
                  f"date created: {message.date_created} \n\n" \
                  f"message status: {message.status} \n\n" \
                  "message text: \n\n" + text
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=MY_EMAIL,
                                msg=msg.encode("utf8"))