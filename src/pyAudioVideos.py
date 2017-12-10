'''
Created on 24 nov. 2017

@author: bellocch
'''
from __future__                     import absolute_import
from pyAudioConfig                  import  pyAudioConfig
from pytube                         import YouTube
import os
import urllib.request 

from pyAudioTqdmProgressBar         import pyAudioTqdmUpTo

#import sys

class pyAudioVideos(object):
    '''
    from a videoid, generates an url
    from url get the various video format
    select the video format with best quality audio
    dow,load the video
    ''' 


    def __init__(self, trackingobject, videoid):
        '''
        Constructor
        '''
        # object that will manage errors, infos
        self.tracking       = trackingobject
        self.videoid        = videoid
        self.url            = None
      
    def GetVideoUrl (self): 
        '''
        construct the url to the video in youtube
        '''
        
        self.url = pyAudioConfig.youtubevideourl + self.videoid 
        return self.url
    
    def SetVideoUrl (self, inurl): 
        '''
        construct the url to the video in youtube
        '''
        
        self.url = inurl   
        
    def AllLinkstoVideo(self):
        
        print ("all links from url")  
        # example from pytube github
        #yt = YouTube('https://www.youtube.com/watch?v=9bZkp7q19f0')
        # austin keen
        yt = YouTube(self.GetVideoUrl())
        for stream in yt.streams.all():
            print(stream)
        #print("now downloading")
        #yt.streams.first().download()
        print("end")    
    
    def DownloadFromRealUrlWithProgressBar(self, finalink):

        with pyAudioTqdmUpTo(unit='B', unit_scale=True, miniters=1,
                      desc=finalink.split('/')[-1]) as t:  # all optional kwargs
            
            urllib.request.urlretrieve(finalink, filename=os.devnull,
                               reporthook=t.update_to, data=None)
        
    
    
    def DownloadVideo(self):
        '''
        try to grab the video on the disk
        display the progress bar about the ongoing download
        '''
        yt = YouTube(self.GetVideoUrl() )
        #yt.streams.filter(progressive=True).all()
        for stream in yt.streams.all():
            print(stream)
        print("progressive only ")
        for stream in yt.streams.filter(progressive=True).order_by().all():
            print(stream)
            realurl = stream.url
            
        print("mp4 only ")

          
        print("now downloading")
        
        #yt.streams.first().download()
        print("end")
        
        
        
