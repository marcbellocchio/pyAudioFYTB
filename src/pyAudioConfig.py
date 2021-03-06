'''
Created on 6 sept. 2017

@author: bellocch

  class pyAudioConfig():
  
  to be updated with your local directory and executable

'''

class pyAudioConfig():

    # >>>> change me <<<<<<< 
    # openssl generic  
    ffmpegexec_win                      = "C:\\Users\\mbl\\develop\\pyAudioFYTB-0.1-alpha\\external\\ffmpeg-20171225-613f789-win64-static\\bin\\ffmpeg.exe"
    detectvolume_win                    = "-vn -sn -dn -f null nul"
    ffmpegexec_linux                    = "C:\\OpenSSL-Win32\\bin\\openssl.exe"
    detectvolume_linux                    = "-vn -sn -dn -f null /dev/null"
    ffmpegexec_mac                      = "C:\\OpenSSL-Win32\\bin\\openssl.exe"
    detectvolume_mac                    = "-vn -sn -dn -f null /dev/null"
    
    #outputdir                           = "C:\\Users\\mbl\\develop\\pyAudioFYTB\\tmp"
    outputvideodir                      = "C:\\Users\mbl\\develop\\pyAudioFYTB-0.1-alpha\\tmpv"
    outputaudiodir                      = "C:\\Users\mbl\\develop\\pyAudioFYTB-0.1-alpha\\tmpa"
    playlistname                        = "myplaylist.m3u8"
    logfile                             = "C:\\Users\\mbl\\develop\\pyAudioFYTB-0.1-alpha\\tmp\\log.txt"
    #logfile                             = "C:\\MBL_DATA\\dev\\python\\pyAudioFYTB\\tmp\\log.txt"
    # >>>> end of change me <<<<<<<
    
    #
    csvlogfile                          = "C:\\Users\mbl\\develop\\pyAudioFYTB-0.1-alpha\\tmpa\\csvlog.txt"
    
    # global settings
    undefined                           = "undefined"
    playlisttag                         = "#playlist#"          # magic tag to inform the tool that the query mention a playlist, all items shall be downloaded
    missingid                           = "missingafterquery"   # value for the key status, when a query has been done and the result is empty    
    missingidasblankquery               = "missingblank"        # value for the key status, when a query cannot be done as the input line is empty
    missingidaserror                    = "missinggooglerror"   # error from google api
    playlistquery                       = "playlistquery"       # magic word for playlist detected
    noid                                = "noquerysearch"       # start dictstatus value or when the end of the input file has been reached, 
    validvideoId                        = "ok"                  # value of dictstatus when the videoid value can be used in url
    dictvideoid                         = "videoId"             # key for the dict videoid, identifier
    dictplaylistid                      = "playlistId"          # key for the dict playlistid, identifier
    dictstatus                          = "status"              # key for the dict videoid, status
    dictdescription                     = "desc"                # key for the dict videoid, video description
    stringtrailingpadding               = 30
    youtubevideourl                     = "https://youtube.com/watch?v="
    youtubemaxresult                    = 1
    youtubesearchvideo                  = "video"
    youtubesearchplaylist               = "playlist"    
    youtubevideoIDkey                   = " 'items'][0]['id']['videoId' "
    mp3extension                        = "mp3"
    mp4extension                        = "mp4"
    extractfromffmpegext                = "exffmpeg"




    
