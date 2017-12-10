'''
Created on 7 sept. 2017

@author: bellocch
'''
from __future__ import absolute_import
#from time import gmtime, strftime
from pyAudioConfig import pyAudioConfig

import logging
#from subprocess import STDOUT, PIPE
#from OpensslConfig import OpensslConfig
#from OpensslTracking import OpensslTracking


class FoundOne(Exception): pass
"""
foundone is an object to use in exception to exit from a nested loop
"""


class pyAudioTracking(object):
    '''
    keep trace of processing
    '''
    session = pyAudioConfig.undefined
    def __init__(self):
        '''
        Constructor
        '''
        #self.session = "undefined"

        
        logging.basicConfig(level=logging.INFO,
                        filename=pyAudioConfig.logfile, filemode='a',
                        format='%(name)-28s %(levelname)-10s %(message)s')
          
    def GetLogger(self, classobject):
        self.loggername = '.'.join([classobject.__class__.__name__])
        return logging.getLogger(self.loggername)
        
    def GetTypeList (self):
        return    self.objecttype 
               
    def SetInfo(self, classobject, functionname, message):
        '''
        Info level, 
        class object to get the name of the class calling the log file,
        function name to identify the name of the function calling log
        message is the text 
        '''        
        self.logger = self.GetLogger(classobject)
        self.GetLogger(classobject).info(": "  + str(functionname).ljust(pyAudioConfig.stringtrailingpadding) + "\t\t" + message)
        
    def SetWarning(self, classobject, functionname, message):
        self.logger = self.GetLogger(classobject)
        self.GetLogger(classobject).warning(": "  + str(functionname).ljust(pyAudioConfig.stringtrailingpadding) + "\t\t" + message)
        
    def SetError(self, classobject, functionname, message):
        self.logger = self.GetLogger(classobject)
        self.GetLogger(classobject).error(": "  + str(functionname).ljust(pyAudioConfig.stringtrailingpadding) + "\t\t" +  message)
                    



        
                