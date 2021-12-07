import os
import smtplib

MY_EMAIL = os.environ.get('MY_EMAIL')
MY_EMAIL_PW = os.environ.get('MY_EMAIL_PW')


def send_message(subject, text, email):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL,
                         password=MY_EMAIL_PW)
        msg = f"Subject: {subject} \n\n" \
              + text
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=email,
                            msg=msg.encode("utf-8"))
