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
        self.tracking           = trackingobject
        self.inputfile      = None
        self.outputfile     = None
        self.command        = None
        
    def SetInputFile (self, inputf):  
        self.inputfile     = inputf
        
    def GetInputFile(self):
        return self.inputfile
    
    def GetOutputFile(self):
        return self.outputfile
    
    def SetOutputFile (self, outf):
        self.outputfile  = outf
        
    def CreateCommand(self): 
        '''
        generate the command with input and output parameters
        will be used by RUN
        ffmpeg -i inputfile (freshly downloaded) -vn -acodec copy output-audio.aac
        '''
        # detect OS to get the right link to ffmpeg
        WhatOS = pyAudioDetectOSPlatform()
        WhatOS.Detect()
        if (WhatOS.IsWindows()):
            self.command = pyAudioConfig.ffmpegexec_win
        if(WhatOS.IsLinux()):
            self.command = pyAudioConfig.ffmpegexec_linux
        if(WhatOS.IsMac()):
            self.command = pyAudioConfig.ffmpegexec_mac          
        
        self.command = self.command + " -i " + "\"" + self.GetInputFile() + "\"" + " -vn -acodec copy -y " + "\"" +  self.GetOutputFile() + "\""
        
     
    def Run(self):
        '''
        execute ffmpeg in a sub process
        command shall be created before
        '''   
        print("starting ffmpeg to extract audio ......") 
        handle = None
        try:
            handle = subprocess.Popen(self.command, stderr=DEVNULL, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            output = handle.communicate()[0] # get stdout data
            if handle.wait() != 0:
                print("warning calling ffmpeg using subprocess fails !, see tracking info", handle.communicate())
                infofile = "warning calling ffmpeg using subprocess fails ! status" + str(handle.communicate()) + "command :" + str(self.command )
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


