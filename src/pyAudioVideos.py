'''
Created on 24 nov. 2017

@author: bellocch
'''
from __future__                     import absolute_import
from pyAudioConfig                  import  pyAudioConfig
from pytube                         import YouTube
import urllib.request

from pyAudioTqdmProgressBar         import pyAudioTqdmUpTo

#import sys


class FoundFinalLInk(Exception): pass
"""
FoundFinalLInk is an object to use in exception to exit from a nested loop
"""

class pyAudioVideos(object):
    '''
    from a videoid, generates an youtube url
    from url get the various video and audio formats
    if no audio is available, select the video format with best quality audio
    download the audio or video object
    '''
    def __init__(self, trackingobject, videoiddict):
        '''
        Constructor
        '''
        # object that will manage errors, infos
        self.tracking           = trackingobject
        self.videoiddict        = videoiddict   # dict
        self.mainurl            = None          # url to google asset with videoId
        self.finalink           = None          # link to the selected object to download
        self.audionly           = None          # true when the object is a pure audio file, set while parsing youtube api response
        self.fulldownloadname   = None          # full name to store on disk (exotic characters have been removed to be posix compliant)
        self.audioext           = None          # file extension as collected from youtube api
        self.shortname          = None          # only the name of  the file without path information

    def GetShortName(self):
        return   self.shortname

    def SetShortName(self, insm):
        self.shortname = insm

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

    def SetFullDownloadName(self, audiooutdir, inquery):
        '''
        create a filename compatible with os
        remove non ascii character as defined in posix spec
        '''
        outline = str("")
        # define valid ascii range value for characters
        az_range=range(97,123)
        AZ_range = range (65, 91)
        val_range = range (48,58)
        space_range = range (32, 33)
        for i in range(len(inquery)):
            value = ord(inquery[i] )
            if ( (value in az_range) or (value in AZ_range) or (value in val_range) or (value in space_range) ):
                outline = "".join([outline,inquery[i]])
            else:
                outline = "".join([outline,"_"])

        # remove carriage return from input list
        self.shortname = outline.replace('\r', '')
        self.shortname = self.shortname.replace('\n', '')
        self.shortname = self.shortname + "." + self.GetAudioExt()
        #build the name of the file on disk
        self.fulldownloadname = audiooutdir + "\\" + self.shortname

    def GetFullDownloadName(self):
        return self.fulldownloadname

    def SetVideoIdValue(self, inval):
        self.videoiddict[pyAudioConfig.dictvideoid] = inval

    def SetVideoIdDesc(self, inval):
        self.videoiddict[pyAudioConfig.dictdescription] = inval

    def SetVideoId(self, dictvid):
        '''
        initialise the dictionary using the dict returned by the search class
        '''
        self.videoiddict     = dictvid  # dict

    def GetVideoIdStatus(self):
        return self.videoiddict[pyAudioConfig.dictstatus] # status only to determine if the main url can be generated

    def GetVideoIdValue(self):
        return self.videoiddict[pyAudioConfig.dictvideoid] # to generate the url to video

    def IsVideoIdValid(self):
        '''
        return true when the videoid value can be used to create a valid url
        '''
        val = False
        if (self.GetVideoIdStatus() == pyAudioConfig.validvideoId):
            val = True
        return val

    def GetVideoUrl (self):
        '''
        construct the url to the video in youtube
        '''
        self.mainurl = pyAudioConfig.youtubevideourl + self.GetVideoIdValue()
        return self.mainurl

    def SetVideoUrl (self, inurl):
        '''
        construct the url to the video in youtube
        '''
        self.mainurl = inurl

    '''
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
    '''
        
    def DownloadFromRealUrlWithProgressBar(self):
        '''
        the file identified by the final link will be downloaded
        a progress bar is displayed to inform about the running process

        '''
        link = self.GetFinalLink()
        #with pyAudioTqdmUpTo(unit='B', unit_scale=True, miniters=1, leave=False,
        #              desc=link.split('/')[-1]) as myprogressbar:  # all optional kwargs

        with pyAudioTqdmUpTo(unit='B', unit_scale=True, miniters=1, leave=False,
                      desc="downloading " + self.GetShortName()) as myprogressbar:  # all optional kwargs
            #print("download name",self.GetFullDownloadName())
            urllib.request.urlretrieve(link, filename=self.GetFullDownloadName(),
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
            #dict: {'status': 'fail', 'reason': 'Invalid parameters.', 'errorcode': '2'}


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




