import requests
import numpy as np
import pprint, os, sys
import argparse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def reformat_props(data):

    props = {'title':data['VTI'],
             'duration':float(data['videoDurationSeconds']/60.),
             'language':[],
             'quality':[],
             'mediaType':[],
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
        props['mediaType'].append(data['VSR'][key]['mediaType'])
    
    props['language'] = np.array(props['language'])
    props['quality'] = np.array(props['quality'])
    props['mediaType'] = np.array(props['mediaType'])
    props['url'] = np.array(props['url'])
    
    if props['title'] == 'ARTE Reportage':
        props['title'] = data['subtitle']+'_ARTE_Reportage'
    props['title'] = props['title'].replace('Xenius -', '')

    props['reformated_title'] = props['title'].replace('  ', '_').replace(' ','_').replace('/', '-').replace('‘', '-').replace('’', '-').replace('?', '').replace('ê', 'e').replace(':', '_')

    return props

class video:
        
    def __init__(self, ID, args,
                 folder='./',
                 subfolder=None,
                 filename=None):
        
        self.ID = ID
        self.file_url, self.file_location = '', ''
        
        req = requests.get(args.api_link+self.ID)
        self.data = req.json()['videoJsonPlayer']
        self.props = reformat_props(self.data)

        if subfolder in [None, '']:
            folder = folder
        else:
            secure_folder(subfolder, folder)
            folder = os.path.join(folder, subfolder)
            
        if filename in [None, '']:
            self.file_location = os.path.join(folder,
                                              self.props['reformated_title']+args.extension)
        else:
            self.file_location = os.path.join(folder,
                                              filename+args.extension)

    def show_props(self):
        pprint.pprint(self.props)
        
    def pick_quality_and_languages(self):
        self.quality = quality
        self.languages = languages
    
    def download(self,
                 quality = '640x360',
                 languages = ['VOF', 'VF', 'VOSTF'],
                 chunk_size = 512*512):
        
        for l in languages:
            cond = (self.props['language']==l) & (self.props['quality']==quality) & (self.props['mediaType']=='mp4')
            if np.sum(cond)>0:
                self.file_url = self.props['url'][cond][0]
                break

        # create response object 
        r = requests.get(self.file_url, stream = True)

        total_length = r.headers.get('content-length')
        # download started 
        with open(self.file_location, 'wb') as f: 
                    
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

    def check_success(self):
        try:
            statinfo = os.stat(self.file_location)
            if statinfo.st_size<1e4:
                print('/!\ Download as failed, visit:')
                print('----->  visit https://api.arte.tv/api/player/v1/config/fr/'+self.ID)
        except FileNotFoundError:
            pass
                    

def already_there(filename, args):
    here = False
    folders = args.archive_folder
    folders.append(args.dest_folder)
    for folder in folders:
        for dd in os.walk(folder):
            if os.path.isfile(os.path.join(dd[0],filename)):
                here = True
                print('---> File already present in:', os.path.join(dd[0],filename))
    return here
    
def secure_folder(folderstring, basefolder):

    full_folder = basefolder
    for f in folderstring.split('/'):
        full_folder = os.path.join(full_folder, f)
        if not os.path.isdir(full_folder):
            os.mkdir(full_folder)
    return full_folder
    

class Download:

    def __init__(self, args):

        self.File = open(args.txt_file, 'r')
        self.args = args
        self.IDS, self.SBFLDR, self.FNS = [], [], [] # Ids, Subfolders, Filenames

        self.run()

    def read_line_and_set_download_location(self):

        if len(self.linestring.split(';'))==3:
            # this means that : desired_name;desired_folder;url
            return self.linestring.split(';')
        elif len(self.linestring.split(';'))==2:
            # this means that : desired_folder;url
            return '', self.linestring.split(';')[0], self.linestring.split(';')[1]
        else: # we have just the link
            return '', '', self.linestring

    def extract_list_of_links(self, link):

        req = Request(link)
        html_page = urlopen(req)

        soup = BeautifulSoup(html_page, "lxml")

        links = []
        for Link in soup.findAll('a'):
            l = Link.get('href')
            if (link.split('/')[-2] in l) and ('RC-' not in l):
                links.append(l)
        return links

    def add_download_instructions(self, subfolder=None):
        self.IDS.append(self.link.split(self.args.root_link)[1][:12])
        if subfolder is None:
            self.SBFLDR.append(self.desired_subfolder)
        else:
            self.SBFLDR.append(subfolder)
        self.FNS.append(self.desired_name)
        
    def run(self):
        
        self.linestring = self.File.readline()
        while len(self.linestring)>0:
            if self.linestring[0]!='#': # not commented
                self.desired_name, self.desired_subfolder, self.link = self.read_line_and_set_download_location()
                if 'RC-' in self.linestring:
                    links = self.extract_list_of_links(self.link)
                    for self.linestring in links:
                        _, _, self.link = self.read_line_and_set_download_location()
                        subfolder = self.desired_subfolder
                        for i in range(1, 20):
                            if ('saison-%i'%i in self.link):
                                subfolder = os.path.join(self.desired_subfolder, 'saison-%i'%i)
                        self.add_download_instructions(subfolder=subfolder)
                else:
                    self.add_download_instructions()
            self.linestring = self.File.readline()

        for ii, link, subfolder, filename in zip(range(len(self.IDS)), self.IDS, self.SBFLDR, self.FNS):
            print('\n Link %s ) ***************************************************' % str(ii+1))
            vid = video(link, args,
                        folder=args.dest_folder,
                        subfolder=subfolder,
                        filename=filename)
            if not already_there(vid.props['reformated_title']+\
                                 args.extension, args):
                try:
                    vid.download(
                        quality = args.quality,
                        languages = args.prefered_languages)
                except requests.exceptions.MissingSchema:
                    print(' /!\ %s not found with the API /!\ ' % vid.props['title'])
            vid.check_success()
        
    def close(self):
        self.File.close()
        
    

        
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
                        # default='/media/yzerlaut/YANN/'
                        default='./')

    parser.add_argument('-af', "--archive_folder",
                        help="archive folder to check if the file is not already present",
                        type=str, nargs='*',
                        default=['/media/yzerlaut/YANN_EXT4/VDtheque/'])
    
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

    Download(args)
    # run_script(args)
