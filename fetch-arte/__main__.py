import os, sys, pathlib
import requests
import numpy as np
import argparse, pprint

# custom modules
import yt_dlp
YT_DLP = 'python -m yt_dlp'

import scraping

def Download(args):

    if args.link!='':

        links = [args.link]

    elif os.path.isfile(args.txt_file):

        File = open(args.txt_file, 'r')
        links = [File.readline().replace('\n', '')]
        while links[-1]!='':
            links.append(File.readline().replace('\n', ''))
            if '# ' in links[-1]: # remove commented links
                links.remove(links[-1])

        links.remove('')
        File.close()

    else:
        print(' /!\ neither link nor text file provided /!\ ' )
        print('    ---> empty set of links')
        links = []

    for i, link in enumerate(links):

        print('\n Link %i ) *******************************************' % (i+1))
        print('    ', link)

        if 'RC-' in link:

            # means playlist
            title, playlist = scraping.extract_infos(link, debug=args.debug)
            pathlib.Path(title).mkdir(parents=True, exist_ok=True) # create folder

            for j, l in enumerate(playlist):
                # loop over episodes
                print('       - Episode #%i' % (j+1))
                dl_link(l,
                        filename=os.path.join(title, '%i.mp4' % (j+1)),
                        debug=args.debug)

        else:
            # single video download
            dl_link(link, 
                    filename=scraping.title_from(link)+'.mp4',
                    debug=args.debug)



def inspect_format(debug=False):

    Formats = open('temp.txt', 'r')
    video_id, audio_id, with_subs = '', '', True

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

    return video_id, audio_id, with_subs




def dl_link(link, filename='vid.mp4', 
            debug=False):

    list_cmd = YT_DLP+' %s --list-formats > temp.txt' % link 
    os.system(list_cmd)

    video_id, audio_id, with_subs = inspect_format(debug=args.debug)

    # video download
    video_cmd = YT_DLP+'%s -f "all[format_id=%s]" %s --output Video.mp4' %\
            (' --write-subs' if with_subs else '',
                    video_id, link)
    if debug:
        print(video_cmd)
    else:
        os.system(video_cmd)
    
    # audio download
    audio_cmd = YT_DLP+' -f "all[format_id=%s]" %s --output Audio.mp4' %\
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

    # add subtitles
    if with_subs:
        merge_cmd = 'ffmpeg -i Merged.mp4 -vf subtitles=Video.fr.vtt %s' % filename
        if debug:
            print(merge_cmd)
        else:
            os.system(merge_cmd)
    else:
        os.rename('Merged.mp4', filename)

    if not debug:
        cleanup()

def cleanup():
    for f in ['Video.mp4', 'Audio.mp4', 'Merged.mp4', 'Video.fr.vtt']:
        if os.path.isfile(f):
            os.remove(f)


        
if __name__=='__main__':
    
    parser=argparse.ArgumentParser(description=
     """ 
     Launch the download of Arte Videos
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
    parser.add_argument('-LQ', '--low_quality', action="store_true")

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
    
    parser.add_argument('--cleanup', action="store_true",
                        help="cleanup residual movie files")
    parser.add_argument('--debug', action="store_true",
                        help="prevent downloading")
    
    args = parser.parse_args()

    if args.low_quality:
        args.quality = '384x216'

    # check if destination folder exists
    if not os.path.isdir(args.dest_folder):
        print('** /!\ the destination directory %s was not found  /!\ **' % args.dest_folder )
        args.dest_folder = os.path.abspath(os.path.curdir)
        print('---> setting the destination directory to the current directory %s' % args.dest_folder)

    if args.cleanup:
        cleanup()
    else:
        Download(args)
