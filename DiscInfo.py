import os
import subprocess
import tempfile
import UI

#Class that holds all the information about a disc e.g. the id, name, size
class Disc:
    name: str
    length: str
    path: str
    titles: str
    letter:str
    

def GetDisc(makemkv_info_args:list, makemkv_config:list):
    disc:Disc = Disc()

    subpr = subprocess.Popen(args = makemkv_info_args, stdout = subprocess.PIPE)
    #read the output as it comes in
    while subpr.poll() is None:     
        outbytes = subpr.stdout.readline() # type: ignore
        out = outbytes.decode("utf-8")
        
        if out.startswith("DRV:0,1"):
            raise Exception("Failed to Open Disc, is one inserted?")
        if out.startswith("DRV:0,2"):
            print("We Found a Disc!")
            disc.path = makemkv_config[1] + out.split(",")[5].replace('"','')
            disc.letter = out.split(",")[6].replace('"', '').replace(":", "")

        if out.startswith("TINFO:0,2,0"):
            disc.name =  out.split(",")[3].replace('"', '')
        if out.startswith("TINFO:0,9"):
            disc.length = out.split(",")[3].replace('"', '')
        if out.startswith("TCOUNT:"):
            disc.titles = out.split(":")[1]
    print(f"Name: {disc.name}\nLength: {disc.length}\nPath: {disc.path}\nLetter: {disc.letter}")
    return disc