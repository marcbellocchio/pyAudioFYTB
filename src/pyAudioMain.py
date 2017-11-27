'''
Created on 2 nov. 2017

@author: mbl
'''



from __future__             import absolute_import
from pytube                 import YouTube
from pyAudioInputList       import pyAudioInputList
from pyAudioTracking        import pyAudioTracking
from pyAudioSearch          import pyAudioSearch
from pyAudioDownloadVideo   import pyAudioDownloadVideo  
import argparse


import sys
# import getopt

class pyAudioMain(object):
    '''
    """pyAudioFromYoutube
    
    from a list of song to audio files on disk.
    The objective is to transform a shopping list of songs in text to a directory of audio files (mp3, ogg, ....) on disk.
    
    Usage: python kgp.py [options] [source]
    
    Options:
      -l ..., --list=...      use input list of song and singer
      -h, --help              show this help
    
    
    Examples:
      pyAudioMain.py      -l list.txt            
    
    """
    '''
    def __init__(self, params):
        '''
        Constructor
        '''
        # input list of song singer in text
        self.inputlistname      = None
        #  developer key to access to youtube api
        self.devkey             = None
        # tracking object
        self.pyAT               = None
        #search object
        self.pyAS               = None
        # object to get videos
        self.pyAV               = None 
        
        
        
 
    def SetInputListName(self, inlist): 
        self.inputlistname      = inlist
 
    def GetInputListName (self):
        return self.inputlistname

    def SetDevKey(self, inkey): 
        self.devkey             = inkey
      
    def GetDevKey(self): 
        return self.devkey
      
    def aaa(self):
        
        print ("testing .....")  
        # example from pytube github
        #yt = YouTube('https://www.youtube.com/watch?v=9bZkp7q19f0')
        # austin keen
        yt = YouTube('https://www.youtube.com/watch?v=J5pYqPSGpcQ')
        for stream in yt.streams.all():
            print(stream)
        print("continue")
        yt.streams.first().download()
        print("end")
        
    def Start(self):
        '''
        start the query based on the input list
        called from main
        '''
        self.pyAT = pyAudioTracking ()
        self.pyAL = pyAudioInputList (self.pyAT, self.GetInputListName())
        self.pyAS = pyAudioSearch(self.pyAT,self.GetDevKey())
        self.pyAS.BuildYoutubeObject()
        self.pyAV = pyAudioDownloadVideo(self.pyAT,None)
        #nbl = pyAL.GetNumberofLine()
        #print ("nb line is", nbl)
        if (self.pyAS.OpenInputList() == True):
            while self.pyAS.SingleSearch() != None:
                # set video id in video class
                self.pyAV.SetVideoId(self.pyAS.GetVideoId())
                # create URL
                self.pyAV.GetVideoUrl()
                # requet the video infos
            
            
            self.pyAS.CloseInputFile()
            
        else:
            print("cannot open inut file" + self.GetInputListName())
        pass
        

def main(argv):
    
    parser = argparse.ArgumentParser()
    # input list is a mandatory argument
    parser.add_argument("-l", "--inputlist",  required='True',
                        help="list of songs to search in text format")
    parser.add_argument("-k", "--devkey",  required='True',
                        help="google developer key to access to main api ")
    argus = parser.parse_args(argv)
    
    pyAM = pyAudioMain("starting")

    if argus.inputlist != '':
        #print ("the input list is : ",args.inputlist )
        # setting the list
        pyAM.SetInputListName(argus.inputlist)

    if argus.devkey != '':
        # set the key
        pyAM.SetKey(argus.devkey)
    
    # now it is time to try to do something ....
    pyAM.Start()



if __name__ == "__main__":
    main(sys.argv[1:])
