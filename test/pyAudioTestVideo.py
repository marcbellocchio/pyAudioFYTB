'''
Created on 24 nov. 2017

@author: bellocch
'''
import unittest
from pyAudioInputList       import pyAudioInputList
from pyAudioTracking        import pyAudioTracking
from pyAudioSearch          import pyAudioSearch
from pyAudioDownloadVideo   import pyAudioDownloadVideo 
import json 

class TestVideo(unittest.TestCase):

    
    jsonextendedresutl = json.dumps({
         "kind": "youtube#searchListResponse",
         "etag": "\"ld9biNPKjAjgjV7EZ4EKeEGrhao/vKrrsJuQNkgevJdwSSgnG8ihbyQ\"",
         "nextPageToken": "CAEQAA",
         "regionCode": "CH",
         "pageInfo": {
          "totalResults": 1000000,
          "resultsPerPage": 1
         },
 "items": [
          {
           "kind": "youtube#searchResult",
           "etag": "\"ld9biNPKjAjgjV7EZ4EKeEGrhao/pDl8RYaBDoe0zRXuTWl3ClFmMtk\"",
           "id": {
            "kind": "youtube#video",
            "videoId": "L3wKzyIN1yk"
           },
           "snippet": {
            "publishedAt": "2016-07-21T11:00:00.000Z",
            "channelId": "UCemsMvkKR1VDm5xtupQ9kyg",
            "title": "Rag'n'Bone Man - Human (Official Video)",
            "description": "Taken from Rag'n'Bone Man's debut album 'Human', out now: http://smarturl.it/HumanDeluxe?IQid=yt Listen to the new single 'Grace (We All Try)' here: ...",
            "thumbnails": {
             "default": {
              "url": "https://i.ytimg.com/vi/L3wKzyIN1yk/default.jpg",
              "width": 120,
              "height": 90
             },
             "medium": {
              "url": "https://i.ytimg.com/vi/L3wKzyIN1yk/mqdefault.jpg",
              "width": 320,
              "height": 180
             },
             "high": {
              "url": "https://i.ytimg.com/vi/L3wKzyIN1yk/hqdefault.jpg",
              "width": 480,
              "height": 360
             }
            },
            "channelTitle": "RagnBoneManVEVO",
            "liveBroadcastContent": "none"
           }
          }
         ]
        }
)
    
    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        tracking = pyAudioTracking ()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()