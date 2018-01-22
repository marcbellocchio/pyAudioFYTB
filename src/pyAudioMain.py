'''
Created on 2 nov. 2017 at home

@author: mbl
'''


from __future__             import absolute_import
from pyAudioInputList       import pyAudioInputList
from pyAudioTracking        import pyAudioTracking
from pyAudioSearch          import pyAudioSearch
from pyAudioVideos          import pyAudioVideos
from pyAudioConfig          import pyAudioConfig
from pyAudioCSV             import pyAudioCSV
from pyAudioFFmpeg          import pyAudioFFmpeg
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
      -l ..., --inputlist  use input list of song and singer
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
        # create tracking object
        self.pyAT               = pyAudioTracking ()
        #search object
        self.pyAS               = None
        # object to get videos
        self.pyAV               = None 
        # metadata, used as property
        self._metadata          = None
        # number of line in the input file
        self.nbline             = 0
        # current line number
        self.currentlinenb      = 0
        # video output dir
        self.videooutputdir     = None
        # audio output dir
        self.audiooutputdir     = None
        # name of the playlist
        self.playlist           = None
            # title for google api result
        self.title              = None
        
      
         
    def _SetMetaData(self, inMD): 
        self.metadata           = inMD
      
    def _GetMetadata(self): 
        return self.metadata             
 
    def SetInputListName(self, inlist): 
        self.inputlistname      = inlist
 
    def GetInputListName (self):
        return self.inputlistname

    def SetDevKey(self, inkey): 
        self.devkey             = inkey
      
    def GetDevKey(self): 
        return self.devkey
        
    def SetVideoOutputDir(self, inVideo): 
        self.videooutputdir     = inVideo
      
    def GetVideoOutputDir(self): 
        return self.videooutputdir    
     
    def SetAudioOutputDir(self, inAudio): 
        self.audiooutputdir    = inAudio
      
    def GetAudioOutputDir(self): 
        return self.audiooutputdir 
     
    def SetPlayList(self, inPlaylist): 
        self.playlist           = inPlaylist
      
    def GetPlayList(self): 
        return self.playlist 

     
     
    # definition of property for fun
    metadata = property (_GetMetadata,_SetMetaData )
        
    def ParseArgs(self, argus):
        '''
        get program arguments, call associated functions to store them
        '''     
        try:           
            if (argus.inputlist != None):
                # setting the list
                self.SetInputListName(argus.inputlist)
        
            if (argus.devkey != None)  :
                # set the key
                self.SetDevKey(argus.devkey)
                
            if (argus.videooutdir != None) :
                # set the key
                self.SetVideoOutputDir(argus.videooutdir)  
            else:
                self.SetVideoOutputDir(pyAudioConfig.outputvideodir) 
                
            if (argus.audiooutdir != None) :  
                self.SetAudioOutputDir(argus.audiooutdir) 
            else:
                self.SetAudioOutputDir(pyAudioConfig.outputaudiodir)   
                
            if (argus.playlist != None) :  
                self.SetPlayList(argus.playlist)  
            else:
                self.SetPlayList(pyAudioConfig.playlistname)

                
                           
        except:
            self.pyAT.SetError(self, sys._getframe().f_code.co_name, "wrong arguments" + str(argus) )
    
    def AddToCSV(self, query, link, outputfile ):
        
        try:
            CSVFile = pyAudioCSV()
            CSVFile.Open()
            CSVFile.AddQuery(query)
            CSVFile.AddLink(link)
            CSVFile.AddOutputFile(outputfile)
            CSVFile.Close()
        except:
            error = "cannot add to CSV: query: "+ query
            self.pyAT.SetError(self, sys._getframe().f_code.co_name, error  )
        
        
        
    def AddToPlayList(self):
        '''
        add the audio filename in the playlist
        '''
        try:
            plfile = open(self.GetAudioOutputDir() + "\\" + self.playlist, 'a')
        except IOError:
            self.pyAT.SetError(self, sys._getframe().f_code.co_name, "cannot open playlist:", self.playlist )
        finally:
            if plfile:
                plfile.write(self.pyAV.GetShortName() + "\r\n")
                plfile.close()

    def NormaliseAudio(self):
        '''
        detect audio level mean and max 
        max level shall be 0 db
        min level shall be close to -12 to -10 db
        '''
        pass

    def ExtractAudio(self):
        '''
        extract audio from a file
        '''
        sffmpeg = pyAudioFFmpeg(self.pyAT)
        sffmpeg.DetectOsPlatform()
        sffmpeg.SetInputFile(self.pyAV.GetFullDownloadName())
        sffmpeg.SetOutputFile(self.pyAV.GetFullDownloadName() + pyAudioConfig.extractfromffmpegext)
        if not self.pyAV.IsAudioFile():
            # extract audio with ffmpeg
            sffmpeg.CreateCommandExtractAudio()
            sffmpeg.RunExtractAudio()
            sffmpeg.SetInputFile(sffmpeg.GetOutputFile())
        
        # by default generate mp3 with metadata title album
        strtostrip = "." + pyAudioConfig.mp4extension
        sffmpeg.SetTitle(str(self.pyAV.GetShortName()).rstrip(strtostrip))
        sffmpeg.SetAlbumDesc(self.pyAS.GetVideoIdDesc())
        sffmpeg.SetAudioExtToStrip(self.pyAV.GetAudioExt())
        sffmpeg.CreateCommandMp4ToMp3()
        sffmpeg.RunConvertToMp3()
        # set the short name to be used in the playlist
        self.pyAV.SetShortName(sffmpeg.GetShortNameMp3())
                   
            
    def IncrementLineProgressBar(self):
            if(not self.pyAS.IsVideoIdBlank()): # when videoid is not available as the query has not been done, the increment is not done
                self.currentlinenb = self.currentlinenb + 1
                print("now processing line " , self.currentlinenb, " over ", self.nbline, "\n" )

              
    def Start(self):
        '''
        start the query based on the input list
        called from main, this is the core function of the program
        '''
        print("python program is starting ...")
        # object that manage input list
        self.pyAL = pyAudioInputList (self.pyAT, self.GetInputListName())
        # object that will handle the query using youtube api
        self.pyAS = pyAudioSearch(self.pyAT,self)
        # create the service object to initiate the youtube query
        self.pyAS.BuildYoutubeObject()
        # object that will get the video from one url
        self.pyAV = pyAudioVideos(self.pyAT,None)
        # processing each input line of the input list
        # prepare the progress bar to inform about the processed line
        #print("python program reading list ...")
        if (self.pyAS.OpenInputList() == True):
            # get the number of line in the input list
            self.nbline = self.pyAS.GetNumberofLine()
            self.currentlinenb = 0
            #print("python program single search ...")
            while self.pyAS.SingleSearch() != None:
                # progress bar
                self.IncrementLineProgressBar()
                # detect if video has been detected
                typeofquery = self.pyAS.GetQueryType()
                if (typeofquery == pyAudioConfig.youtubesearchvideo):
                    self.DownloadVideo()
                if(typeofquery == pyAudioConfig.youtubesearchplaylist):
                    self.DownloadPlaylist()
            self.pyAS.CloseInputFile()
            print("end of pyAudio Grabber, thank you for using!")
            
        else:
            print("cannot open input file" + self.GetInputListName())
        
    def DownloadVideo(self):  
        '''
        get the links to the file when video id is valid
        get audio
        update input playlist
        do nothing when video id is not valid
        '''
        # set video id in video class
        self.pyAV.SetVideoId(self.pyAS.GetVideoId())
        if (self.pyAV.IsVideoIdValid()):
            # get all possible links
            if (self.pyAV.SearchFinalLinks()):
                #create a name for the file stored on disk
                self.pyAV.SetFullDownloadName(self.GetAudioOutputDir(), self.pyAS.GetQuery())
                #download with progress bar
                self.pyAV.DownloadFromRealUrlWithProgressBar()
                # if the file is video and audio, start ffmpeg, extract audio 
                self.ExtractAudio()
                # add the short name to the playlist
                self.AddToPlayList()
                # CSV fr logging
                self.AddToCSV(self.pyAS.GetQuery(), self.pyAV.GetFinalLink(), self.pyAV.GetFullDownloadName())
            else:
                # final link not found shall be kept in tracking
                error = "cannot get final link for download, query is:" + self.pyAS.GetQuery()
                self.pyAT.SetError(self, sys._getframe().f_code.co_name, error )
                # CSV fr logging
                self.AddToCSV(self.pyAS.GetQuery(), "extended result" + "cannot get final link for download", "not downloaded")
        else:
            if(self.pyAS.IsVideoIdMissing() ): # if missing due to a query with empty result, store in trace
                warn = " >>> videoid is missing from query " + str(self.pyAS.GetQuery()) + str(self.pyAS.GetExtendedResult())
                self.pyAT.SetWarning(self, sys._getframe().f_code.co_name, warn)

    def DownloadPlaylist(self):
        '''
        from the playlist id get all the items and download all of them
        '''
        # from pyaudiosearch get the id of the playlist
        # start searching for all items in the playlist
        self.pyAS.PlayListItemsSearchQuery()
        listofresults   = self.pyAS.GetListOfResults()
        totalofitems    = int(self.pyAS.GetTotalResults())
        currentitem     = 0
        self.pyAV.SetVideoId(self.pyAS.GetVideoId())

        for swarmres in listofresults: # looping all list items
            for search_result in swarmres.get('items', []): # for one list item, parse the whole dict
                currentitem+=1
                print(" now collecting item n: ", currentitem, "over ", totalofitems , " items")
                self.pyAV.SetVideoIdValue(search_result['contentDetails']['videoId'])
                self.pyAV.SetVideoIdDesc(search_result['snippet']['description'])
                self.title          = search_result['snippet']['title']                     # used a main filename
                # get all possible links
                if (self.pyAV.SearchFinalLinks()):
                    #create a name for the file stored on disk
                    self.pyAV.SetFullDownloadName(self.GetAudioOutputDir(), self.title)
                    #download with progress bar
                    self.pyAV.DownloadFromRealUrlWithProgressBar()
                    # if the file is video and audio, start ffmpeg, extract audio 
                    self.ExtractAudio()
                    # add the short name to the playlist
                    self.AddToPlayList()
                    # CSV fr logging
                    self.AddToCSV(self.title , self.pyAV.GetFinalLink(), self.pyAV.GetFullDownloadName())
                else:
                    # final link not found shall be kept in tracking
                    self.pyAT.SetError(self, sys._getframe().f_code.co_name, "cannot get final link for download, title is:",self.title )
                    # CSV fr logging
                    self.AddToCSV(self.title, "extended result" + search_result, "not downloaded")
        
    
def main(argv):
    
    parser = argparse.ArgumentParser(description='list of song and singer to audio files')
    # input list is a mandatory argument
    parser.add_argument("-l", "--inputlist",  required='True',
                        help="list of songs to search in text format")
    parser.add_argument("-k", "--devkey",  required='True',
                        help="google developer key to access to main api ")
    parser.add_argument("-vo", "--videooutdir",  
                        help="outputdir for video")    
    parser.add_argument("-ao", "--audiooutdir",  
                        help="outputdir for audio")   
    parser.add_argument("-pl", "--playlist",  
                        help="name of the playlist to store links to audio files, it will be stored in the output dir of audio")     
    
    argus = parser.parse_args(argv)
    # creating main class
    pyAM = pyAudioMain("starting ....")
    # check input arguments
    pyAM.ParseArgs(argus)

        
    # now it is time to try to do something ....
    pyAM.Start()



if __name__ == "__main__":
    main(sys.argv[1:])
