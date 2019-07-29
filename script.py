import requests
import numpy as np
import pprint, os, sys
from bs4 import BeautifulSoup


def reformat_props(data):

    props = {'title':data['VTI'],
             'duration':float(data['videoDurationSeconds']/60.),
             'language':[],
             'quality':[],
             'url':[]}
    if 'VDE' in data:
        props['summary'] = data['VDE']
    if 'V7T' in data:
        props['synopsis'] = data['V7T']
             
    for key in data['VSR']:
        props['language'].append(data['VSR'][key]['versionShortLibelle'])
        props['quality'].append(str(data['VSR'][key]['width'])+'x'+\
                                                    str(data['VSR'][key]['height']))    
        props['url'].append(data['VSR'][key]['url'])
    
    props['language'] = np.array(props['language'])
    props['quality'] = np.array(props['quality'])
    props['url'] = np.array(props['url'])
    
    if props['title'] == 'ARTE Reportage':
        props['title'] += ' '+data['subtitle']

    props['reformated_title'] = props['title'].replace('  ', '_').replace(' ','_').replace('/', '|')

    return props

    def reformat_title(title):
        return 

    
class video:
    
    global api_url
    api_url = 'https://api.arte.tv/api/player/v1/config/fr/'

        
    def __init__(self, ID):
        self.ID = ID
        
        req = requests.get(api_url+self.ID)
        if True:
            self.data = req.json()['videoJsonPlayer']
            self.props = reformat_props(self.data)
        else:
            self.props = {}
                    
    def show_props(self):
        pprint.pprint(self.props)
        
    def pick_quality_and_languages(self):
        self.quality = quality
        self.languages = languages
    
    def download(self,
                 quality = '640x360',
                 languages = ['VOF', 'VOSTF'],
                 folder='/media/yann/DATA/Arte/',
                 chunk_size = 1024*1024):
        
        file_url = ''
        for l in languages:
            cond = (self.props['language']==l) & (self.props['quality']==quality)
            if np.sum(cond)>0:
                file_url = self.props['url'][cond][0]
                break

        print(file_url)
        # create response object 
        r = requests.get(file_url, stream = True) 
          
        total_length = r.headers.get('content-length')

        # download started 
        with open(os.path.join(folder,self.props['reformated_title']+'.mp4'), 'wb') as f: 
                    
            print('%s (%.0f min)' % (self.props['title'],self.props['duration']))
            if total_length is None: # no content length header
                f.write(r.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in r.iter_content(chunk_size=chunk_size):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                    sys.stdout.flush()                
                    

                    
f = open('/home/yann/Desktop/arte.txt')
IDS = []
l = f.readline()
while len(l)>10:
    IDS.append(l.split('https://www.arte.tv/fr/videos/')[1][:12])
    l = f.readline()
    
for link in IDS:
    vid = video(link)
    try:
        vid.download()
    except requests.exceptions.MissingSchema:
        print(vid.props['title'], 'not found with the api')
