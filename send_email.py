import smtplib, ssl
import os


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "yourmail@gmail.com"
    password = "here_goes_your_gmail_password"

    receiver = "yourmail@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
