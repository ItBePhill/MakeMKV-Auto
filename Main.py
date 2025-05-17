# MakeMKV_Auto - Phill
# use makemkv to rip a DVD or Blu-ray disc
# pop open the disc drive when ready for a disc / done

import configparser
import subprocess
import os
import time
import open_tray
import tempfile
import sys
import io
from StringProgressBar import progressBar
def Startup():
    global makemkv_cache_size, makemkv_min_length, makemkv_directio, makemkv_extra_options, makemkv_disc, makemkv_output, trayOpen, makemkv_info_args, makemkv_path, disc_check_interval
    configDefault = """[makemkv]
; Path to MakeMKV
; must be an absolute path and must end in \\
makemkv_path = C:\Program Files (x86)\MakeMKV


; Path to the directory where the output files will be saved
; a new folder will be created at this path for each disc
; must be an absolute path and must end in \\
makemkv_output = \\192.168.1.118\Home\Movies\\


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
open_tray = 1


; interval of when a disc will be checked in seconds
disc_check_interval = 5

"""


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

    out = GetInfo(makemkv_path)
    outlines = out.splitlines()
    outSplit = outlines[1].split(",") 
    letter =  outSplit[6].replace('"', '').removesuffix(":")
    return letter

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
def WaitForDisc(disc_check_interval, letter):
    loadingstrings = [".","..","..."]
    loadingindex = 0
    #bad but easy
    while True:
        try:
            os.listdir(f"{letter}:\\")
            sys.stdout.write('\033[2K\033[1G')
            print("found a disc!")
            return
        except:
            sys.stdout.write('\033[2K\033[1G')
            print(f"Waiting for a disc{loadingstrings[loadingindex]}", end = "\r")
            if(loadingindex < 2): loadingindex+=1
            else: loadingindex = 0
            time.sleep(disc_check_interval)
        

#run the makemkv command and start ripping the files
def Rip(makemkv_args, makemkv_path):
    subpr = subprocess.Popen(args = makemkv_args, executable=f"{makemkv_path}\\makemkvcon64.exe", shell=False, stdout= subprocess.PIPE, text=True)
    while True:
        line = subpr.stdout.readline()
        if not line:
            break
        lineStrip = line.rstrip()

        if("PRGV" in lineStrip):
            total = lineStrip.split(":")[1].split(",")[2]
            current = lineStrip.split(":")[1].split(",")[0]
            bardata = progressBar.filledBar(int(total), int(current))
            sys.stdout.write('\033[2K\033[1G')
            print(bardata, end = "\r")
    return



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


def main(letter):
    WaitForDisc(disc_check_interval, letter)
    ReadyToRip()
    if(trayOpen):
        open_tray.Run(letter)

    main(letter)






main(Startup())