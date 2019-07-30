# Fetch Arte videos

*Download the videos in the `mp4` format from a list of links from the ARTE website*

## Requirements

1. a recent version of python (see https://www.python.org/downloads/ )

2. some python modules (installed with pip, see https://pip.pypa.io/en/stable/installing/):
- "requests" (install it from the shell with pip: `pip install requests`)
- "numpy" (install it from the shell with pip: `pip install numpy`)
- "argparse" (install it from the shell with pip: `pip install argparse`)

## Installation

Two options:

1. clone the repository with `git`: `git clone https://github.com/yzerlaut/Fetch-Arte.git`

2. download the code in the zip format here:
https://github.com/yzerlaut/Fetch-Arte/archive/master.zip
and unzip it where you want

## Build your "arte.txt" file:

Just copy-paste the links one by one from the Arte website (one per line).

Example of the "arte.txt" file content, see the file: https://github.com/yzerlaut/Fetch-Arte/blob/master/arte.txt

By default, you should just modify this file in the `Fetch-Arte` folder (remove the current links and put the one you want).

## Run the script

1. open the shell (command line interface)
2. navigate to the directory 
3. run the command:

`python script.py `

## Run the script with options

Let's say that instead of the default setting, you want that:
1. the `arte.txt` file considered is a file on the desktop
2. your destination folder is a usb drive located at `/media/yann/USB_STICK/`
3. the video is downloaded in the highest quality available, i.e.: 1280x720
4. the prefered language is german instead of french

you can run:
`python script.py --txt_file /home/yann/Desktop/arte.txt --dest_folder /media/yann/USB_STICK/ --quality 1280x720 --prefered_languages VOA VA VOSTA`

N.B. to deal with prefered languages, maybe one should use the different APIs, not the french one, to be discussed...

the different options can be seen by running:

`python script.py --help`

