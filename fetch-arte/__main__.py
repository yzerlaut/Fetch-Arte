import os, sys, pathlib
import requests
import numpy as np
import argparse, pprint
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

import yt_dlp
YTDLP = 'python -m yt_dlp'

def Download(args):

    if args.link!='':

        links = [args.link]

    elif os,path.isfile(args.txt_file):

        File = open(args.txt_file, 'r')
        links = [File.readline().replace('\n', '')]
        while links[-1]!='':
            links.append(File.readline().replace('\n', ''))
        links.remove('')
        File.close()

    else:
        print(' /!\ neither link nor text file provided /!\ ' )
        print('    ---> empty set of links')
        links = []

    for i, link in enumerate(links):
        print('\n Link %i ) ***************************************************' % (i+1))
        print('    ', link)
        dl_link(link)



def inspect_format(debug):

    Formats = open('temp.txt', 'r')
    video_id, audio_id = '', ''

    line = Formats.readline()

    language_index = 0 # ADD LOOP

    while line !='':
        # video
        if (args.quality in line) and (args.languages[language_index] in line):    
            video_id = line.split(' ')[0]
            if debug:
                print(video_id)
        # audio
        if (args.languages[language_index]+'-program_audio' in line):    
            audio_id = line.split(' ')[0]
            if debug:
                print(audio_id)
        line = Formats.readline()

    return video_id, audio_id



def dl_link(link, debug=False):

    list_cmd = YT_DLP+' %s --list-formats > temp.txt' % link 
    os.system(list_cmd)

    video_id, audio_id = inspect_format()

    # video download
    video_cmd = YT_DLP+' --write-subs -f "all[format_id=%s]" %s --output Video.mp4' %\
            (video_id, link)
    if debug:
        print(video_cmd)
    else:
        os.system(video_cmd)
    
    # audio download
    audio_cmd = YT_DLP+'-f "all[format_id=%s]" %s --output Audio.mp4' %\
            (audio_id, link)
    if debug:
        print(audio_cmd)
    else:
        os.system(audio_cmd)

    # merge with ffmpeg
    merge_cmd = 'ffmpeg -i Video.mp4 -i Audio.mp4 -c:v copy -c:a aac Merged.mp4'
    if debug:
        print(merge_cmd)
    else:
        os.system(merge_cmd)


# def reformat_props(data):


    # props = {'title':data['metadata']['title'],
             # 'duration':float(data['metadata']['duration']['seconds'])/60.,
             # 'description':data['metadata']['description'],
             # 'language':[], 'language_short':[],
             # 'url':[]}
    
             
    # for stream in data['streams']:
        # props['language'].append(stream['versions'][0]['shortLabel'])
        # props['url'].append(stream['url'])
    
    # props['language'] = np.array(props['language'])
    # props['url'] = np.array(props['url'])
    
    # if props['title'] == 'ARTE Reportage':
        # props['title'] = data['subtitle']+'_ARTE_Reportage'
    # props['title'] = props['title'].replace('Xenius -', '')

    # props['reformated_title'] = props['title'].replace('  ', '_').replace(' ','_').replace('/', '-').replace('‘', '-').replace('’', '-').replace('?', '').replace('ê', 'e').replace(':', '_')

    # return props

# class video:
        
    # def __init__(self, ID, args,
                 # folder='./',
                 # subfolder=None,
                 # filename=None):
        

        # self.ID = ID
        # self.file_url, self.file_location = '', ''
        # req = requests.get(self.ID)

        # if args.debug:
            # print('request output:')
            # pprint.pprint(req.json())

        # try:
            # self.data = req.json()['data']['attributes']
            # self.props = reformat_props(self.data)
            # self.props['original_link'] = ID
        # except BaseException as be:
            # # print(be)
            # print('')
            # print(' /!\ video metadata couldnt be extracted from the webpage  /!\ ')
            # print('')
            # self.props = {'original_link':ID,
                    # 'reformated_title':'test.mp4'}
        
        # if args.debug:
            # pprint.pprint(self.props)
        
        # if subfolder in [None, '']:
            # folder = folder
        # else:
            # secure_folder(subfolder, folder)
            # folder = os.path.join(folder, subfolder)
            
        # # if filename in [None, '']:
            # # self.file_location = os.path.join(folder,
                                              # # self.props['reformated_title']+args.extension)
        # # else:
            # # self.file_location = os.path.join(folder,
                                              # # filename+args.extension)

    # def show_props(self):
        # pprint.pprint(self.props)
        
    # def pick_url_based_on_language(self,
                                   # languages = ['VOSTF', 'VOF', 'VF']):

        # self.file_url = None

        # for l in languages:
            # # looking for the first match
            # cond = (self.props['language']==l)
            # if np.sum(cond)>0:
                # self.file_url = self.props['url'][cond][0]
                # break # the loop over language

    
    # def download(self,
                 # languages = ['VOSTF', 'VOF', 'VF'],
                 # quality='720p',
                 # chunk_size = 512*512):
       
        # # no just relying on yt-dlp
        # #sys.argv = ['', self.props['original_url'], 
        # #            '--output', '"%s"' % self.props['reformated_title']]
        # sys.argv = ['', self.props['original_url'], '--list-formats']
        # yt_dlp.main()

        # # self.pick_url_based_on_language(languages)
        # # cmd = 'ffmpeg -i %s -c copy -bsf:a aac_adtstoasc %s' % (self.file_url, self.file_location)
        # # print(cmd)
        # # os.system(cmd)
        # # if 'arteptwebvod' in self.file_url:
            # # os.system(cmd)
        # # else:
            # # print('video stream currently not supported')
        

    # def check_success(self):
        # try:
            # statinfo = os.stat(self.file_location)
            # if statinfo.st_size<1e4:
                # print('/!\ Download failed, visit:')
                # # print('----->  visit https://api.arte.tv/api/player/v1/config/fr/'+self.ID)
        # except FileNotFoundError:
            # pass
                    

# def already_there(filename, args):
    # here = False
    # folders = args.archive_folder
    # folders.append(args.dest_folder)
    # for folder in folders:
        # for dd in os.walk(folder):
            # if os.path.isfile(os.path.join(dd[0],filename)):
                # here = True
                # print('---> File already present in:', os.path.join(dd[0],filename))
    # return here
    
# def secure_folder(folderstring, basefolder):

    # full_folder = basefolder
    # for f in folderstring.split('/'):
        # full_folder = os.path.join(full_folder, f)
        # if not os.path.isdir(full_folder):
            # os.mkdir(full_folder)
    # return full_folder
    

# class Download:

    # def __init__(self, args):

        # self.args = args
        # self.IDS, self.SBFLDR, self.FNS = [], [], [] # Ids, Subfolders, Filenames

        # if args.link!='':
            # self.single_run(args)
        # else:
            # self.File = open(args.txt_file, 'r')
            # self.list_run()

    # def read_line_and_set_download_location(self):

        # if len(self.linestring.split(';'))==3:
            # # this means that : desired_name;desired_folder;url
            # return self.linestring.split(';')
        # elif len(self.linestring.split(';'))==2:
            # # this means that : desired_folder;url
            # return '', self.linestring.split(';')[0], self.linestring.split(';')[1]
        # elif '/RC-' in self.linestring:
            # folder = self.linestring.split('/')[-1]
            # if len(folder)==0:
                # folder = self.linestring.split('/')[-2]
            # # print(folder)
            # return '', folder, self.linestring
        # else: # we have just the link
            # return '', '', self.linestring

    # def extract_list_of_links(self, link):

        # req = Request(link)
        # html_page = urlopen(req)

        # soup = BeautifulSoup(html_page, 'lxml')
        # links = []
        # for Link in soup.findAll('a'):
            # l = Link.get('href')
            # if (link.split('/')[-2] in l) and ('RC-' not in l) and ('boutique' not in l):
                # links.append(l)

        # return links

    # def single_run(self, args,
                   # subfolder='', filename=None, ii=0):
        
        # print('\n Link %i ) ***************************************************' % (ii+1))
        # print('    ', args.link)

        # if '/RC-' in args.link:
            # links = self.extract_list_of_links(args.link)
            # pprint.pprint(links)
        # # else:

        # vid = video(args.link, args,
                    # folder=args.dest_folder,
                    # subfolder=subfolder,
                    # filename=filename)

        # vid.props['original_url'] = args.link
        # if args.debug:
            # print(' -- debug mode --   not downloading')
        # else:
            # vid.download()

    # def list_run(self):
        
        # self.linestring = self.File.readline()
        
        # while len(self.linestring)>1:

            # if self.linestring[0]!='#': # not commented
                # self.desired_name, self.desired_subfolder, self.link = self.read_line_and_set_download_location()
                # args.link = self.linestring
                # self.single_run(args)

            # self.linestring = self.File.readline()

        
    # def close(self):
        # self.File.close()
        
    

        
if __name__=='__main__':
    
    # First a nice documentation 
    parser=argparse.ArgumentParser(description=
     """ 
     Generating random sample of a given distributions and
     comparing it with its theoretical value
     """
    ,formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-l', "--link",
                        help="",
                        default='')

    parser.add_argument('-f', "--txt_file",
                        help="filename of files with the ARTE links",
                        default='arte.txt')

    parser.add_argument('-df', "--dest_folder",
                        help="destination folder", type=str,
                        default=os.path.join(os.path.expanduser('~'), 'Videos'))

    parser.add_argument('-af', "--archive_folder",
                        help="archive folder to check if the file is not already present",
                        type=str, nargs='*',
                        default=['/media/yzerlaut/YANN_EXT4/VDtheque/'])
    
    parser.add_argument('-q', "--quality",
                        help="""
                        quality of the videos in pixels, either:
                        384x216, 640x360, 768x432, 1280x720
                        """,
                        type=str, default='640x360')

    parser.add_argument("--languages",\
                        help="""
                        default language of the videos
                        in the order of preferences, 
                        e.g. for a french speaker prefering french only 
                        when original language was french otherwise vostfr,
                        pick: ['VO-STF', 'VF-STF']""", 
                        nargs='+',
                        type=str,
                        default=['VO-STF', 'VFSTF'])
    
    parser.add_argument('--debug', action="store_true",
                        help="prevent downloading")
    
    args = parser.parse_args()

    # check if destination folder exists
    if not os.path.isdir(args.dest_folder):
        print('** /!\ the destination directory %s was not found  /!\ **' % args.dest_folder )
        args.dest_folder = os.path.abspath(os.path.curdir)
        print('---> setting the destination directory to the current directory %s' % args.dest_folder)

    Download(args)
    
