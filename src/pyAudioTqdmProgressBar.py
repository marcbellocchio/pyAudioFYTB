'''
Created on 4 déc. 2017

@author: mbl
'''

from __future__             import absolute_import
from tqdm                   import tqdm

class pyAudioTqdmUpTo(tqdm):
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
        #self.clear()
        self.update(b * bsize - self.n)  # will also set self.n = b * bsize


