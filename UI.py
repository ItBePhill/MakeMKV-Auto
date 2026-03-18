import tkinter as tk
import ttkbootstrap as ttk
from tkinter import font
import subprocess
import threading
import datetime

"""
TODO:
 -----------
| key:      |
| / = doing |
| // = done |
|           |
 -----------


    - Calculate and show the ETA //
    - Get and show how many titles there are and which we are currently ripping /
    - change the window title to ripping if we are ripping and waiting if we are waiting
"""


root = ttk.Window(themename='darkly', iconphoto=None)
windowStr="MakeMKV-Auto | "
windowTitleStr:str = windowStr + ""
root.title(windowTitleStr)


titleStr = "Waiting for Disc..."
subtitleStr = "Waiting for Disc..."
logStr = "Waiting for Disc..."
etaStr =  "N/A"
pgValue = 0
pgMax = 0
elapsedStr = "N/A"

Width = 600
Height = 150
root.minsize(Width,Height)
root.maxsize(Width,Height)
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
subtitle =  ttk.Label(titleframe, textvariable=subtitleVar, font=subtitleFont, wraplength=9000)
pgVar = tk.IntVar(root, 0)
prgbar = ttk.Progressbar(otherFrame, variable=pgVar, length=Width-50)
logVar = tk.StringVar(root, "N/A")
log = ttk.Label(otherFrame, textvariable = logVar, font=defaultFont, width=30)
etaVar =  tk.StringVar(root, "N/A")
eta = ttk.Label(otherFrame, textvariable=etaVar, font=defaultFont)
elapsedVar =  tk.StringVar(root, "N/A")
elapsed = ttk.Label(otherFrame, textvariable=elapsedVar, font=defaultFont)
title.grid(sticky="nw", row=0)  
subtitle.grid(stick="nw", row=1)
prgbar.grid(sticky="w", row=2, pady=2)
log.grid(sticky="w", row=3)
eta.grid(sticky="e", row=3, pady=2)
elapsed.grid(sticky="nse", row=3, pady=2, padx=70)


#Start the process for the main program
args = ["python", "main.test.py"]
subpr = subprocess.Popen(args = args, stdout = subprocess.PIPE)     
out = ""
def run():
    global out, titleStr, subtitleStr, logStr, etaStr, pgValue, pgMax, elapsedStr, windowTitleStr
    startTime:datetime.datetime = datetime.datetime.now()
    last_time = datetime.datetime.now()
    last_value = 0
    last_speed = 0
    path = "0"
    total = "0"
    while subpr.poll() is None:
        elapsedStr = datetime.timedelta(seconds=round(datetime.datetime.now().timestamp() - startTime.timestamp()))
        out = subpr.stdout.readline().decode() #type:ignore
        print(out)
        if out.startswith("ST|"):
            windowTitleStr = windowStr + out.split("|")[1].replace("\n", "")
        if out.startswith("INF0|"):
            titleStr = out.split("|")[1].replace("\n", "")
        if out.startswith("INF2|"):
            path =  f"Saving to: {out.split("|")[1].replace("\n", "")}"
        if out.startswith("INF3|"):
            total = out.split("|")[1].replace("\n", "")
        if out.startswith("TINF|"):
            subtitleStr = f"Saving: {out.split("|")[1].replace("\n", "")} of {total} title(s) to: {path}"
        if out.startswith("MSG|"):
            logStr = out.split("|")[1].replace("\n", "")
        if out.startswith("PG|"):  
            pgValue = int(out.split("|")[1].split("/")[0])
            pgMax = int(out.split("|")[1].split("/")[1])
            # Source - https://stackoverflow.com/a/929104
            new_value = ((pgValue - 0) / (pgMax - 0) ) * (100 - 0) + 0
            print("\n\n\n")

            print(f"Percentage: {new_value.__floor__()}%")
            pgValue = new_value
            #calculate average speed
            valueDiff = new_value - last_value
            timeDiff = datetime.datetime.now().timestamp() - last_time.timestamp()
            #we progressed valuediff amount in timeDiff time
            # e.g. 1 unit in 1 second
            

            smoothing = .1
            speed = valueDiff / timeDiff if timeDiff > 0 else 0
            if speed <=0:
                smoothed_speed = last_speed

            else:
                smoothed_speed = smoothing * speed + (1-smoothing) * last_speed
            
            speed = smoothed_speed

            if speed <= 0:
                etaTime = 0
            else:
                remaining = 100 - new_value 
                etaTime = remaining / speed

            etaStr = str(datetime.timedelta(seconds=int(etaTime)))
            print(f"Time Elapsed: {elapsedStr}")
            print(f"Average Speed: {round(speed, 2)} u/{round(timeDiff, 2)}s")
            print(f"ETA: {etaStr}")

            windowTitleStr = windowTitleStr
            last_value = new_value
            last_time = datetime.datetime.now()
            last_speed = speed



            
            

            

#since tkinter is single threaded we can't gather info in the main loop
#so we need to create a new thread for it           
#we create a thread to gather the info from stdout
thread = threading.Thread(target = run, name = "GatherThread")
thread.start()

#main thread has to be in tk loop so we update the widgets from the tk loop
def updateVars():
    global logVar, subtitleVar, titleVar, etaVar, pgVar, elapsedVar
    titleVar.set(titleStr)
    subtitleVar.set(subtitleStr)
    pgVar.set(int(pgValue))
    logVar.set(logStr)
    etaVar.set(etaStr)
    elapsedVar.set(str(elapsedStr))
    root.title(windowTitleStr)
    

#tk loop
while True:
    updateVars()
    root.update_idletasks()
    root.update()
    

    
