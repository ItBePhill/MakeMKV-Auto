import DiscInfo
import subprocess
import configparser
import datetime
import os
import psutil
import time
import open_tray
makemkv_config:list

def Cancel():
    if subpr.poll() is None:
        subpr.kill()


def Rip(disc):
    global subpr
    # compile the args
    makemkv_args = [
        f"{makemkv_config[0]}makemkvcon64",
        "mkv",
        f"disc:{makemkv_config[2]}", 
        "all",
        "--decrypt", 
        f"--cache={makemkv_config[3]}", 
        f"--minlength={makemkv_config[4]}", 
        "--noscan",  
        "--progress=-same",
        "--robot", 
        f"--directio={makemkv_config[5]}",
        disc.path
    ]
    
    # create the output folder
    print(f"MSG|Creating: {disc.path}")
    if not os.path.exists(disc.path): os.mkdir(disc.path)
    # get the current time before ripping
    t1 = datetime.datetime.now()
    print(f"MSG|Started rip at: {t1}")
    # rip the movie and continually grab output from stdout
    subpr = subprocess.Popen(args = makemkv_args, stdout = subprocess.PIPE)
    print(f"Ripping: {disc.name}")
    print("\n")
    #read the output as it comes in
    while subpr.poll() is None:    
        print(f"MI|{round(psutil.Process(subpr.pid).memory_info()[0] / 1000000, 2)} MB") 
        outbytes = subpr.stdout.readline() # type: ignore | This error is erroneous, the type is not None and therefore is being ignored
        out = outbytes.decode("utf-8")
        if("MSG:5014" in out):
            print(f"TINF|{out.split(",")[3].split(" ")[1]}")
        if("PRGV:" in out):
            total = out.split(":")[1].split(",")[2]
            current = out.split(":")[1].split(",")[0]
            print("PG|"+current + "/" +total + "\n")
        if out.startswith("MSG:"):
            print("MSG|"+out.split(",")[3].replace('"', ''))
        
    # get time after rip
    t2 = datetime.datetime.now()
    # show results and then wait for another disc
    print(f"MSG|Rip finished at: {t2}", flush=True)
    print(f"MSG|Taking: {t2-t1}", flush=True)
    open_tray.Run(disc.letter)






def WaitForDisc():
    disc = None
    makemkv_info_args = [
         f"{makemkv_config[0]}makemkvcon64",
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
        except Exception as exc:
            if "Failed to Open Disc, is one inserted?" in exc.args:
                print("Didn't find a disc")
            else:
                print(exc.args)
            print("MSG|Waiting for a disc" + dots[x], flush=True)
            print(f"PG|{x+1} / {3}")
            x+=1
            continue
            
        else:
            print(f"INF0|{disc.name}")
            print(f"INF1|{disc.length}")
            print(f"INF2|{disc.path}")
            print(f"INF3|{disc.titles}")
            print(f"MSG|Preparing to rip: {disc.name}", flush=True)
            Rip(disc)
            open_tray.Run(disc.letter)
            continue





def Startup():
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


    print(makemkv_path)
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
    print(str(int(makemkv_config[2])))
    
    WaitForDisc()
        

    


