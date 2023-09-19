import sys, os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


def extract_infos(link, debug=False):

    title = link.split('/')[-2]
    # print(title)
    root_site = link[:31]
    # print(root_site)

    req = Request(link)
    html_page = urlopen(req)

    soup = BeautifulSoup(html_page, 'html.parser')
    
    links = []
    for Link in soup.findAll('a'):
        l = Link.get('href')
        print(l)
        if debug:
            print(l)
        if (title in l) and ('.html' in l):
            if 'francetv' not in l:
                l = 'https://www.francetv.fr'+l
            if debug:
                print('   -> selecting:', l)
            links.append(l)

    return title, links
    




if __name__=='__main__':
    
    link = sys.argv[-1]

    title, links = extract_infos(link)

    with open('list.txt', 'w') as f:
        for l in links:
            f.write(l+'\n')


