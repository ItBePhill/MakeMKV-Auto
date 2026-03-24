import tkinter as tk
from tkinter import font
import ttkbootstrap as ttk

import datetime
from PyTaskbar import TaskbarProgress, ProgressType

def truncateStr(string:str, maxLength=400):
    return string if len(string) <= maxLength else string[:maxLength-3] + "..."

def cleanStr(string:str):
    return string.replace("\n", "").replace("\r", "")

class UI:
    def __init__(self):
        #---------- String Variables ---------
        self.windowTitleStr:str = "MakeMKV-Auto"
        self.titleStr:str = "N/A"
        self.subtitleStr:str = "N/A"
        self.logStr:str = "N/A"
        self.etaStr:str = "0:00:00"
        self.pValue:str = "0"
        self.elapsedStr:str = "0:00:00"
        self.memStr:str = 0
        self.Width:str = 650
        self.Height:str = 150
        #---------- TK ----------
        self.root = ttk.Window(themename="darkly")
        self.root.minsize(self.Width,self.Height)
        self.root.maxsize(self.Width,self.Height)
        #--------- Fonts ----------
        self.titleFont = font.Font(self.root, name="title", family="Segoe UI", size=12, weight='bold')
        self.subtitleFont = font.Font(self.root, name="subtitle", family="Segoe UI", size=9, weight='normal')
        self.defaultFont = font.Font(self.root, name="default", family="Segoe UI", size=9, weight='normal')
        #---------- TK Variables --------
        self._titleVar = tk.StringVar()
        self._subtitleVar = tk.StringVar()
        self._logVar = tk.StringVar()
        self._etaVar = tk.StringVar()
        self._pVar = tk.IntVar()
        self._elapsedVar = tk.StringVar()
        self._memVar = tk.StringVar()
        #--------- TK Widgets ----------
        self.mainFrame = ttk.Frame(self.root)
        self.titleFrame = ttk.Frame(self.mainFrame)
        self.otherFrame = ttk.Frame(self.mainFrame)
        self.title = ttk.Label(self.titleFrame, textvariable=self._titleVar, font = self.titleFont)
        self.subtitle =  ttk.Label(self.titleFrame, textvariable=self._subtitleVar, font=self.subtitleFont, wraplength=self.Width-40)
        self.pBar = ttk.Progressbar(self.otherFrame, variable=self._pVar, length=self.Width-50)
        self.log = ttk.Label(self.otherFrame, textvariable = self._logVar, font=self.defaultFont)
        self.eta = ttk.Label(self.otherFrame, textvariable=self._etaVar, font=self.defaultFont)
        self.elapsed = ttk.Label(self.otherFrame, textvariable=self._elapsedVar, font=self.defaultFont)
        self.mem = ttk.Label(self.otherFrame, textvariable=self._memVar, font=self.defaultFont)
        
        #place all of the widgets
        self.mainFrame.pack(anchor="w", padx=10, pady=10, fill="both")
        self.titleFrame.pack(fill="x", anchor="nw")
        self.otherFrame.pack(fill="x", anchor="sw")
        self.title.grid(sticky="nw", row=0)  
        self.subtitle.grid(sticky="ew", row=1)
        self.pBar.grid(sticky="w", row=2, pady=2)
        self.log.grid(sticky="w", row=4)
        self.eta.grid(sticky="e", row=4, pady=2)
        self.elapsed.grid(sticky="nse", row=4, pady=2, padx=70)
        self.mem.grid(sticky="w", row=5, pady=2)
       
    def reset(self):
        self.titleStr = "N/A"
        self.subtitleStr = "N/A"
        self.pValue = 0
        self.logStr = "N\A"
        self.etaStr = "0:00:00"
        self.elapsedStr = "0:00:00"
        self.memStr = "N/A"
        self.windowTitleStr = "MakeMKV-Auto"
        self.update()
    def update(self):    
        try: 
            self.root.winfo_exists()
        except:
            print("Couldn't find the window... Closing")
            quit()
        #update widgets
        self._titleVar.set(self.titleStr)
        self._subtitleVar.set(self.subtitleStr)
        self._pVar.set(self.pValue)
        self._logVar.set(self.logStr)
        self._etaVar.set(self.etaStr)
        self._elapsedVar.set(self.elapsedStr)
        self._memVar.set(self.memStr)
        self.root.title(self.windowTitleStr)

        #run tk update loop
        self.root.update_idletasks()
        self.root.update()
        
def Cancel(updater, ui):
    del updater
    ui.reset()
#an instance of this class will be called every time we start a new task
class Updater:
    def __init__(self):
        self.startTime = datetime.datetime.now()
        self.last_time = datetime.datetime.now()
        self.last_value = 0
        self.last_speed = 0
        self.path = ""
        self.total = 0

def Update(updater, ui, title, subtitle, log, value, mem, max):
        ui.titleStr = title
        ui.subtitleStr = subtitle
        ui.pValue = value
        ui.logStr = log
        ui.memStr = mem
        # Source - https://stackoverflow.com/a/929104
        new_value = ((value - 0) / (max - 0) ) * (100 - 0) + 0
        print("\n\n\n")

        print(f"Percentage: {new_value.__floor__()}%")
        # pgValue = new_value
        # progress.setself._progress(int(new_value))
        #calculate average speed
        valueDiff = new_value - updater.last_value
        timeDiff = datetime.datetime.now().timestamp() - updater.last_time.timestamp()
        #we progressed valuediff amount in timeDiff time
        # e.g. 1 unit in 1 second
        

        smoothing = .1
        speed = valueDiff / timeDiff if timeDiff > 0 else 0
        if speed <=0:
            smoothed_speed = updater.last_speed

        else:
            smoothed_speed = smoothing * speed + (1-smoothing) * updater.last_speed
        
        speed = smoothed_speed

        if speed <= 0:
            etaTime = 0
        else:
            remaining = 100 - new_value 
            etaTime = remaining / speed

        ui.etaStr = str(datetime.timedelta(seconds=int(etaTime)))
        print(f"Time Elapsed: {ui.elapsedStr}")
        print(f"Average Speed: {round(speed, 2)} u/{round(timeDiff, 2)}s")
        print(f"ETA: {ui.etaStr}")


        ui.windowTitleStr = f"{new_value.__floor__()}% | {ui.elapsedStr} | {ui.etaStr}"
        updater.last_value = new_value
        updater.last_time = datetime.datetime.now()
        updater.last_speed = speed
def Init():
    updater = Updater()
    ui = UI()
    return updater, ui