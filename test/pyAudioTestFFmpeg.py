'''
Created on 28 déc. 2017

@author: mbl
'''
import unittest
from pyAudioFFmpeg              import pyAudioFFmpeg
from pyAudioTracking        import pyAudioTracking


class Test(unittest.TestCase):
    '''
    
    test execution of ffmpeg on the local machine
    C:\\Users\\mbl\\develop\\pyAudioFYTB\\test\\nightwakesurfmarc.mp4
    C:\\Users\\mbl\\develop\\pyAudioFYTB\\test\\sound.mp4
    
    '''

    def testFFMPEG(self):
        mytracking = pyAudioTracking()
        myffmpeg = pyAudioFFmpeg(mytracking)
        myffmpeg.SetInputFile("C:\\Users\\mbl\\develop\\pyAudioFYTB\\test\\nightwakesurfmarc.mp4")
        myffmpeg.SetOutputFile("C:\\Users\\mbl\\develop\\pyAudioFYTB\\test\\sound.mp4")
        myffmpeg.CreateCommand()
        myffmpeg.Run()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testFFMPEG']
    unittest.main()