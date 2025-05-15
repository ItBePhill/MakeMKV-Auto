# MakeMKV_Auto - Phill
# use makemkv to rip a DVD or Blu-ray disc
# pop open the disc drive when ready for a disc / done

import configparser
import subprocess
import os
import string
import time
import open_tray
import tempfile

def Startup():
    global makemkv_cache_size, makemkv_min_length, makemkv_directio, makemkv_extra_options, makemkv_disc, makemkv_output, trayOpen, makemkv_info_args, makemkv_path, disc_check_interval
    configDefault = """[makemkv]
; Path to MakeMKV
; must be an absolute path and must end in \
makemkv_path = \\path\\to\\makemkv


; Path to the directory where the output files will be saved
; a new folder will be created at this path for each disc
; must be an absolute path and must end in \
makemkv_output = \\path\\to\\output


; size of read cache
makemkv_cache_size = 1024


; options "-r --decrypt and --noscan" are always used
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
open_tray = 1"""


    if not os.path.exists("config.ini"):
        with open("config.ini", 'w') as configfile:
            configfile.write(configDefault)
    #load config
    config = configparser.ConfigParser()
    config.read("config.ini")
    makemkv_path = config.get("makemkv", "makemkv_path")
    print(makemkv_path)
    makemkv_cache_size = config.get("makemkv", "makemkv_cache_size")
    makemkv_min_length = config.get("makemkv", "makemkv_min_length")
    makemkv_directio = config.get("makemkv", "makemkv_directio")
    makemkv_extra_options = config.get("makemkv", "makemkv_extra_options")
    makemkv_disc = config.get("makemkv", "makemkv_disc")
    makemkv_output = config.get("makemkv", "makemkv_output")
    trayOpen = config.getboolean("general", "open_tray")
    disc_check_interval = config.getfloat("general", "disc_check_interval")

def GetInfo(makemkv_path):
    makemkv_info_args = [
         f"{makemkv_path}\\makemkvcon64.exe",
         "info",
         f"disc:{makemkv_disc}", 
         "--robot",
        f"--minlength={makemkv_min_length}"
    ] 
    #create a temp file to write stdout to
    pipefile = tempfile.TemporaryFile()
    #not using subprocess.PIPE cos of limited size
    subpr = subprocess.Popen(args = makemkv_info_args, executable=f"{makemkv_path}\\makemkvcon64.exe", stdout=pipefile)
    #wait for process to finish
    subpr.wait()
    #go to start of file
    pipefile.seek(0)
    #read, decode and return the file
    return pipefile.read().decode("utf-8")


#loop and try to get the len of the drive if it is empty it will return nothing
def WaitForDisc(disc_check_interval, makemkv_disc):
    #bad but easy
    while True:
        try:
            print(os.listdir(f"{makemkv_disc}\\"))
            return
        except:
            time.sleep(disc_check_interval)
            continue
        

#run the makemkv command and start ripping the files
def Rip(makemkv_args, makemkv_path):
    subpr = subprocess.run(args = makemkv_args, executable=f"{makemkv_path}\\makemkvcon64.exe", shell=False)


def ReadyToRip():
    #get movie info for folder name
    out = GetInfo(makemkv_path)
    outlines = out.splitlines()
    with open("out.txt", "w+") as f:
        f.write(str(out))
    outSplit = outlines[1].split(",") 
    # Title   
    title = outSplit[5].replace('"', '')
    # Drive Letter
    letter =  outSplit[6].replace('"', '')
    print(title)
    print(letter)


    # Create the folder that the files will go in
    if (not os.path.exists(f"{makemkv_output}{title}")):
        os.makedirs(f"{makemkv_output}{title}")


    makemkv_args = [
        f"{makemkv_path}\\makemkvcon64.exe",
        "mkv",
        f"disc:{makemkv_disc}", 
        "all",
        "--decrypt", 
        f"--cache={makemkv_cache_size}", 
        f"--minlength={makemkv_min_length}", 
        "--noscan",  
        "--progress=-same",
        "--robot", 
        f"--directio={makemkv_directio}",
        f"{makemkv_output}{title}"
    ]

    Rip(makemkv_args, makemkv_path)
    return


def main():
    out = GetInfo(makemkv_path)
    outlines = out.splitlines()
    outSplit = outlines[1].split(",") 
    letter =  outSplit[6].replace('"', '')

    WaitForDisc(disc_check_interval, letter)
    ReadyToRip()
    if(trayOpen):
        open_tray.Run(letter)

    main()






Startup()
main()