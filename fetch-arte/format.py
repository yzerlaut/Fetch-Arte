import sys, os, argparse
from env import *

def inspect(args, debug=False):

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

    if ('VF-STF' in audio_id) or ('VOF-STF' in audio_id):
        with_subs = False # turn off if in french

    return video_id, audio_id, with_subs


if __name__=='__main__':

    parser=argparse.ArgumentParser()

    parser.add_argument("link", help="url", default='')

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
                        default=['VO-STF', 'VOF-STF', 'VF-STF'])

    args = parser.parse_args()

    if args.low_quality:
        args.quality = '384x216'

    link = sys.argv[-1]

    list_cmd = YT_DLP+' %s --list-formats > temp.txt' % link
    os.system(list_cmd)

    inspect(args, debug=True)

