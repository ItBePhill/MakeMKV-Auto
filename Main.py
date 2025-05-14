# MakeMKV_Auto - Phill
# use makemkv to rip a DVD or Blu-ray disc
# pop open the disc drive when ready for a disc / done

import configparser
import subprocess
import os
import string
def Startup():
    if not os.path.exists("config.ini"):
        with open("config.ini", 'w') as configfile:
            pass

def GetInfo():
    return
#run the makemkv command and start ripping the files
def Rip(makemkv_args, makemkv_path):
    commandstr = ""
    for i in makemkv_args:
        commandstr += f"{i} "
    print("Arguments: ", commandstr)
    subprocess.run(makemkv_args, -1, makemkv_path, shell=True)
    
def main():
    Startup()
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
    makemkv_args = [
        "--decrypt", 
        f"--cache={makemkv_cache_size}", 
        f"--minlength={makemkv_min_length}", 
        "--noscan",  
        "--robot", 
        f"--directio={makemkv_directio}",
        "mkv",
        f"disc:{makemkv_disc}", 
        "all",
        makemkv_output
    ]
    #get movie info for folder name and 
    Rip(makemkv_args, makemkv_path)






main()