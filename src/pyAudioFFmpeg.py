'''
Created on 26 déc. 2017

@author: mbl
'''
from __future__                     import  absolute_import
from pyAudioConfig                  import  pyAudioConfig
from pyAudioDetectOSPlatform        import  pyAudioDetectOSPlatform
import subprocess
from subprocess import DEVNULL
from subprocess import TimeoutExpired
import sys
import os

class pyAudioFFmpeg(object):
    '''
    wrapper of ffmpeg
    single command line
    allow to extract audio from the source file
    '''


    def __init__(self, trackingobject):
        '''
        Constructor
        '''
        # object that will manage errors, infos
        self.tracking                   = trackingobject
        self.inputfile                  = None
        self.outputfile                 = None   # output file when the audio is extracted from input file
        self.commandextractaudio        = None   # ffmpeg cmd to extract only audio from input file
        self.commandmp4tomp3            = None   # ffmpeg cmd to covert to mp3
        self.ffmpeg                     = None   # link to ffmpeg executable
        self.album                      = None   # description to add to metadata album
        self.audioexttostrip            = None   # after the youtube search the audio extension mp4, opus, is automatically added to the object video
        self.title                      = None   # title of the song
        self.shortnamemp3               = None


    def StripString(self, instr):
        '''
        remove strange character from input str
        used when collected title, description from youtube contains #, "" '``
        '''
        pass
        outstr = str(instr)
        outstr = outstr.replace('#',' ')
        outstr = outstr.replace('`',' ')
        outstr = outstr.replace('"',' ')
        outstr = outstr.replace('\'',' ')
        return outstr

    def GetShortNameMp3(self):
        return self.shortnamemp3

    def SetShortNameMp3(self, insn):
        self.shortnamemp3 = self.StripString(insn)

    def SetTitle(self, intitle):
        self.title = self.StripString(intitle)

    def GetTitle(self ):
        return self.title

    def SetAudioExtToStrip(self, inaudiodesc):
        self.audioexttostrip = self.StripString(inaudiodesc)


    def GetAudioExtToStrip(self):
        return self.audioexttostrip

    def SetAlbumDesc(self, inalbum):
        self.album = self.StripString(inalbum)
        if(len(self.album) > 70): #limit the string length to avoid strange artefact in audio player
            self.album = str(self.album[0:69])

    def GetAlbumDesc(self):
        return self.album

    def SetInputFile (self, inputf):
        self.inputfile     = inputf

    def GetInputFile(self):
        return self.inputfile

    def GetOutputFile(self):
        return self.outputfile

    def SetOutputFile (self, outf):
        self.outputfile  = outf


    def CreateCommandMp4ToMp3(self):
        '''
        generate the command with input and output parameters
        will be used by RUN
        to extract generate mp3 from input file
        ffmpeg -i input -id3v2_version 3 -c:a libmp3lame -b:a 128k -metadata title="..." -metadata album="from test ffmepg"  -y output
        remove initial audio extension from the output file to add only mp3
        self.ffmpeg is initialised by the function DetectOsPlatform
        '''
        stripstr = str(self.GetAudioExtToStrip() + pyAudioConfig.extractfromffmpegext)
        filenamemp3 = str(self.GetOutputFile()).strip(stripstr) + pyAudioConfig.mp3extension
        self.SetShortNameMp3(os.path.basename(filenamemp3)) # get only the tail of the path to store it in the playlist
        self.commandmp4tomp3     = self.ffmpeg + " -i " + "\"" + self.GetInputFile() + "\"" + " -id3v2_version 3 -c:a libmp3lame -b:a 128k -metadata title=" + "\""  + self.GetTitle()  + "\""  + " -metadata album=" + "\""  + self.GetAlbumDesc()  + "\""  + " -y " + "\"" + filenamemp3  + "\""


    def RunConvertToMp3(self):
        '''
        execute ffmpeg in a sub process
        command shall be created before
        any audio input to mp3 with metadata
        '''
        #print("starting ffmpeg to convert to mp3 :" + self.GetInputFile())
        handle = None
        try:
            handle = subprocess.Popen(self.commandmp4tomp3, stderr=DEVNULL, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            output = handle.communicate()[0] # get stdout data
            if handle.wait() != 0:
                print("warning calling ffmpeg using subprocess fails !, see tracking info", handle.communicate())
                infofile = "warning calling ffmpeg using subprocess fails ! status" + str(handle.communicate()) + "command :" + str(self.commandmp4tomp3 )
                self.tracking.SetInfo(self, sys._getframe().f_code.co_name, infofile )
        except (IOError, OSError, TimeoutExpired):
            handle.kill()
            self.tracking.SetError(self, sys._getframe().f_code.co_name, "exception while executing ffmpeg", output )
        finally:
            try:
                if (os.path.isfile(self.GetInputFile()) ):
                    os.remove(self.GetInputFile())
                else:    ## Show an error ##
                    errorfile = "cannot delete file after ffmpeg" + str(self.GetInputFile())
                    self.tracking.SetInfo(self, sys._getframe().f_code.co_name, errorfile )
            except :  ## if failed, report it back to the user ##
                errorfile = "exception cannot delete file after ffmpeg" + str(self.GetInputFile())
                self.tracking.SetError(self, sys._getframe().f_code.co_name, errorfile )


    def CreateCommandExtractAudio(self):
        '''
        generate the command with input and output parameters
        will be used by RUN
        to extract only audio
        ffmpeg -i inputfile (freshly downloaded) -vn -acodec copy output-audio.aac

        '''

        self.commandextractaudio = self.ffmpeg + " -i " + "\"" + self.GetInputFile() + "\"" + " -vn -acodec copy -y " + "\"" +  self.GetOutputFile() + "\""



    def RunExtractAudio(self):
        '''
        execute ffmpeg in a sub process
        command shall be created before
        '''
        print("starting ffmpeg to extract audio from :" + self.GetInputFile())
        handle = None
        try:
            handle = subprocess.Popen(self.commandextractaudio, stderr=DEVNULL, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            output = handle.communicate()[0] # get stdout data
            if handle.wait() != 0:
                print("warning calling ffmpeg using subprocess fails !, see tracking info", handle.communicate())
                infofile = "warning calling ffmpeg using subprocess fails ! status" + str(handle.communicate()) + "command :" + str(self.commandextractaudio )
                self.tracking.SetInfo(self, sys._getframe().f_code.co_name, infofile )
        except (IOError, OSError, TimeoutExpired):
            handle.kill()
            self.tracking.SetError(self, sys._getframe().f_code.co_name, "exception while executing ffmpeg", output )
        finally:
            try:
                if (os.path.isfile(self.GetInputFile()) ):
                    os.remove(self.GetInputFile())
                else:    ## Show an error ##
                    errorfile = "cannot delete file after ffmpeg" + str(self.GetInputFile())
                    self.tracking.SetInfo(self, sys._getframe().f_code.co_name, errorfile )
            except :  ## if failed, report it back to the user ##
                errorfile = "exception cannot delete file after ffmpeg" + str(self.GetInputFile())
                self.tracking.SetError(self, sys._getframe().f_code.co_name, errorfile )

    def DetectOsPlatform(self):
        '''
        based on os detection get the link to the configured ffmpeg sw
        '''
        # detect OS to get the right link to ffmpeg
        try:
            WhatOS = pyAudioDetectOSPlatform()
            WhatOS.Detect()
            if (WhatOS.IsWindows()):
                self.ffmpeg = pyAudioConfig.ffmpegexec_win
            if(WhatOS.IsLinux()):
                self.ffmpeg = pyAudioConfig.ffmpegexec_linux
            if(WhatOS.IsMac()):
                self.ffmpeg = pyAudioConfig.ffmpegexec_mac
        except:
                errorfile = "cannot detect the os platform for input file" + str(self.GetInputFile())
                self.tracking.SetError(self, sys._getframe().f_code.co_name, errorfile )



