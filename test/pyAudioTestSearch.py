'''
Created on 24 nov. 2017

@author: bellocch
'''
import unittest
from pyAudioSearch      import pyAudioSearch
from pyAudioTracking    import pyAudioTracking 
from pyAudioMain        import pyAudioMain
import json

class TestSearch(unittest.TestCase):



    jsondata = {
  "kind": "youtube#searchListResponse",
  "etag": "test",
  "nextPageToken": "CAEQAA",
  "regionCode": "CH",
  "pageInfo": {
    "totalResults": 1000000,
    "resultsPerPage": 1
  },
  "items": [
    {
      "kind": "youtube#searchResult",
      "etag": "test",
      "id": {
        "kind": "youtube#video",
        "videoId": "L3wKzyIN1yk"
      },
      "snippet": {
        "publishedAt": "2016-07-21T11:00:00.000Z",
        "channelId": "UCemsMvkKR1VDm5xtupQ9kyg",
        "title": "Rag'n'Bone Man - Human (Official Video)"
      }
    }
  ]
}
    


    def setUp(self):
        #
        print(" objective is to test the extraction of the videoID from an existing search response done online")


    def tearDown(self):
        pass


    def testname(self):
        jsonextendedresutl = json.dumps(TestSearch.jsondata)
        pyAT = pyAudioTracking ()
        pyAM = pyAudioMain("starting test")
        pyAM.SetInputListName("fake.txt") # pure virtual input file as will not be used
        pysearch = pyAudioSearch(pyAT, pyAM )
        pysearch.SetExtendedResult(jsonextendedresutl)
        pysearch.ExtractVideoId()
        print("videoId is:" + pysearch.GetVideoId() )
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()