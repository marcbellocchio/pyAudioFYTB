'''
Created on 12 nov. 2017

@author: mbl
'''
#from pyAudioTracking import pyAudioTracking
#from time import   strftime, localtime
import sys


class pyAudioInputList(object):
    '''
    open, parse, getline from text file
    '''


    def __init__(self, trackingobject, inputlist ):
        '''
        Constructor
        '''
        self.filename       = inputlist
        self.file           = None
        # object that will manage errors, infos
        self.tracking       = trackingobject

    def Open(self):
        '''
        return True when file is opened
        '''
        ret = True
        try:
            self.file = open(self.filename, 'r')
        except IOError:
            self.tracking.SetError(self, sys._getframe().f_code.co_name, "cannot open input list" + self.filename )
            ret = False
        return ret
    def GetLine(self):
        """
        read a line from the inpout file
        """
        retline = None
        try:
            retline= self.file.readline()
        except IOError:
            self.tracking.SetError(self, sys._getframe().f_code.co_name, "cannot read a line from" + self.filename )
        finally:  
            return   retline           

    def GetNumberofLine (self):
        nbline = 0
        try:
            while (self.GetLine()!= None):
                nbline = nbline + 1
        except IOError:
            self.tracking.SetError(self, sys._getframe().f_code.co_name, "cannot read a line from" + self.filename )
        finally:             
            return nbline    

    def Close(self): 
        
        try:
            self.file.close()
        except IOError:
            self.tracking.SetError(self, sys._getframe().f_code.co_name, "cannot close file" + self.filename )
        finally:  
            pass    
         
        
        
        
            