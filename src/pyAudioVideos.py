'''
Created on 24 nov. 2017

@author: bellocch
'''
#from __future__ import absolute_import
from pyAudioConfig                  import  pyAudioConfig

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
      
    def GetVideoUrl (self): 
        '''
        contruct the url to the video in youtube
        '''
        
        url = pyAudioConfig.youtubevideourl + self.videoid 
        return url
