import requests
import selectorlib
import time
import smtplib, ssl
import sqlite3

connection = sqlite3.connect('data.db')

URl = "http://programmer100.pythonanywhere.com/tours/"

def scrape(URl):
    response = requests.get(URl)
    text = response.text
    return text

def extract(text):
    extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
    value = extractor.extract(text)['tours']
    return value

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

def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()

def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date =  row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    rows = cursor.fetchall()
    print(rows)
    return rows


if __name__ == '__main__':
    while True:
        scraped = scrape(URl)
        extracted = extract(scraped)
        print(extracted)

        if extracted != 'No upcoming tours':
            row = read(extracted)
            if not row:
                store(extracted)
                send_email('Hey, new event found')
        time.sleep(2)
