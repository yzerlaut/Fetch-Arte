from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

page = 'https://www.arte.tv/fr/videos/RC-020451/house-of-cards/'
page = 'https://www.arte.tv/fr/videos/RC-020753/baghdad-central/'
page = 'https://www.arte.tv/fr/videos/RC-020692/bron/'
req = Request(page)
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "lxml")

links = []
for link in soup.findAll('a'):
    l = link.get('href')
    if page.split('/')[-2] in l:
        links.append(l)
        print(l)

