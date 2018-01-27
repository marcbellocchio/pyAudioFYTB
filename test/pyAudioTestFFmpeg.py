'''
Created on 28 déc. 2017

@author: mbl
'''
import unittest
from pyAudioFFmpeg              import pyAudioFFmpeg
from pyAudioTracking            import pyAudioTracking
import subprocess

import re


class Test(unittest.TestCase):
    '''
    
    test execution of ffmpeg on the local machine
    C:\\Users\\mbl\\develop\\pyAudioFYTB\\test\\nightwakesurfmarc.mp4
    C:\\Users\\mbl\\develop\\pyAudioFYTB\\test\\sound.mp4
    '''

    def testRunProcess(self):
        

        #test running process and collectting response
        
        

        #mycmd = "C:\\MBL_DATA\\wip\\ffmpeg-3.4.1-win64-static\\bin\\ffmpeg.exe -i \"C:\\MBL_DATA\\wip\\Simple Minds Love Song_.mp4 \" -af \"volumedetect\"  -f null -y pipe:1 "
        return 
        mycmd = "C:\\MBL_DATA\\wip\\ffmpeg-3.4.1-win64-static\\bin\\ffmpeg.exe -i \"C:\\MBL_DATA\\wip\\Simple Minds Love Song_.mp4 \" -af \"volumedetect\"  -f null  - "


        p = subprocess.Popen(mycmd ,stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        #p = subprocess.Popen(mycmd ,stdout=subprocess.PIPE, universal_newlines=True)
    
        stdout, stderr = p.communicate()
    
        if p.returncode == 0:
            strall = stdout + stderr
            print("stdout::" , stdout)
            print ("stderr::", stderr)
            print("all is ::", strall)
            
            getmaxvolume = re.findall(r"max_volume: ([\-\d\.]+) dB", strall)
            if getmaxvolume:
                value = float(getmaxvolume[0])
                print("max value is", value, "abs is :: ", abs (value))
                
            
            getminvolume = re.findall(r"mean_volume: ([\-\d\.]+) dB", strall)
            value = float(getminvolume[0])
            print("min value is", value, "abs is :: ", abs (value)) 
            
            print ("adjusting value is ", 0.0 - float(getmaxvolume[0]))

#max value is -4.5 abs is ::  4.5
#min value is -23.2 abs is ::  23.2
# value post processing     
#[Parsed_volumedetect_0 @ 000002670508dc20] mean_volume: -19.2 dB
#[Parsed_volumedetect_0 @ 000002670508dc20] max_volume: -0.5 dB

        else:
            print(" error launching ffmepg for subprocess")
    
    def testFFMPEG(self):
        #return
        mytracking = pyAudioTracking()
        myffmpeg = pyAudioFFmpeg(mytracking)
        myffmpeg.DetectOsPlatform()
        myffmpeg.SetFFmpegLink("C:\\MBL_DATA\\wip\\ffmpeg-3.4.1-win64-static\\bin\\ffmpeg.exe")
        myffmpeg.SetInputFile("C:\\MBL_DATA\\wip\\Simple Minds Love Song_.mp4 ")
        myffmpeg.SetOutputFile("C:\\MBL_DATA\\wip\\Simple Minds Love Song_normalize.mp4exffmpeg")
        myffmpeg.SetAudioExtToStrip("mp4")   
        myffmpeg.SetNormalizeOptions(" -f null nul") 
        myffmpeg.SetTitle("Simple Minds Love Song_normalize")
        myffmpeg.SetAlbumDesc("normalized")
        myffmpeg.CreateCommandMp4ToMp3()
        myffmpeg.RunConvertToMp3()
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testFFMPEG']
    unittest.main()