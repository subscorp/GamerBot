import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from time import strptime

def get_free_games():
    games = []
    URL = "https://www.fanbyte.com/trending/epic-games-store-free-games-list/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    #print(soup.prettify())
    #print(soup)
    #print(soup.find_all('h3'))
    available = soup.find_all(string=re.compile("Available from"))
    first_month = available[0].split()[2:4][0]
    for item in available[:-1]:
        #print(item.find_parent().find_previous_sibling().text)
        #print(item)
        month, day = item.split()[2:4]
        #print(day)
        today = datetime.now().day
        try:
            if today == int(day) and month == first_month:
                game = item.find_parent().find_previous_sibling().text + '\n' + item
                games.append(game)
                print(game)
                print()
        except ValueError as e:
            print(e)

    return games