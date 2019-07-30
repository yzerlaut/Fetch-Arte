import requests
import numpy as np
import pprint, os, sys
import argparse

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

    props['reformated_title'] = props['title'].replace('  ', '_').replace(' ','_').replace('/', '-')

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
                 folder='./',
                 chunk_size = 512*512):
        
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
                    
            print('Downloading: %s (%.0f min)' % (self.props['title'],self.props['duration']))
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
        print('')
                    

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
    for ii, link in enumerate(IDS):
        print('\n Link %s ) ***************************************************' % str(ii+1))
        vid = video(link, args)
        if not already_there(vid.props['reformated_title']+\
                             args.extension,
                             args.dest_folder):
            try:
                vid.download(
                    quality = args.quality,
                    languages = args.prefered_languages,
                    folder=args.dest_folder)
            except requests.exceptions.MissingSchema:
                print(' /!\ %s not found with the API /!\ ' % vid.props['title'])


if __name__=='__main__':
    
    # First a nice documentation 
    parser=argparse.ArgumentParser(description=
     """ 
     Generating random sample of a given distributions and
     comparing it with its theoretical value
     """
    ,formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-f', "--txt_file",
                        help="filename of files with the ARTE links",
                        default='arte.txt')

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

    parser.add_argument('-q', "--quality",
    help="""
    quality of the videos in pixels, either:
    384x216, 640x360, 720x406, 1280x720
    """,
                        type=str, default='640x360')

    parser.add_argument('-pl', "--prefered_languages",\
    help="""
    default language of the videos
    in the order of preferences, 
    e.g. for a french speaker prefering french only when original language was french,
    pick: ['VOF', 'VF', 'VOSTF']""", nargs='+',
                        type=str,
                        default=['VOF', 'VF', 'VOSTF'])
    
    args = parser.parse_args()

    # check if destination folder exists
    if not os.path.isdir(args.dest_folder):
        print('** /!\ the destination directory %s was not found  /!\ **' % args.dest_folder )
        args.dest_folder = os.path.abspath(os.path.curdir)
        print('---> setting the destination directory to the current directory %s' % args.dest_folder)
        
    run_script(args)
