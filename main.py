from bs4 import BeautifulSoup
from requests import get
import sqlite3
from sys import argv
import datetime

today = datetime.date.today()
week_number = datetime.date(today.year, today.month, today.day).isocalendar().week

URL = 'https://www.olx.pl/d/nieruchomosci/mieszkania/sprzedaz/gliwice/'

con = sqlite3.connect("apartments.db")
cur = con.cursor()


if len(argv) > 1 and argv[1] == 'setup':
    cur.execute('''CREATE TABLE new_offers(date TEXT, description TEXT, price REAL, city TEXT, district TEXT, area REAL, price_per_metre REAL, week REAL, url TEXT)''')
    quit()


def parse_page(page_number):
    if page_number == 1:
        page = get(f'{URL}')
    else:
        page = get(f'{URL}?page={page_number}')
    bs = BeautifulSoup(page.content, 'html.parser')
    date = datetime.date.today()
    for offer in bs.findAll(type='list'):
        description = offer.findNext('h6').text.split('zł')[0].strip()
        price = offer.findNext('p').text.split('zł')[0].strip().replace(' ', '').replace(',', '.')
        offer_url = offer.find_parent('a', href=True)['href']
        if ('/d' in offer_url):
            offer_url = 'https://www.olx.pl' + offer_url
        try:
            location = offer.findAllNext('div')[0].findAllNext('p')[1]
            city = str(location.text).split(',')[0].split('-')[0].strip()
            district = str(location.text).split(',')[1].split('-')[0].strip()
        except IndexError:
            district = ""
        area_price = location.previous_element.findNext('div').text
        area = area_price.split('-')[0].split('m²')[0].strip().replace(' ', '').replace(',', '.')
        price_per_metre = area_price.split('-')[1].split('zł')[0].strip().replace(' ', '').replace(',', '.')
        apartment = (date, description, float(price), city, district, float(area), float(price_per_metre), week_number, offer_url)
        apartments.add(apartment)


apartments = set()

for i in range(1, 20):
    parse_page(i)

j = 1

for i in apartments:
    cur.execute('INSERT INTO new_offers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', i)
    con.commit()

con.close()