'''
Created on 12 nov. 2017

@author: mbl
'''
#from pyAudioTracking import pyAudioTracking
#from time import   strftime, localtime
import sys
import unicodedata 
import locale


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
            locale.getdefaultlocale()
            self.file = open(self.filename, 'rU')
        except IOError:
            self.tracking.SetError(self, sys._getframe().f_code.co_name, "cannot open input list" )
            ret = False
        return ret
    
    
    
    def GetLine(self):
        """
        read a line from the inpout file
        """
        retline = None
        outline = None
        try:
            retline= str(self.file.readline())
        except IOError:
            self.tracking.SetError(self, sys._getframe().f_code.co_name, "cannot read a line from"  )
        finally:  
            #outline1 = retline.replace("/","")
            #if( (retline !="") and (retline !="\n")) :
            outline = str(retline)
            return   outline.replace("+","")
            #return unicodedata.normalize('NFKD', outline).encode('ascii','ignore')
        
    def GetLinePostProcess(self):
        """
        read a line from the inpout file
        post process to remove non ascii character
        allow only a-zA-Z0-9._-
        not compliant character will be replaced by _
        """
        retline = None
        outline = None
        try:
            retline= str(self.file.readline())
        except IOError:
            self.tracking.SetError(self, sys._getframe().f_code.co_name, "cannot read a line from"  )
        finally:  
            #outline1 = retline.replace("/","")
            if( (retline !="") and (retline !="\n")) :
                outline = str("")
                az_range=range(97,123)
                AZ_range = range (65, 91)
                val_range = range (48,58)
                space_range = range (32, 33)
                for i in range(len(retline)):
                    value = ord(retline[i] )
                    if ( (value in az_range) or (value in AZ_range) or (value in val_range) or (value in space_range) ):
                        outline = "".join([outline,retline[i]])
                    else:
                        outline = "".join([outline,"_"])
                    '''
                    if( (retline[i] != "/") and (retline[i] != "&") and (retline[i] != "\\") and (retline[i] != "%") and (retline[i] != "#") and (retline[i] != "_") and (retline[i] != '"') and (retline[i] != "@") and (retline[i] != ":") and (retline[i] != "\n")):
                        #charac = str(retline[i].encode('ascii','ignore'))
                        if(ord(retline[i]) < 128):
                            outline = "".join([outline,retline[i]])
                    '''       
                        
                        
                        
                    
                #outline2 = outline1.replace("\\","")
                #outline = outline2.replace("@","")
                #outline = retline.replace("\\","_")
                #outline = retline.replace("@","_")
                #retline = retline.strip('\\')
            return   outline
            #return unicodedata.normalize('NFKD', outline).encode('ascii','ignore')
  

    def GetNumberofLine (self):
        '''
        number of real line with text
        '''
        nbline = 0
        try:
            while ( True):
                retline = self.GetLine()
                if ( (retline == None) or (retline == "")):
                    break
                realine = str(retline).strip()
                if(len(realine) > 5):
                #if( (retline !="") and (retline !="\n") and (retline !=" ")) :
                    nbline = nbline + 1
        except IOError:
            self.tracking.SetError(self, sys._getframe().f_code.co_name, "cannot read a line from" )
        finally:
            self.file.seek(0,0)          
            return nbline    

    def Close(self): 
        
        try:
            self.file.close()
        except IOError:
            self.tracking.SetError(self, sys._getframe().f_code.co_name, "cannot close file"  )
        finally:  
            pass    
         
        
        
        
            