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
    
     #---------- String Variables ---------
    windowTitleStr:str = ""
    titleStr:str = ""
    subtitleStr:str = ""
    logStr:str = ""
    etaStr:str = ""
    pValue:str = ""
    elapsedStr:str = ""
    memStr:str = ""
    Width:str = 650
    Height:str = 150
    #---------- TK ----------
    root = ttk.Tk()
    root.minsize(Width,Height)
    root.maxsize(Width,Height)
    #--------- Fonts ----------
    titleFont = font.Font(root, name="title", family="Segoe UI", size=12, weight='bold')
    subtitleFont = font.Font(root, name="subtitle", family="Segoe UI", size=9, weight='normal')
    defaultFont = font.Font(root, name="default", family="Segoe UI", size=9, weight='normal')
    #---------- TK Variables --------
    _titleVar = tk.StringVar()
    _subtitleVar = tk.StringVar()
    _logVar = tk.StringVar()
    _etaVar = tk.StringVar()
    _pVar = tk.IntVar()
    _elapsedVar = tk.StringVar()
    _memVar = tk.StringVar()
    #--------- TK Widgets ----------
    mainFrame = ttk.Frame(root)
    titleFrame = ttk.Frame(mainFrame)
    otherFrame = ttk.Frame(mainFrame)
    title = ttk.Label(titleFrame, textvariable=_titleVar, font = titleFont)
    subtitle =  ttk.Label(titleFrame, textvariable=_subtitleVar, font=subtitleFont, wraplength=Width-40)
    pBar = ttk.Progressbar(otherFrame, variable=_pVar, length=Width-50)
    log = ttk.Label(otherFrame, textvariable = _logVar, font=defaultFont)
    eta = ttk.Label(otherFrame, textvariable=_etaVar, font=defaultFont)
    elapsed = ttk.Label(otherFrame, textvariable=_elapsedVar, font=defaultFont)
    mem = ttk.Label(otherFrame, textvariable=_memVar, font=defaultFont)
    
    
    title.grid(sticky="nw", row=0)  
    subtitle.grid(sticky="ew", row=1)
    pBar.grid(sticky="w", row=2, pady=2)
    log.grid(sticky="w", row=4)
    eta.grid(sticky="e", row=4, pady=2)
    elapsed.grid(sticky="nse", row=4, pady=2, padx=70)
    mem.grid(sticky="w", row=5, pady=2)
       

    def update(self):
        self._titleVar.set(self.titleStr)
        self._subtitleVar.set(self.subtitleStr)
        self._pVar.set(self.pValue)
        self._logVar.set(self.logStr)
        self._etaVar.set(self.etaStr)
        self._elapsedVar.set(self.elapsedStr)
        self._memVar.set(self.memStr)
        self.root.title(self.windowTitleStr)

        self.root.update_idletasks()
        self.root.update()
        

#an instance of this class will be called every time we start a new task
class Updater:
    def __init__():
        startTime = datetime.datetime.now()
        last_time = datetime.datetime.now()
        last_value = 0
        last_speed = 0
        path = "0"
        total = "0"
    #this will update all of the strings and progressBar
    def Update(self, ui, title, subtitle, value, mem, max):
        ui.titleStr = title
        ui.subtitleStr = subtitle
        ui.pValue = value
        ui.memStr = mem
        # Source - https://stackoverflow.com/a/929104
        new_value = ((value - 0) / (max - 0) ) * (100 - 0) + 0
        print("\n\n\n")

        print(f"Percentage: {new_value.__floor__()}%")
        # pgValue = new_value
        # progress.set_progress(int(new_value))
        #calculate average speed
        valueDiff = new_value - self.last_value
        timeDiff = datetime.datetime.now().timestamp() - self.last_time.timestamp()
        #we progressed valuediff amount in timeDiff time
        # e.g. 1 unit in 1 second
        

        smoothing = .1
        speed = valueDiff / timeDiff if timeDiff > 0 else 0
        if speed <=0:
            smoothed_speed = self.last_speed

        else:
            smoothed_speed = smoothing * speed + (1-smoothing) * self.last_speed
        
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
        self.last_value = new_value
        self.last_time = datetime.datetime.now()
        self.last_speed = speed


def Init():
    updater = Updater()
    ui = UI()
    return updater, ui