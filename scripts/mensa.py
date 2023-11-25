#!/usr/bin/python
# import libraries
import datetime
import urllib.request as request
from bs4 import BeautifulSoup
import sys

diff=0
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    diff=float(sys.argv[1])

# specify the url
date=datetime.datetime.now()+datetime.timedelta(days=diff)
quote_page = "https://www.studentenwerk-muenchen.de/mensa/speiseplan/speiseplan_" + date.strftime('%Y-%m-%d') + "_422_-de.html"
# query the website and return the html to the variable page
page = request.urlopen(quote_page)
# parse the html using beautiful soup and store in variable soup
soup = BeautifulSoup(page, "html.parser")
# Take out the <div> of name and get its value
box = soup.find("div", attrs={"class": "c-schedule__item"})

datum=box.find("div", attrs={"class": "c-schedule__header"})
datum=datum.span.text.strip()

liste = box.find("ul", attrs={"class": "c-schedule__list"})
items=liste.find_all("li")
print(datum)
for item in items:
    artname=item.find("span", attrs={"class": "stwm-artname"}).text.strip()
    if artname == "Beilagen":
        print("\n"),
    if not artname:
        artname="\t"
    print(f'{artname}\t', end="")
    print(item.find("p", attrs={"class": "js-schedule-dish-description"}).text.strip())
