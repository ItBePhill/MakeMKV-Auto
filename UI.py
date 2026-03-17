import tkinter as tk
import ttkbootstrap as ttk
from tkinter import font
import subprocess
import threading

root = ttk.Window(themename='cyborg', iconphoto=None)
windowStr="MakeMKV-Auto"
windowTitleStr:str = windowStr + " | N/A"
root.title(windowTitleStr)


titleStr = "N/A"
subtitleStr = "N/A"
logStr = "N/A"
etaStr =  "N/A"
pgValue = 0
pgMax = 0


Width = 600
Height = 150
root.minsize(Width,Height)
#root.maxsize(Width,Height)
titleFont = font.Font(root, name="title", family="Segoe UI", size=12, weight='bold')
subtitleFont = font.Font(root, name="subtitle", family="Segoe UI", size=9, weight='normal')
defaultFont = font.Font(root, name="default", family="Segoe UI", size=9, weight='normal')
frame = ttk.Frame(root)
frame.pack(anchor="w", padx=10, pady=10, fill="both")
titleframe = ttk.Frame(frame)
titleframe.pack(fill="x", anchor="nw")
otherFrame = ttk.Frame(frame)
otherFrame.pack(fill="x", anchor="sw")

titleVar = tk.StringVar(root, "N/A")
title = ttk.Label(titleframe, textvariable=titleVar, font = titleFont)
subtitleVar = tk.StringVar(root, "N/A")
subtitle =  ttk.Label(titleframe, textvariable=subtitleVar, font=subtitleFont)
pgVar = tk.IntVar(root, 0)
prgbar = ttk.Progressbar(otherFrame, variable=pgVar, length=Width-50)
logVar = tk.StringVar(root, "N/A")
log = ttk.Label(otherFrame, textvariable = logVar, font=defaultFont)
etaVar =  tk.StringVar(root, "N/A")
eta = ttk.Label(otherFrame, textvariable=etaVar, font=defaultFont)
title.grid(sticky="nw", row=0)  
subtitle.grid(stick="nw", row=1)
prgbar.grid(sticky="w", row=2, pady=2)
log.grid(sticky="w", row=3)
eta.grid(sticky="e", row=3, pady=2)


#Start the process for the main program
etaTime = None

args = ["python", "main.test.py"]
subpr = subprocess.Popen(args = args, stdout = subprocess.PIPE)     
out = ""
def run():
    global out, titleStr, subtitleStr, logStr, etaStr, pgValue, pgMax
    while subpr.poll() is None:
        out = subpr.stdout.readline().decode() #type:ignore
        print(out)
        if out.startswith("INF0|"):
            titleStr = out.split("|")[1].replace("\n", "")
        if out.startswith("INF2|"):
            subtitleStr =  f"Saving to: {out.split("|")[1].replace("\n", "")}"
        if out.startswith("MSG|"):
            logStr = out.split("|")[1].replace("\n", "")
        if out.startswith("PG|"):
            # Source - https://stackoverflow.com/a/929104
            pgValue = int(out.split("|")[1].split("/")[0])
            
            pgMax = int(out.split("|")[1].split("/")[1])
            new_value = ( (pgValue - 0) / (pgMax - 0) ) * (100 - 0) + 0
            pgValue = new_value

           

thread = threading.Thread(target = run, name = "GatherLoop")
thread.start()

def updateVars():
    global logVar, subtitleVar, titleVar, etaVar, pgVar
    titleVar.set(titleStr)
    subtitleVar.set(subtitleStr)
    pgVar.set(float(pgValue))
    logVar.set(logStr)
    etaVar.set(etaStr)
    

#tk loop
while True:
    updateVars()
    root.update_idletasks()
    root.update()
    

    
