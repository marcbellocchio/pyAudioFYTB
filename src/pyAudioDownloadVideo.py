'''
Created on 24 nov. 2017

@author: bellocch
'''

from pyAudioConfig import  pyAudioConfig

class pyAudioDownloadVideo(object):
    '''
    classdocs
    '''
    def __init__(self, trackingobject, videoid):
        '''
        Constructor
        '''
        # object that will manage errors, infos
        self.tracking       = trackingobject
        self.videoid        = videoid
      
      
    def SetVideoId(self, vid):  
        self.videoid = vid
      
    def GetVideoUrl (self): 
        '''
        contruct the url to the video in youtube
        '''
        url = pyAudioConfig.youtubevideourl + self.videoid 
        return url
        