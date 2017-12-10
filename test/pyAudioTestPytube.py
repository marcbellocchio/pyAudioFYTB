'''
Created on 2 déc. 2017

@author: mbl
'''
from __future__             import absolute_import
from pytube                 import YouTube



import unittest


class Test(unittest.TestCase):


    def testPytube(self):
        print ("testing pytube, try downloading austin keen.....")  
        # example from pytube github
        #yt = YouTube('https://www.youtube.com/watch?v=9bZkp7q19f0')
        # austin keen
        yt = YouTube('https://www.youtube.com/watch?v=J5pYqPSGpcQ')
        #yt.streams.filter(progressive=True).all()
        for stream in yt.streams.all():
            print(stream)
        print("progressive only ")
        for stream in yt.streams.filter(progressive=True).all():
            print(stream)
        print("mp4 only ")
        for stream in yt.streams.filter(file_extension='mp4').order_by('resolution').all():
            print(stream)
          
        print("now downloading")
        
        #yt.streams.first().download()
        print("end")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testPytube']
    unittest.main()