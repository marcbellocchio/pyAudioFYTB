'''
Created on 12 nov. 2017

@author: mbl
'''

from __future__ import absolute_import
from pyAudioConfig import  pyAudioConfig
from googleapiclient.discovery  import build 
#from googleapiclient.errors     import HttpError
from pyAudioInputList import pyAudioInputList
#from pyAudioConfig import  pyAudioConfig
import sys
import json

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.

'''
*   Python 2.6 or greater

*   The pip package management tool

*   The Google APIs Client Library for Python:
    ```
    pip install --upgrade google-api-python-client
    ```
*   The google-auth, google-auth-oauthlib, and google-auth-httplib2 for user authorization.
    ```
    pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2
    ```
    ### Setting up your project and running code samples

1.  Create a project in the API Console and set up credentials for a web application. Set the authorized redirect URIs as appropriate.
2.  Save the client_secrets.json file associated with your credentials to a local file.
3.  Copy the full code sample to a local file in the same directory as the client_secrets.json file (or modify the sample to correctly identify that file's location.
4.  Run the sample from the command line and set command-line arguments as necessary:


https://developers.google.com/youtube/v3/sample_requests
https://developers.google.com/youtube/v3/code_samples/code_snippets
https://developers.google.com/apis-explorer/#p/youtube/v3/youtube.search.list?part=snippet&maxResults=25&q=surfing&type=video&_h=1&
'''


DEVELOPER_KEY = 'your own key'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

class pyAudioSearch(object):
    '''
    class to search for a video on youtube
    search is started using a line of text used as a query
    search in done on video only
    '''

    def __init__(self, trackingobject, pymain):
        '''
        Constructor
        create variables
        create youtube object
        store object pymain to get input parameters
        '''
        # object that will manage errors, infos
        self.tracking           = trackingobject
        # youtube search result of video id coded as dict
        self.ytsvideoidict      = dict([(pyAudioConfig.dictstatus, None), (pyAudioConfig.dictvideoid, None) , (pyAudioConfig.dictdescription, None)])
        # youtube search result of playlist id coded as dict
        self.ytsplaylistidict   = dict([(pyAudioConfig.dictstatus, None), (pyAudioConfig.dictplaylistid, None) , (pyAudioConfig.dictdescription, None)])
        # extended result stored the query result of video or playlist
        self.extendedresult     = None
        # input list object
        self.pyAL               = pyAudioInputList (self.tracking , pymain.GetInputListName())
        # youtube object to use api and lock for videos
        self.youtube            = None
        # store py main object created in main file
        self.pyMain             = pymain
        # query a line of text from the input file
        self.query              = None
        # type of the query
        self.querytype          = None
        # number of items collected in one api call
        self.resultperpage      = None
        # maximum number of results, shall be collected using several api calls
        self.totalresults       = None
        # list of extended results
        self.listofextresults   = list()
        
    def GetTotalResults(self):
        return self.totalresults

    def GetListOfResults(self):
        return self.listofextresults
    
    def IsVideoIdMissing(self):
        '''
        return true when the videoid is not valid as the result of the query is empty
        '''
        val = False
        if (self.GetVideoIdStatus() == pyAudioConfig.missingid):
            val = True
        return val
    
    def IsVideoIdBlank(self):
        '''
        return true when the videoid cannot be used due to a query not done
        '''
        val = False
        if (self.GetVideoIdStatus() == pyAudioConfig.missingidasblankquery):
            val = True
        return val
    
    def SetPlayListId(self, status, inId):
        self.ytsplaylistidict[pyAudioConfig.dictstatus]     = status
        self.ytsplaylistidict[pyAudioConfig.dictplaylistid] = inId
        
    def GetPlayListId(self):
        return self.ytsplaylistidict[pyAudioConfig.dictplaylistid]       

    def SetPlayListIdDesc(self, descrip):
        self.ytsplaylistidict[pyAudioConfig.dictdescription] = descrip
        
    def GetPlayListIdDesc(self):
        return self.ytsplaylistidict[pyAudioConfig.dictdescription]

    def GetVideoId(self):
        return self.ytsvideoidict  # return dict
    
    def SetVideoId(self, status, inId):
        
        self.ytsvideoidict[pyAudioConfig.dictstatus] = status
        self.ytsvideoidict[pyAudioConfig.dictvideoid] = inId
        
    def SetVideoIdDesc(self, descrip):
        self.ytsvideoidict[pyAudioConfig.dictdescription] = descrip
        
    def GetVideoIdDesc(self):
        return self.ytsvideoidict[pyAudioConfig.dictdescription]    
           
    def GetVideoIdStatus(self):
        return self.ytsvideoidict[pyAudioConfig.dictstatus]
           
    def SetExtendedResult(self, result): 
        '''
        used to reset the result or to initialise it
        ''' 
        self.extendedresult = result 
            
    def GetExtendedResult(self):  
        '''
        call it when it is necessary to be inform of the full result of the single search
        '''
        return self.extendedresult  
     
    def SetQueryType(self, intype):
        self.querytype  = intype
        
    def GetQueryType(self):
        return self.querytype
        
    def GetYouTube(self):
        return  self.youtube
    
    def GetQuery(self):
        return self.query
    
    def SetQuery(self, inquery):
        self.query = inquery
        
    def OpenInputList(self):
        '''
        return True when file is opened
        '''
        return self.pyAL.Open()
    
    def GetNumberofLine(self):
        return self.pyAL.GetNumberofLine()

    def CloseInputFile(self):
        self.pyAL.Close()  
        
    def BuildYoutubeObject(self):
        # youtube object to use api and lock for videos
        self.youtube        = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=self.pyMain.GetDevKey())         

    def SingleSearch(self):  
        '''
        The function will get a line from the input list by reading the input file
        then call the search api of youtube
        finally report the videoId collected from the api response
        return None when finished  
        return missingvideoidasblankquery when the collected line is empty
        '''
        self.SetVideoId(pyAudioConfig.noid, 0)
        self.SetPlayListId(pyAudioConfig.noid, 0)
        returnval           = None
        self.extendedresult = None
        self.SetQueryType(pyAudioConfig.undefined)
        # read a line of text from the input file
        self.SetQuery(self.pyAL.GetLine())
        #("single search query ", str(self.query))
        if ( (self.GetQuery() != None) and (self.GetQuery() != "")  ) :
            try:       
                returnval = True
                detectemptyline = str(self.GetQuery()).strip()        
                if( (detectemptyline != "\n") and  (detectemptyline != "") ):# no need to start searching
                    # here the detection of the search for a playlist:
                    if (detectemptyline.find(pyAudioConfig.playlisttag) >= 0):
                        # playlist detected, remove tag from the query
                        playlistquery   = detectemptyline.strip(pyAudioConfig.playlisttag)
                        if( (playlistquery != "\n") and  (playlistquery != "") ):
                            self.SetQuery(playlistquery)# save without the playlist code
                            self.PlaylistSearchQuery()
                            self.ExtractPlaylistId()
                        else:
                            # not a real query
                            self.SetPlayListId(pyAudioConfig.missingidasblankquery, 0)
                    else:# video query detected
                        self.VideoSearchQuery()
                        self.ExtractVideoId()
                else: # detected a line that is not a real query
                    self.SetVideoId(pyAudioConfig.missingidasblankquery, 0) # \n detected so videoID is missing for blank query
                    self.SetPlayListId(pyAudioConfig.missingidasblankquery, 0)
            except: 
                self.tracking.SetError(type(self).__name__, sys._getframe().f_code.co_name, "error while calling youtube search" )
            finally:
                return returnval # True to say that the end of the input list is not here
        else:
            return returnval   # at the end of the input list 
      

        
              
    def VideoSearchQuery(self):
        '''
        use youtube search api to collect information about a video identified by a text query
        '''
        self.SetQueryType(pyAudioConfig.youtubesearchvideo)
        self.SetExtendedResult(self.youtube.search().list(
            q=self.GetQuery(),                      # query contains the line of text words (song interpret for example)
            type=self.GetQueryType(),               # only video shall be collected
            part='id,snippet',                      # request both id and request object in the response
            key=self.pyMain.GetDevKey(),            # dev key 2500 query per day for free
            maxResults=1                            # single result as best hit at the beginning of the result
          ).execute() )
        
    def PlaylistSearchQuery(self):
        '''
        use youtube search api to collect information about a playlist identified by a text query
        '''  
        self.SetQueryType(pyAudioConfig.youtubesearchplaylist)
        #self.SetQuery(self.StripString(self.GetQuery())) # remove strange character in query
        self.SetExtendedResult(self.youtube.search().list(
            q=self.GetQuery(),                          # query contains the line of text words (song interpret for example)
            type=self.GetQueryType(),                   # only playlist shall be collected
            part='id,snippet',                          # request both id and request object in the response
            key=self.pyMain.GetDevKey(),                # dev key 2500 query per day for free
            maxResults=1                                # single result as best hit at the beginning of the result
          ).execute() )
                      
    def PlayListItemsSearchQuery(self):
        '''
        use playlistItems api to get all the items of a playlist identifier using GetPlayListId()
        '''
        self.SetExtendedResult(self.youtube.playlistItems().list(
            part='snippet,contentDetails',
            maxResults=50,
            playlistId = self.GetPlayListId()
          ).execute())
        # now if extendedresult contains data, they shall be parsed to collect the whole items
        # detect number of results
        getout = 0
        self.nextpagetoken = "empty"
        for mykey, value in self.GetExtendedResult().items():
            if mykey == 'pageInfo':
                self.resultperpage = value.get('resultsPerPage')
                self.totalresults  = value.get('totalResults')
                getout     +=1 
            # get token
            if mykey == 'nextPageToken':   
                self.nextpagetoken  = value
                getout     +=1 
            if getout == 2 :
                break
        
        self.listofextresults.append(self.GetExtendedResult())
        
        while (self.nextpagetoken != "empty"):
            self.SetExtendedResult(self.youtube.playlistItems().list(
            part='snippet,contentDetails',
            maxResults=50,
            playlistId = self.GetPlayListId(),
            pageToken = self.nextpagetoken
            ).execute())
          
            self.listofextresults.append(self.extendedresult)
            self.getout = 0
            self.nextpagetoken = "empty"
            for mykey, value in self.extendedresult.items():
                # get token
                if mykey == 'nextPageToken':   
                    self.nextpagetoken  = value
                    self.getout     +=1 
                if self.getout == 1 :
                    break
        
    def ExtractPlaylistId(self):

        if ((self.GetExtendedResult() != None) and (self.GetExtendedResult() != "") ):

            try:     
                self.SetPlayListId(pyAudioConfig.missingid, 0) # missing as the query result has not been parsed
                self.SetPlayListIdDesc("")
                # manage error in extended result, 
                for search_result in self.GetExtendedResult().get('items', []):
                    self.SetPlayListId(pyAudioConfig.validvideoId, search_result['id']['playlistId']) # get playlist id in the result
                    self.SetPlayListIdDesc(search_result['snippet']['description']) # description to be used for next call 
                    break                   
            except :
                error = "cannot get the id of the playlist from jsonobject: " + str(self.GetExtendedResult()) + "query is : " + str(self.GetQuery())
                self.tracking.SetError(type(self).__name__, sys._getframe().f_code.co_name, error  )
   

    def ExtractVideoId(self):
        '''
        extract videoid from extended result after a call to the youtube api
        https://github.com/youtube/api-samples/blob/master/python/search.py for parsing
        
         "items": [
              {
               "kind": "youtube#searchResult",
               "etag": "\"ld9biNPKjAjgjV7EZ4EKeEGrhao/pDl8RYaBDoe0zRXuTWl3ClFmMtk\"",
               "id": {
                "kind": "youtube#video",
                "videoId": "L3wKzyIN1yk"
               },
               https://docs.python.org/2/library/re.html#
               
               https://console.cloud.google.com/home/dashboard?project=musicsearchtofile&pli=1
        return the videoid from the extended result
        return missingvideoid when the response isempty and the videoid field is missing
        '''
        # extended result is a dict returned by youtube api
        if ((self.GetExtendedResult() != None) and (self.GetExtendedResult() != "") ):

            try:     
                self.SetVideoId(pyAudioConfig.missingid, 0) # missing as the query result has not been parsed
                self.SetVideoIdDesc("")
                # manage error in extended result, 
                for search_result in self.GetExtendedResult().get('items', []):
                    self.SetVideoId(pyAudioConfig.validvideoId, search_result['id']['videoId'])# videoid ok
                    self.SetVideoIdDesc(search_result['snippet']['description']) # description to be used as idtag for audio
                    break
            except :
                error = "cannot get the id of the video from jsonobject: " + str(self.GetExtendedResult()) + "query is : " + str(self.GetQuery())
                self.tracking.SetError(self, sys._getframe().f_code.co_name, error  )
