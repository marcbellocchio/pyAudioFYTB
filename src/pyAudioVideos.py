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


class FoundFinalLInk(Exception): pass
"""
foundone is an object to use in exception to exit from a nested loop
"""

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
        self.mainurl        = None
        self.finalink       = None
        self.audionly       = None
        self.downloadname   = None
        self.audioext       = None
      
    def SetAudioExt(self, ext):
        self.audioext = ext
        
    def GetAudioExt(self):      
        return self.audioext 
    
    def IsAudioFile(self):
        return self.audionly  
    
    def SetAudioOnly(self, Val):
        self.audionly = Val
 
    def SetFinalLink(self, flink):
        self.finalink = flink  
      
    def GetFinalLink(self):
        return self.finalink  
    
    def SetDownloadName(self, audiooutdir, query):
        
        name = query.replace('\r', '')
        name = name.replace('\n', '')
        self.downloadname = audiooutdir + "\\" + name + "." + self.GetAudioExt()
        
    def GetDownloadName(self):
        return self.downloadname
            
      
    def SetVideoId(self, Id):
        self.videoid     = Id
          
    def GetVideoUrl (self): 
        '''
        construct the url to the video in youtube
        '''
        self.mainurl = pyAudioConfig.youtubevideourl + self.videoid 
        return self.mainurl
    
    def SetVideoUrl (self, inurl): 
        '''
        construct the url to the video in youtube
        '''
        self.mainurl = inurl   
        
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
    
    def DownloadFromRealUrlWithProgressBar(self):
        '''
        finalink is to url to the video to download
        
        '''
        link = self.GetFinalLink()
        with pyAudioTqdmUpTo(unit='B', unit_scale=True, miniters=1,
                      desc=link.split('/')[-1]) as myprogressbar:  # all optional kwargs
            
            urllib.request.urlretrieve(link, filename=self.GetDownloadName(),
                               reporthook=myprogressbar.update_to, data=None)
        
    def SearchFinalLinks(self):
        '''
        from the main url, get all possible links, keep one to download the file
        the file is pure audio or video and audio
        return true when a link has been found
        '''
        self.SetAudioOnly(None)
        self.SetFinalLink(None)
        linkfound  = False
        try:
            yt = YouTube(self.GetVideoUrl() )
            #yt.streams.filter(progressive=True).all()
            
            # try to find first a link with audio only, self.type is audio, self.subtype = mp4
            for stream in yt.streams.filter(only_audio=True).all():
                #print(stream)
                if( (stream.abr !=None) and ( (stream.abr == "128kbps") or (stream.abr == "160kbps") or (stream.abr == "192kbps") ) ):
                    self.finalink   = stream.url
                    self.audionly   = True
                    self.audioext   = stream.subtype  
                    linkfound       = True
                    raise FoundFinalLInk("finalink")
               
            # try to get bigger file with both audio and video, audio will be extracted afterwards   
            for stream in yt.streams.filter(progressive=True).all():
                if( stream.audio_codec != None) :
                    self.finalink   = stream.url
                    self.audionly   = False
                    self.audioext   = stream.subtype 
                    linkfound       = True  
                    raise FoundFinalLInk("finalink")      
            '''
            for stream in yt.streams.all():
                print(stream)
                print(stream.url)
                print(stream.audio_codec)
                
            print("mp4 only ")
            for stream in yt.streams.filter(file_extension='mp4').all():
            print(stream)    
            
            ''' 
        except FoundFinalLInk :
                pass
                       
        finally:
            return linkfound    

        

        
