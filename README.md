# pyAudioFYTB
from a list of song to audio files on disk.
The objective is to transform a shopping list of songs (text format) to a directory of audio files (mp3 with title and album metadata) on disk.

# overall processing
1. read the input text file
2. for each line of the file, a youtube search is started to check if a video clip or simple audio is available, then get the link of the file
3. get file details
4. download the file on disk
5. extract audio and convert to mp3
6. delete temporary files (video, convertion data)
7. add to a playlist

# APIs world

## google API
searching using google api, you need a developper key, see https://developers.google.com/api-client-library/python/guide/aaa_apikeys
https://developers.google.com/youtube/v3/code_samples/python
https://developers.google.com/youtube/v3/code_samples/python#search_by_keyword

## pytube
https://github.com/nficano/pytube
pytube is a lightweight, dependency-free Python library (and command-line utility) for downloading YouTube Videos.
the starting point si to get a link to the video to use this code.
http://youtube.com/watch?v=9bZkp7q19f0



# Planning

- [x] start it
- [x] use python 3.x
- [x] overall objectives and specification
- [x] run on windows
- [x] use pytest
- [x] test pytube
- [x] test google api
- [x] manage python unit test
- [x] first python code extracts  mp4 files
- [x] run test using a list of 116 songs
- [x] filter extra characters in the input list for robustness
- [x] second python code extracts mp4 files and convert to mp3
- [x] test playlist type search to get id of the playlist and get all the videos links using playlist items
- [ ] update code to manage playlist and playlist items [branch + pull request]
- [ ] test using known playlists of 50, 100 items 
- [ ] test using bigger playlists
- [ ] wip
- [ ] run on linux
- [ ] run on mac OS
- [ ] dockers ?

# Install
- Windows
 
 google api
 pip install --upgrade google-api-python-client
 
 six 
 pip install --upgrade six
 
 progress bar
 pip install tqdm
 
 httplib2
 pip3 install httplib2 --upgrade

  wip

- Linux

  wip

- Mac OS

  wip


