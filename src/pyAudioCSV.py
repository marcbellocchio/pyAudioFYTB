'''
Created on 26 déc. 2017

@author: mbl
'''
from __future__                     import  absolute_import
import csv
from pyAudioConfig                  import pyAudioConfig
from csv import excel_tab

class pyAudioCSV(object):
    '''
    class to store information about each query
    query    link to video   output name
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.csv        = None
        self.fieldnames = ['query', 'videolink', 'outputname']
        self.writer     = None
        
    def Open(self):
        try:
            self.csv        = open(pyAudioConfig.csvlogfile, 'a', newline='')
            self.writer     = csv.DictWriter(self.csv,  fieldnames=self.fieldnames)
            self.writer.writeheader()
        except:
            print("exception in open from pyAudioCSV")
        finally:
            pass

        
    def Close(self):
        self.csv.close()
        
    def AddQuery(self, inQ):
        self.writer.writerow({'query': inQ })
        
    def AddLink(self, inLink):
        self.writer.writerow({'videolink': inLink })
        
    def AddOutputFile (self, inOut):
        self.writer.writerow({'outputname': inOut })