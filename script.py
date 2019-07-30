import requests
import numpy as np
import pprint, os, sys
desktop = os.path.expanduser("~/Desktop")


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

    
class video:
    
        
    def __init__(self, ID, args):
        self.ID = ID
        
        req = requests.get(args.api_link+self.ID)
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
                 languages = ['VOF', 'VF', 'VOSTF'],
                 folder='/media/yann/DATA/Arte/',
                 chunk_size = 1024*1024):
        
        file_url = ''
        for l in languages:
            cond = (self.props['language']==l) & (self.props['quality']==quality)
            if np.sum(cond)>0:
                file_url = self.props['url'][cond][0]
                break

        # create response object 
        r = requests.get(file_url, stream = True)
        
        total_length = r.headers.get('content-length')
        # download started 
        with open(os.path.join(folder,
          self.props['reformated_title']+args.extension), 'wb') as f: 
                    
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
                    sys.stdout.write("\r[%s%s]\n" % ('=' * done, ' ' * (50-done)) )    
                    sys.stdout.flush()                
                    

def already_there(filename, folder):
    here = False
    for dd in os.walk(folder):
        if os.path.isfile(os.path.join(dd[0],filename)):
            here = True
            print('---> File already present in:', os.path.join(dd[0],filename))
    return here
    


def run_script(args):                    
    f = open(args.txt_file)
    IDS = []
    l = f.readline()
    while len(l)>10:
        IDS.append(l.split(args.root_link)[1][:12])
        l = f.readline()
    for link in IDS:
        print('\n*************************************************************')
        vid = video(link, args)
        if not already_there(vid.props['reformated_title']+\
                             args.extension,
                             args.dest_folder):
            try:
                vid.download(folder=args.dest_folder)
            except requests.exceptions.MissingSchema:
                print(vid.props['title'], 'not found with the API')


if __name__=='__main__':
    
    import argparse
    # First a nice documentation 
    parser=argparse.ArgumentParser(description=
     """ 
     Generating random sample of a given distributions and
     comparing it with its theoretical value
     """
    ,formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-f', "--txt_file",
                        help="filename of files with the ARTE links",
                        default=os.path.join(desktop, 'arte.txt'))
    parser.add_argument('-rl', "--root_link",
                        help="root of ARTE links", type=str,
                        default='https://www.arte.tv/fr/videos/')
    parser.add_argument('-al', "--api_link",
                        help="API link of ARTE videos", type=str,
                        default='https://api.arte.tv/api/player/v1/config/fr/')
    
    parser.add_argument('-df', "--dest_folder",
                        help="destination folder", type=str,
                        default='/media/yann/DATA/Arte/')
    parser.add_argument('-e', "--extension",
                        help="extension", type=str,
                        default='.mp4')
    args = parser.parse_args()
    run_script(args)
