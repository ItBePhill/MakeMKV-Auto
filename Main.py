import UI
import threading
import configparser
import os
import DiscInfo
import time
import open_tray
import subprocess
import datetime
import psutil


def DebugRun():
    name = "Debug Test Disc"
    titles = 2
    path = "/path/to/output/DEBUG_TEST_DISC"
    UI.logMsg(f"Ripping: {name}")
    print("\n")
    currenttitle = "0"
    log = ""
    current = 0
    total = 0
    maxVal = 100
    mem = ""
    current_title = 1
    for i in range(0, titles):
        for i in range(0, maxVal, 5):
            if UI.header.running:
                time.sleep(1)
                mem = f"{i * 100} MB"
                currenttitle = current_title
                total = maxVal
                current = i
                log = f"Log: {i}" 
                UI.Update(name, f"Saving {currenttitle} of {titles} title(s) to: {path}", log, current, mem, total)
            else:
                break
        if not UI.header.running:
            break
        current_title+=1
    UI.Cancel()
    return

def Run(disc:DiscInfo.Disc):
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
    subpr = subprocess.Popen(args = makemkv_args, stdout = subprocess.PIPE)
    UI.logMsg(f"Ripping: {disc.name}")
    print("\n")
    currenttitle = "0"
    log = ""
    current = 0
    total = 0
    mem = ""
    
    while subpr.poll() is None and UI.header.running:
        mem = f"{round(psutil.Process(subpr.pid).memory_info()[0] / 1000000, 2)} MB"
        outbytes = subpr.stdout.readline() # type: ignore | This error is erroneous, the type is not None and therefore is being ignored
        out = outbytes.decode("utf-8")
        if("MSG:5014" in out):
            currenttitle = UI.cleanStr(f"{out.split(",")[3].split(" ")[1]}")
        if("PRGV:" in out):
            total = int(UI.cleanStr(out.split(":")[1].split(",")[2]))
            current = int(UI.cleanStr(out.split(":")[1].split(",")[0]))

        if out.startswith("MSG:"):
            log = UI.truncateStr(UI.cleanStr(out.split(",")[3].replace('"', '')), 50)
        UI.Update(disc.name, f"Saving {currenttitle} of {disc.titles} title(s) to: {disc.path}", log, current, mem, total)
    if not UI.header.running:
        subpr.kill()
    elif subpr.returncode == 0:
        subpr.terminate()
    else:
        print(f"Something went wrong and the process had to quit return code: {subpr.returncode}")
        UI.logMsg(f"Something went wrong and the process had to quit return code: {subpr.returncode}")
    UI.Cancel()
    return





def WaitForDisc():
    disc = None
    UI.header.ui.waiting = True
    if os.path.exists(f"{makemkv_config[0]}makemkvcon64"): path = f"{makemkv_config[0]}makemkvcon64"
    elif os.path.exists(f"{makemkv_config[0]}makemkvcon"): path = f"{makemkv_config[0]}makemkvcon"
    else: 
        print("MakeMKV couldn't be found is it installed?")
        os.system("pause")
        exit()

    makemkv_info_args = [
         path,
         "info",
         f"disc:{makemkv_config[2]}", 
         "--robot",
        f"--minlength={makemkv_config[4]}"
    ] 
    while disc == None:
        time.sleep(int(makemkv_config[9]))
        #this will continuosly run GetDisc, which will either return a disc or throw an error
        if(not makemkv_config[10]):
            try:
                disc = DiscInfo.GetDisc(makemkv_info_args, makemkv_config)
                disc.letter = UI.cleanStr(disc.letter)
            except Exception as exc:
                if "Failed to Open Disc, is one inserted?" in exc.args:
                    print("Couldn't Find Disc")
                else:
                    UI.logMsg(exc.args)
                continue
                
            else:
                UI.logMsg(f"Preparing to rip: {disc.name}")
                UI.header.ui.waiting = False
                UI.header.running = True
                Run(disc)
                open_tray.Run(disc.letter)
                disc = None
                continue
        else:
            UI.header.ui.waiting = False
            UI.header.running = True
            DebugRun()
            continue



def Start():
    global makemkv_config
    configDefault = r"""[makemkv]
    ; Path to MakeMKV
    ; must be an absolute path
    ;!! If you are on linux and have installed makemkv via the forum post !!
    ;!! Leave this as a single backslash (\) as makemkvcon is on the PATH !!
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

    ;if set to 1 will bypass makemkv and run a debug script instead
    debug_mode = 0

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
    log_to_file = config.getboolean("general", "log_to_file")
    debug_mode = config.getboolean("general", "debug_mode")
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
        debug_mode              #10
    ]
    
    #start the thread that will rip and provide the 
    UI.Init()
    thread = threading.Thread(name="WaitThread", target=WaitForDisc, daemon=True)
    thread.start()
    while True:
        UI._TkUpdate()

Start()