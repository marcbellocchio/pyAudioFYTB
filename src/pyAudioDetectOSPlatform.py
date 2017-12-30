'''
Created on 26 déc. 2017

@author: mbl
'''

from __future__             import absolute_import
import platform

class pyAudioDetectOSPlatform(object):
    '''
    classdocs
    https://docs.python.org/3/library/platform.html
    '''


    def __init__(self):
        '''
        Constructor
        example:
        https://github.com/easybuilders/easybuild/wiki/OS_flavor_name_version
        mac osx :::: system: Darwin, platform: Darwin-10.8.0-i386-64bit
        linux :::: system: Linux, platform: Linux-2.6.32-279.9.1.el6.x86_64-x86_64-with-centos-6.3-Final
        '''
        self.platformname   = None
        self.systemname     = None
        
    def Detect(self):  
        
        self.platformname   = platform.platform()
        self.systemname     = platform.system()
        self.maxinfo        = platform.uname()
        
        
    def IsWindows(self):
        ret = None
        try:  
            if(self.systemname.startswith("win") or self.systemname.startswith("Win")):
                ret = True
            else:
                ret = False
        except:
            pass
        finally:
            return ret    
            
        
    def IsLinux(self):
        ret = None
        try:  
            if(self.systemname.startswith("lin") or self.systemname.startswith("Lin")):
                ret = True
            else:
                ret = False
        except:
            pass
        finally:
            return ret    
                
    def IsMac(self): 
        
        ret = None
        try:  
            if(self.systemname.startswith("Darw") or self.systemname.startswith("darw")):
                ret = True
            else:
                ret = False
        except:
            pass
        finally:
            return ret    
        
        