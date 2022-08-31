import os, sys, pathlib
import numpy as np
import argparse, pprint

# yt_ldp command 
YT_DLP = 'python -m yt_dlp'
# ffmpeg command 
FFMPEG = 'ffmpeg'

import scraping

def Download(args):

    if args.link!='':

        links = [args.link]

    elif os.path.isfile(args.txt_file):

        File = open(args.txt_file, 'r')
        links = [File.readline().replace('\n', '')]

        while links[-1]!='':
            
            # remove commented links
            if '# ' in links[-1]:
                links.remove(links[-1])

            links.append(File.readline().replace('\n', ''))

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
            pathlib.Path(os.path.join(args.dest_folder, 
                         title)).mkdir(parents=True, exist_ok=True) # create folder

            season, ep = 0, 1

            for l in playlist:
                # loop over playlist element

                # checking if aranged by seasons
                is_sorted_by_season, previous_season_ep, season = False, season, 0
               
                while season<30 and not is_sorted_by_season:

                     # find out which season is it
                    if ('saison-%i-'%season) in l:
                        is_sorted_by_season = True
                        # is it a new season ?
                        if season!=previous_season_ep:
                            # reset episode number
                            ep = 1
                            # and create folder if not there
                            season_folder = os.path.join(args.dest_folder, title, 'saison-%i'%season)
                            pathlib.Path(season_folder).mkdir(parents=True, exist_ok=True) # create folder

                    season += 1
                season -=1 
                print(season)

                if is_sorted_by_season:

                    print('       - Season %i - Episode #%i' % (season, ep))
                    dl_link(l,
                            filename=os.path.join(season_folder, '%i.mp4' % ep),
                            debug=args.debug)

                else:

                    print('       - Episode #%i' % ep)
                    dl_link(l,
                            filename=os.path.join(args.dest_folder, title, '%i.mp4' % ep),
                            debug=args.debug)
                ep += 1
                
        else:
            # single video download
            dl_link(link, 
                    filename=os.path.join(args.dest_folder, scraping.title_from(link)+'.mp4'),
                    debug=args.debug)



def inspect_format(debug=False):

    video_id, audio_id, with_subs = '', '', True

    for language_index in range(len(args.languages)):

        Formats = open('temp.txt', 'r')
        line = Formats.readline()

        while line !='':

            # video
            if (args.quality in line) and (args.languages[language_index] in line):    
                video_id = line.split(' ')[0]
                if debug:
                    print('video ID:', video_id)
            # audio
            if (args.languages[language_index]+'-program_audio' in line):    
                audio_id = line.split(' ')[0]
                if debug:
                    print('audio ID:', audio_id)
            line = Formats.readline()

        if video_id!='' and audio_id!='':
            break

    if 'VF-STF' in audio_id:
        with_subs = False # turn off if in french

    return video_id, audio_id, with_subs




def dl_link(link, 
            filename='vid.mp4', 
            debug=False):

    list_cmd = YT_DLP+' %s --list-formats > temp.txt' % link 
    os.system(list_cmd)

    video_id, audio_id, with_subs = inspect_format(debug=args.debug)

    # video download
    video_cmd = YT_DLP+'%s -f "all[format_id=%s]" %s --output Video.mp4' %\
            (' --write-subs' if with_subs else '',
                    video_id, link)
    print('\n           --> downloading video')
    if debug:
        print(video_cmd)
    else:
        os.system(video_cmd)
    
    # audio download
    audio_cmd = YT_DLP+' -f "all[format_id=%s]" %s --output Audio.mp4' %\
            (audio_id, link)
    print('\n           --> downloading audio')
    if debug:
        print(audio_cmd)
    else:
        os.system(audio_cmd)

    # merge with ffmpeg
    merge_cmd = 'ffmpeg -i Video.mp4 -i Audio.mp4 -c:v copy -c:a copy Merged.mp4'
    print('\n           --> merging video and audio')
    if debug:
        print(merge_cmd)
    else:
        os.system(merge_cmd)

    # add subtitles
    if with_subs:
        print('\n           --> adding subtitles')
        merge_cmd = 'ffmpeg -i Merged.mp4 -vf subtitles=Video.fr.vtt -c:a copy %s' % filename
        if debug:
            print(merge_cmd)
        else:
            os.system(merge_cmd)
    elif not debug:
        os.rename('Merged.mp4', filename)

    if not debug and not args.no_cleanup:
        cleanup()

def cleanup():
    for f in ['Video.mp4', 'Audio.mp4', 'Merged.mp4', 'Video.fr.vtt', 'temp.txt']:
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
                        default=['VO-STF', 'VF-STF'])
    
    parser.add_argument('--cleanup', action="store_true",
                        help="do only the cleanup of residual movie files")
    parser.add_argument('-ncu', '--no_cleanup', action="store_true",
                        help="prevent cleanup of residual movie files")
    parser.add_argument('--debug', action="store_true",
                        help="prevent downloading")
    
    args = parser.parse_args()

    if args.low_quality:
        args.quality = '384x216'

    if not os.path.isdir(args.dest_folder):
        args.dest_folder = ''

    # check if destination folder exists
    if not os.path.isdir(args.dest_folder):
        print('** /!\ the destination directory %s was not found  /!\ **' % args.dest_folder )
        args.dest_folder = os.path.abspath(os.path.curdir)
        print('---> setting the destination directory to the current directory %s' % args.dest_folder)

    if args.cleanup:
        cleanup()
    else:
        Download(args)
