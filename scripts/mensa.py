#!/usr/bin/python
# import libraries
import datetime
import urllib.request as request
import urllib.error
from bs4 import BeautifulSoup
import sys
from rich.console import Console
from rich.table import Table
import re

console = Console()
diff=0
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    diff=float(sys.argv[1])

# specify the url
date=datetime.datetime.now()+datetime.timedelta(days=diff)
quote_page = "https://www.studentenwerk-muenchen.de/mensa/speiseplan/speiseplan_" + date.strftime('%Y-%m-%d') + "_422_-de.html"
# query the website and return the html to the variable page

try:
    page = request.urlopen(quote_page)
except urllib.error.HTTPError as e:
    console.print(f"No menu for {date.strftime('%Y-%m-%d')} 🚫📆🍽️ ")
    console.print(f"\n[i]add number of days to get menu for other days[/i]")
    console.print(f"[i]e.g.[/i] mensa.py 1")
    sys.exit(1)
# parse the html using beautiful soup and store in variable soup
soup = BeautifulSoup(page, "html.parser")
# Take out the <div> of name and get its value
box = soup.find("div", attrs={"class": "c-schedule__item"})

datum=box.find("div", attrs={"class": "c-schedule__header"})
datum=datum.span.text.strip()

liste = box.find("ul", attrs={"class": "c-schedule__list"})
items=liste.find_all("li")

console.rule(datum, style="green")
table = Table(show_header=True, header_style="bold blue")
table.add_column("Art")
table.add_column(f"Gericht")

for item in items:
    artname=item.find("span", attrs={"class": "stwm-artname"}).text.strip()
    if artname == "Beilagen":
        table.add_section()
    if not artname:
        artname="\t"
    desc = item.find("p", attrs={"class": "js-schedule-dish-description"}).text
    desc = desc.replace("[Allergene]","").strip()
    desc = re.sub(r'\((.*?)\)', r'[green](\1)[/green]', desc)
    table.add_row(artname, desc)

console.print(table)