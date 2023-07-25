import requests
import selectorlib

URl = "http://programmer100.pythonanywhere.com/tours/"

def scrape(URl):
    response = requests.get(URl)
    text = response.text
    return text

def extract(text):
    extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
    value = extractor.extract(text)['tours']
    return value

def send_email():
    print('Email was Sent!')

def store(extracted):
    with open('data.txt', 'a') as file:
        file.write(extracted + '\n')

def read(extracted):
    with open('data.txt', 'r') as file:
        return file.read()

if __name__ == '__main__':
    scraped = scrape(URl)
    extracted = extract(scraped)
    content = read(extracted)
    print(extracted)
    if extracted != 'No upcoming tours':
        if extracted not in content:
            store(extracted)
            send_email()

