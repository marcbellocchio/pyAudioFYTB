'''
Created on 12 nov. 2017

@author: mbl
'''

from __future__ import absolute_import

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
        self.tracking       = trackingobject
        # youtube search result of video id
        self.ytsvideoid      = None
        # extended result stored the query result
        self.extendedresult = None
        # input list object
        self.pyAL           = pyAudioInputList (self.tracking , pymain.GetInputListName())
        # youtube object to use api and lock for videos
        self.youtube        = None
        # store py main object created in main file
        self.pyMain         = pymain
        # query a line of text from the input file
        self.query          = None
        
    def GetQuery(self):
        return self.query

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
        return missing when videoid cannot be collected
        '''
        self.ytsvideoid     = None
        self.extendedresult = None
        # read a line of text from the input file
        self.query = self.pyAL.GetLine()
        #("single search query ", str(self.query))
        if ( (self.query != None) and (self.query != "")  ) :
            try:       
                detectemptyline = str(self.query).strip()        
                if( (detectemptyline != "\n") and  (detectemptyline != "") ):# no need to start searching
                    self.extendedresult = self.youtube.search().list(
                        q=self.query,                    # query contains the line of text words (song interpret for example)
                        type='video',               # only video shall be collected
                        part='id,snippet',          # request both id and request object in the response
                        key=self.pyMain.GetDevKey(),# dev key 2500 query per day for free
                        maxResults=1                # single result as best hit at the beginning of the result
                      ).execute()
                    self.ExtractVideoId()
                else:
                    self.SetVideoId("missing blank") # \n detected so videoID is missing for blank
            except:
                self.tracking.SetError(self, sys._getframe().f_code.co_name, "error while calling youtube search" )
            finally:
                return self.ytsvideoid  
        else:
            print("end detected")
            print("query is " + self.query )
            return self.ytsvideoid 
              
    def GetVideoId(self):
        return self.ytsvideoid 
    
    def SetVideoId(self, inId):
        self.ytsvideoid = inId

    def ExtractVideoId(self):
        '''
        extract videoid from extended result
        https://github.com/youtube/api-samples/blob/master/python/search.py for parsing
        ...
         "items": [
              {
               "kind": "youtube#searchResult",
               "etag": "\"ld9biNPKjAjgjV7EZ4EKeEGrhao/pDl8RYaBDoe0zRXuTWl3ClFmMtk\"",
               "id": {
                "kind": "youtube#video",
                "videoId": "L3wKzyIN1yk"
               },
               
        ...
        '''
        
        
        # create json object
        if ((self.extendedresult != None) and (self.extendedresult != "") ):
            strfromdict = json.dumps(self.extendedresult)  # create the json using dumps as the results is a dict
            #print("strfromdict:", strfromdict)
            #print ("video id from dict", self.extendedresult.get('videoId'))
            jsonob = json.loads(strfromdict)
            #print("json object", jsonob)
            # shall find the key videoId in the json
            try:     
                self.ytsvideoid = "missing"
                for search_result in jsonob.get('items', []):
                    self.ytsvideoid = search_result['id']['videoId']
                    break
            except :
                error = "cannot get the id of the video from jsonobject: " + str(jsonob) + "query is : " + str(self.GetQuery())
                self.tracking.SetError(self, sys._getframe().f_code.co_name, error  )
            
            
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