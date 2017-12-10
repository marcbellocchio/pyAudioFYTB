'''
Created on 2 déc. 2017

@author: mbl
'''
import unittest
import time, sys
import os
import urllib.request 
from tqdm import tqdm

class TqdmUpTo(tqdm):
    """Provides `update_to(n)` which uses `tqdm.update(delta_n)`."""
    def update_to(self, b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)  # will also set self.n = b * bsize




class Test(unittest.TestCase):


    def testProgressBarAscii(self):
        print ("Loading simple progress bar ascii")
        for i in range(0, 100):
            #time.sleep(0.1)
            width = int((i + 1) / 4)
            bar = "[" + "#" * width + " " * (25 - width) + "]"
            sys.stdout.write(u"\u001b[1000D" +  bar)
            sys.stdout.flush()
        print()

    def testtdqm(self):
        
        eg_link = "https://github.com/marcbellocchio/pyAudioFYTB/archive/master.zip"
        print("testing tdqm ....")
        with TqdmUpTo(unit='B', unit_scale=True, miniters=1,
                      desc=eg_link.split('/')[-1]) as t:  # all optional kwargs
            
            urllib.request.urlretrieve(eg_link, filename=os.devnull,
                               reporthook=t.update_to, data=None)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testProgressBarAscii']
    unittest.main()
