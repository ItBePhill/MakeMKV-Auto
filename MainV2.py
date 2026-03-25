import UIV2
import threading
import configparser
import os
import DiscInfo
import time
import open_tray
import subprocess
import datetime
import psutil
import os



def Run(disc):
    i = 0
    while True:
        if UIV2.header.running and i <= 100:
            UIV2.Update("Test", "Test Subtitle", f"Log: {i}", i, "100 MB", 100)
            i+=10
            time.sleep(1)
        else:
            UIV2.Cancel()
            return





def WaitForDisc():
    disc = None
    UIV2.header.ui.waiting = True
    if os.path.exists(f"{makemkv_config[0]}makemkvcon64"): path = f"{makemkv_config[0]}makemkvcon64"
    else: path = f"{makemkv_config[0]}makemkvcon"
    makemkv_info_args = [
         path,
         "info",
         f"disc:{makemkv_config[2]}", 
         "--robot",
        f"--minlength={makemkv_config[4]}"
    ] 
    dots = [".","..","..."]
    x = 0
    while disc == None:
        time.sleep(int(makemkv_config[9]))
        if x > 2:
            x = 0
        
        #this will continuosly run GetDisc, which will either return a disc or throw an error
        try:
            disc = DiscInfo.GetDisc(makemkv_info_args, makemkv_config)
            disc.letter = UIV2.cleanStr(disc.letter)
        except Exception as exc:
            if "Failed to Open Disc, is one inserted?" in exc.args:
                print("Couldn't Find Disc")
            else:
                UIV2.logMsg(exc.args)
            x+=1
            continue
            
        else:
            UIV2.logMsg(f"Preparing to rip: {disc.name}")
            UIV2.header.ui.waiting = False
            Run(disc)
            open_tray.Run(disc.letter)
            continue



def Start():
    global makemkv_config
    configDefault = r"""[makemkv]
    ; Path to MakeMKV
    ; must be an absolute path
    ;!! If you are on linux and have installed makemkv via the forum post !!
    ;!! Leave this blank as makemkvcon is on the PATH !!
    makemkv_path = \path\to\makemkv


    ; Path to the directory where the output files will be saved
    ; a new folder will be created at this path for each disc
    ; must be an absolute path
    makemkv_output = \path\to\output


    ; size of read cache
    makemkv_cache_size = 5000


    ; options "--robot --decrypt and --noscan" are always used
    makemkv_extra_options = ""




    ; the minimum amount of seconds long a video needs to be to get ripped
    ; 1 hours in seconds
    makemkv_min_length = 3600 


    ; the disc to rip from unless you are using multiple drives this will always be 0
    makemkv_disc = 0 

    ; whether to use direct disc access mode
    makemkv_directio = 1


    [general]
    ;whether the tray will be opened when it is done ripping
    open_tray = 1


    ; interval of when a disc will be checked in seconds
    disc_check_interval = 5

    ; Whether the log the output to a file
    log_to_file = 1

    """


    if not os.path.exists("config.ini"):
        with open("config.ini", 'w') as configfile:
            configfile.write(configDefault)
    #load config
    config = configparser.ConfigParser()
    config.read("config.ini")
    makemkv_path = config.get("makemkv", "makemkv_path")
    if(makemkv_path[-1] != "\\" and makemkv_path != "/"):
        makemkv_path += "\\"
    elif(makemkv_path == "/"):
        makemkv_path = ""
    makemkv_cache_size = config.get("makemkv", "makemkv_cache_size")
    makemkv_min_length = config.get("makemkv", "makemkv_min_length")
    makemkv_directio = config.get("makemkv", "makemkv_directio")
    makemkv_extra_options = config.get("makemkv", "makemkv_extra_options")
    makemkv_disc = config.get("makemkv", "makemkv_disc")
    makemkv_output = config.get("makemkv", "makemkv_output")
    trayOpen = config.getboolean("general", "open_tray")
    disc_check_interval = config.getfloat("general", "disc_check_interval")
    log_to_file = config.getfloat("general", "log_to_file")
    makemkv_config = [
        makemkv_path,           #0
        makemkv_output,         #1
        makemkv_disc,           #2
        makemkv_cache_size,     #3
        makemkv_min_length,     #4
        makemkv_directio,       #5
        makemkv_extra_options,  #6
        log_to_file,            #7
        trayOpen,               #8
        disc_check_interval,    #9
    ]
    
    #start the thread that will rip and provide the 
    UIV2.Init()
    thread = threading.Thread(name="WaitThread", target=WaitForDisc)
    thread.start()
    while True:
        UIV2._TkUpdate()

Start()