#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup

# with open("insee_death.html", "r") as f:
#     insee_page = f.read()
insee_page = requests.get('https://www.data.gouv.fr/fr/datasets/fichier-des-personnes-decedees/').text
# print(insee_page)

root = BeautifulSoup(insee_page, 'lxml').html
for article in root.descendants:
    if article.name != 'article':
        continue
    filename = article.select("h4.ellipsis")[0].text
    if filename[-4:] != '.txt':
        continue
    print(filename)
    # print(article['id'])
    # print(article.select("div.resource-card-description")[0].text)
    url = article.select("a.btn-primary")[0]['href']
    print(url)
    data = requests.get(url).text
    with open(f'./data/{filename}', 'w') as f:
        f.write(data)
    print('')
