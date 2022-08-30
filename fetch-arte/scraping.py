import sys, os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def extract_infos(link):

    title = link.split('/')[-1]
    if len(title)==0:
        title = link.split('/')[-2]


    req = Request(link)
    html_page = urlopen(req)

    soup = BeautifulSoup(html_page, 'lxml')
    
    links = []
    for Link in soup.findAll('a'):
        l = Link.get('href')
        if (title in l) and ('RC-' not in l) and ('boutique' not in l):
            links.append(l)

    return title, links
    




if __name__=='__main__':
    
    link = sys.argv[-1]


    extract_infos(link)
