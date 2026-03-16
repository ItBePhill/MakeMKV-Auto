import tkinter as tk
import ttkbootstrap as ttk
from tkinter import font
import subprocess
import threading

root = ttk.Window(themename='darkly', iconphoto=None)
windowStr="MakeMKV-Auto"
windowTitleStr:str = windowStr + " | N/A"
titleStr:str = "N/A"
subtitleStr:str = "N/A"
logStr:str = "N/A"
etaStr: str = "N/A"
prgBarValue =  0
prgBarMax = 100


Width = 600
Height = 150
root.minsize(Width,Height)
root.maxsize(Width,Height)
titleFont = font.Font(root=root, name="title", family="Segoe UI", size=12, weight='bold')
subtitleFont = font.Font(root=root, name="subtitle", family="Segoe UI", size=9, weight='normal')
defaultFont = font.Font(root=root, name="default", family="Segoe UI", size=9, weight='normal')
frame = ttk.Frame(root)
frame.pack(anchor="w", padx=10, pady=10)

otherFrame = ttk.Frame(frame)
otherFrame.grid(row=1, sticky="sw", pady=5)
titleframe = ttk.Frame(frame)
titleframe.grid(row=0, sticky="nw", pady=5)
title = ttk.Label(titleframe, text = titleStr, font = titleFont)
subtitle =  ttk.Label(titleframe, text = subtitleStr, font=subtitleFont)
progress = tk.IntVar()
prgbar = ttk.Progressbar(otherFrame, variable=prgBarValue, maximum=prgBarMax, length=Width-50)
log = ttk.Label(otherFrame, text = logStr, font=defaultFont)
eta = ttk.Label(otherFrame, text=etaStr, font=defaultFont)
title.grid(sticky="nw", row=0)  
subtitle.grid(stick="nw", row=1)
prgbar.grid(sticky="w", row=2, pady=2)
log.grid(sticky="w", row=3)
eta.grid(sticky="e", row=3, pady=2)


#Start the process for the main program
args = ["python", "main.py"]
subpr = subprocess.Popen(args = args, stdout = subprocess.PIPE)     
out = ""
def run():
    global out, logStr, subtitleStr, windowTitleStr, titleStr, etaStr, prgBarValue, prgBarMax
    while True:
        out = subpr.stdout.readline().decode() #type:ignore
        if out.startswith("MSG|"):
            logStr = out.split("|")[1]
            #windowTitleStr = windowStr + " | " + out.split("|")[1]
        if out.startswith("PG|"):
            print(out.split("|")[1])
            prgBarValue = out.split("|")[1].split("/")[0]
            prgBarMax = out.split("|")[1].split("/")[1]

thread = threading.Thread(target = run, name = "Main loop")
thread.start()
    
def updateWidgets():
    global progress
    root.title(windowTitleStr)
    title.configure(text=titleStr)
    subtitle.configure(text=subtitleStr)
    progress = prgBarValue
    prgbar.configure(maximum=prgBarMax)
    log.configure(text=logStr)
    eta.configure(text=etaStr)
#tcl main loop and program main loop
while True:
    root.update_idletasks()
    root.update()
    updateWidgets()

    
