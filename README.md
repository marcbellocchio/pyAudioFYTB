# pyAudioFYTB
from a list of song to audio files on disk.
The objective is to transform a shopping list of songs (text format) to a directory of audio files (mp3, ogg, ....) on disk.

# overall processing
1. read the input text file
2. for each line of the file, a youtube search is started to check if a video clip is available, then get the link of the video
3. get video file details
4. download the video on disk
5. extract audio
6. delete temporary files (video, convertion data)


# usefull python code

searching using google api, you need a developper key, see https://developers.google.com/api-client-library/python/guide/aaa_apikeys
https://developers.google.com/youtube/v3/code_samples/python
https://developers.google.com/youtube/v3/code_samples/python#search_by_keyword


https://github.com/nficano/pytube
pytube is a lightweight, dependency-free Python library (and command-line utility) for downloading YouTube Videos.
the starting point si to get a link to the video to use this code.
http://youtube.com/watch?v=9bZkp7q19f0


https://github.com/rg3/youtube-dl/blob/master/README.md#installation
youtube-dl is a command-line program to download videos from YouTube.com and a few more sites. It requires the Python interpreter, version 2.6, 2.7, or 3.2+, and it is not platform specific. It should work on your Unix box, on Windows or on Mac OS X. It is released to the public domain, which means you can modify it, redistribute it or use it however you like. 
It allows to download files and start ffmpeg to extract audio

# examples of code
https://stackoverflow.com/questions/26495953/youtube-dl-python-library-documentation


