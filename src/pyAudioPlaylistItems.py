'''
Created on 18 janv. 2018

@author: mbl
'''

from __future__             import absolute_import
from pyAudioSearch          import pyAudioSearch
from pyAudioTracking        import pyAudioTracking
from pyAudioVideos          import pyAudioVideos
from pyAudioConfig          import pyAudioConfig
from pytube                 import YouTube
import os
import urllib.request 

from pyAudioTqdmProgressBar         import pyAudioTqdmUpTo

class pyAudioPlaylistItems(pyAudioVideos):
    '''
    class inherit from video class
    objective is to get all items from a playlist from youtube and download audio from such playlist
    the playlist id must have been collected first in the search object
    '''

    def __init__(self, searchobject, trackingobject):
        '''
        Constructor
        '''
        # object that will manage errors, infos
        self.tracking           = trackingobject
        self.ytsvideoidict      = dict([(pyAudioConfig.dictstatus, pyAudioConfig.validvideoId), (pyAudioConfig.dictvideoid, None) , (pyAudioConfig.dictdescription, None)])
        #calling mother class constructor with a default dict
        pyAudioVideos.__init__(self, trackingobject, self.ytsvideoidict)
        self.pyAS               = searchobject
        self.extendedresult     = None
        self.resultperpage      = None
        self.totalresults       = None
        self.title              = None
        
        
        
    def DownloadAllItems(self):
        
        # start searching for all items in the playlist
        self.pyAS.PlayListItemsSearchQuery()
        listofresults = self.pyAS.GetListOfResults()
        
        for swarmres in listofresults:
            for search_result in swarmres.get('items', []):
                self.SetVideoIdValue(search_result['contentDetails']['videoId'])
                self.SetVideoIdDesc(search_result['contentDetails']['description'])
                self.title          = search_result['snippet']['title']  # used a main filename
                self

                # get all possible links
                if (self.SearchFinalLinks()):
                    #create a name for the file stored on disk
                    self.SetFullDownloadName(self.GetAudioOutputDir(), self.title)
                    #download with progress bar
                    self.DownloadFromRealUrlWithProgressBar()
                    # if the file is video and audio, start ffmpeg, extract audio 
                    self.ExtractAudio()
                    # add the short name to the playlist
                    self.AddToPlayList()
                    # CSV fr logging
                    self.AddToCSV(self.pyAS.GetQuery(), self.pyAV.GetFinalLink(), self.pyAV.GetFullDownloadName())
                else:
                    # final link not found shall be kept in tracking
                    self.pyAT.SetError(self, sys._getframe().f_code.co_name, "cannot get final link for download, query is:",self.pyAS.GetQuery() )
                    # CSV fr logging
                    self.AddToCSV(self.pyAS.GetQuery(), "extended result" + self.pyAS.GetExtendedResult(), "not downloaded")
            else:
                if(self.pyAS.IsVideoIdMissing() ): # if missing due to a query with empty result, store in trace
                    warn = " >>> videoid is missing from query " + str(self.pyAS.GetQuery()) + str(self.pyAS.GetExtendedResult())
                    self.pyAT.SetWarning(self, sys._getframe().f_code.co_name, warn)
                
            
        
   
        
        
        