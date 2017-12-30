'''
Created on 26 déc. 2017

@author: mbl
'''

from __future__                 import absolute_import
from pyAudioDetectOSPlatform    import pyAudioDetectOSPlatform
import unittest



class Test(unittest.TestCase):


    def testUnderliningPlatform(self):
        print("starting  platform")
        myplatform = pyAudioDetectOSPlatform()
        myplatform.Detect()
        print("platform name" ,myplatform.platformname)
        print("system name" ,myplatform.systemname)
        myplatform.IsLinux()
        print ("is windows", myplatform.IsWindows())
        print ("full  infos", myplatform.maxinfo)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testUnderliningPlatform']
    unittest.main()