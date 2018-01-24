'''
Created on 7 janv. 2018

@author: mbl
'''
from __future__ import absolute_import
import unittest
from googleapiclient.discovery  import build 
#import google.oauth2.credentials
#from google_auth_oauthlib.flow import InstalledAppFlow
#from googleapiclient.errors     import HttpError
#from pyAudioConfig import  pyAudioConfig


# pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google.oauth2.credentials



# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains



# the OAuth 2.0 information for this application, including its client_id and

# client_secret. You can acquire an OAuth 2.0 client ID and client secret from

# the {{ Google Cloud Console }} at

# {{ https://cloud.google.com/console }}.

# Please ensure that you have enabled the YouTube Data API for your project.

# For more information about using OAuth2 to access the YouTube Data API, see:

#   https://developers.google.com/youtube/v3/guides/authentication

# For more information about the client_secrets.json file format, see:

#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets

CLIENT_SECRETS_FILE = 'client_secret_test.json'

# This OAuth 2.0 access scope allows for full read/write access to the

# authenticated user's account.

SCOPES = ['https://www.googleapis.com/auth/youtube']
DEVELOPER_KEY = 'AIzaSyCWyIFgr_3zzF5JRwEdoM-nPVvN20knEj8'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
QUERY = "Pop Music Playlist: Timeless Pop Hits (Updated Weekly 2018)"


class Test(unittest.TestCase):
    '''
    example 
    channel : https://www.youtube.com/user/andre0y0you/featured
    playlist Pop Music Playlist: Timeless Pop Hits (Updated Weekly 2018)
        https://www.youtube.com/playlist?list=PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj
        
        using search feature channel playlist or video can be collected
        when playlist is requested, type in search shall be playlist
            part='snippet',
            maxResults=1,
            q='pop music playlist Timeless Pop Hits (Updated Weekly 2018)',
            type='playlist')
        
        then the playlist id shall be collected from response
        "playlistId": "PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj"
        
        specific credential shall be created for authentication
        https://developers.google.com/youtube/registering_an_application
        
        example here
        https://github.com/youtube/api-samples/blob/master/python/playlist_localizations.py
        https://github.com/jay0lee/GAM/wiki/CreatingClientSecretsFile
        
        then to get a list of video : https://developers.google.com/youtube/v3/docs/playlistItems/list
            playlist_items_list_by_playlist_id(client,
            part='snippet,contentDetails',
            maxResults=50,
            playlistId='PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj')
            
            the response is limited to 50 assets
                "pageInfo": {
                "totalResults": 200,
                "resultsPerPage": 50
                
    https://developers.google.com/youtube/v3/quickstart/python
    https://developers.google.com/apis-explorer/#p/youtube/v3/youtube.playlistItems.list?part=snippet%252CcontentDetails&maxResults=25&playlistId=PLBCF2DAC6FFB574DE&_h=4&
    '''

    def testYoutubeChannel(self):
        # build youtube
        # youtube object to use api and lock for videos
        self.youtubesearch        = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)         

        # search for playlist
        self.extendedresult = None
        self.extendedresult = self.youtubesearch.search().list(
            q=QUERY,                    # query contains the line of text words (song interpret for example)
            type='playlist',            # only playlist shall be collected
            part='id,snippet',          # request both id and request object in the response
            key=DEVELOPER_KEY,         # dev key 2500 query per day for free
            maxResults=1                # single result as best hit at the beginning of the result
          ).execute()

               
        # parse extended result
        # get playlist ID
        for search_result in self.extendedresult.get('items', []):
            self.playlistid     = search_result['id']['playlistId'] # get playlist id in the result 
            self.description    = search_result['snippet']['description'] # description to be used as idtag for audio
            break
        print("playlist id", self.playlistid)
        print("description", self.description)

        # Authorize the request and store authorization credentials.
        '''
        self.flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        self.credentials = self.flow.run_console()
        self.youtubelist = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials = self.credentials)
        
        # get playlist items

        self.extendedresult = self.youtubelist.playlistItems().list(
            part='snippet,contentDetails',
            maxResults=50,
            playlistId = self.playlistid 
          ).execute()
 
        '''
        
                       
               
        self.extendedresult = self.youtubesearch.playlistItems().list(
            part='snippet,contentDetails',
            maxResults=50,
            playlistId = self.playlistid 
          ).execute()
        # detect number of results
        self.getout = 0
        for mykey, value in self.extendedresult.items():
            if mykey == 'pageInfo':
                self.resultperpage = value.get('resultsPerPage')
                self.totalresults  = value.get('totalResults')
                self.getout     +=1 
                
            
            # get token
            if mykey == 'nextPageToken':   
                self.nextpagetoken  = value
                self.getout     +=1 
            if self.getout == 2 :
                break
        
        self.mylist   = list()
        self.mylist.append(self.extendedresult)
        
        while (self.nextpagetoken != "empty"):
            self.extendedresult = self.youtubesearch.playlistItems().list(
            part='snippet,contentDetails',
            maxResults=50,
            playlistId = self.playlistid,
            pageToken = self.nextpagetoken
            ).execute()
          
            self.mylist.append(self.extendedresult)
            self.getout = 0
            self.nextpagetoken = "empty"
            for mykey, value in self.extendedresult.items():
                # get token
                if mykey == 'nextPageToken':   
                    self.nextpagetoken  = value
                    self.getout     +=1 
                if self.getout == 1 :
                    break
            
        
        '''
        # parse extended result
        for search_result in self.extendedresult.get('items', []):
            self.description    = search_result['snippet']['description'] # description to be used as idtag for audio
            self.title          = search_result['snippet']['title']  # used a main filename
            self.videoid        = search_result['contentDetails']['videoId']       
            print("videoid id", self.videoid)
            print("description", self.description)
            # download items here using videoID
        '''
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testYoutubeChannel']
    unittest.main()