import requests
from bs4 import BeautifulSoup
import re

URL = "https://www.epicgames.com/store/en-US/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
free_games = soup.find('h2', string='"Free Games"')
print(free_games)

#print(soup.prettify())
#print(soup)
#print(soup.find_all('h3'))
#available = soup.find_all('div', class_='css-1442lgn-CardGrid-styles__group')
#print(available[0])
#child = available[3].div.div.a
#print(child)
#x = available[0].find_all('a')
#print(x)
#print(len(available))
#print(available[0])
#available[0]

"""
for item in available[:-1]:
    try:
        print(item)
        print(item.find_parent().find_previous_sibling().text)
    except AttributeError as e:
        pass
        #print(e)
#print(available)
#h3s = soup.find_all('h3')
#print(h3s)
#ps = soup.find_all('p')
#print(ps)
#ps = soup.find_all('p', string=lambda text: "available" in text.lower())
#print(ps)
#print(soup)

#print(soup)
#results = soup.find(id='main-content-row')
#print(results)
#games = results.find("div", class_='entry-content')
#print(type(games))
"""