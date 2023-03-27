import sys, os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def title_from(link):

    title = link.split('/')[-1]
    if len(title)==0:
        title = link.split('/')[-2]

    return title

def extract_infos(link, debug=False):

    title = title_from(link)

    req = Request(link)
    html_page = urlopen(req)

    soup = BeautifulSoup(html_page, 'lxml')
    
    links = []
    for Link in soup.findAll('a'):
        l = Link.get('href')
        if debug:
            print(l)
        if (title in l) and ('RC-' not in l) and ('boutique' not in l):
            if 'arte' not in l:
                l = 'https://www.arte.tv'+l
            if debug:
                print('   -> selecting:', l)
            links.append(l)

    return title, links
    




if __name__=='__main__':
    
    link = sys.argv[-1]

    extract_infos(link)
