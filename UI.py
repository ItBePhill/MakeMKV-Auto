import tkinter as tk
from tkinter import font
import ttkbootstrap as ttk
import datetime
from PyTaskbar import TaskbarProgress, ProgressType
import time
def truncateStr(string:str, maxLength=400):
    return string if len(string) <= maxLength else string[:maxLength-3] + "..."

def cleanStr(string:str):
    return string.replace("\n", "").replace("\r", "")
        


def Cancel():
    global header
    header.updater = Updater()
    header.ui.reset()
    header.running = False
class UI:
    def __init__(self):
        self.waiting:bool = True
        #---------- String Variables ---------
        self.titleStr = "Looking For a Disc..."
        self.subtitleStr = "Looking For a Disc..."
        self.pValue = 0
        self.logStr = "Looking For a Disc..."
        self.etaStr = "0:00:00"
        self.elapsedStr = "0:00:00"
        self.memStr = "0 MB"
        self.windowTitleStr = "MakeMKV-Auto"
        self.Width:int = 650
        self.Height:int = 170
        #---------- TK ----------
        self.root = ttk.Window(themename="darkly", alpha=0.95)
        

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
        self.pBar = ttk.Progressbar(self.otherFrame, variable=self._pVar, length=self.Width-50, mode="indeterminate")
        self.log = ttk.Label(self.otherFrame, textvariable = self._logVar, font=self.defaultFont)
        self.eta = ttk.Label(self.otherFrame, textvariable=self._etaVar, font=self.defaultFont)
        self.elapsed = ttk.Label(self.otherFrame, textvariable=self._elapsedVar, font=self.defaultFont)
        self.mem = ttk.Label(self.otherFrame, textvariable=self._memVar, font=self.defaultFont)
        self.cancelButton = ttk.Button(self.otherFrame, text="Abort", command=Cancel)
        
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
        self.cancelButton.grid(sticky="e", row=5, pady=2)
       
    def reset(self):
        self.titleStr = "Looking For a Disc..."
        self.subtitleStr = "Looking For a Disc..."
        self.pValue = 0
        self.logStr = "Looking For a Disc..."
        self.etaStr = "0:00:00"
        self.elapsedStr = "0:00:00"
        self.memStr = "0 MB"
        self.windowTitleStr = "MakeMKV-Auto"
        self.waiting = True
        

#an instance of this class will be called every time we start a new task
class Updater:
    def __init__(self):
        self.startTime = datetime.datetime.now()
        self.last_time = datetime.datetime.now()
        self.last_value = 0
        self.last_speed = 0
        self.path = ""
        self.total = 0

def logMsg(logStr):
    ui = header.ui
    ui.logStr = logStr
def Update(title, subtitle, log, value, mem, maxVal):
        ui = header.ui
        ui.titleStr = title
        ui.subtitleStr = subtitle
        updater = header.updater
        ui.logStr = log
        ui.memStr = mem
        # Source - https://stackoverflow.com/a/929104
        new_value = (value / maxVal) * 100 if maxVal > 0 and value > 0 else 0
        print("\n\n\n")
        print(f"Percentage: {int(new_value)}%")
        # pgValue = new_value
        # progress.setself._progress(int(new_value))
        #calculate average speed
        valueDiff = new_value - updater.last_value
        timeDiff = datetime.datetime.now().timestamp() - updater.last_time.timestamp()
        #we progressed valuediff amount in timeDiff time
        # e.g. 1 unit in 1 second
        ui.pValue = int(new_value)

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
        print(f"Average Speed: {round(speed, 2)} u/{round(timeDiff, 4)}s")
        print(f"ETA: {ui.etaStr}")


        ui.windowTitleStr = f"{int(new_value)}% | {ui.elapsedStr} | {ui.etaStr}"
        updater.last_value = int(new_value)
        updater.last_time = datetime.datetime.now()
        updater.last_speed = speed

class uiHeader:
    running:bool = True
    updater:Updater
    ui:UI
    def __init__(self):
        self.running:bool = True
        self.updater:Updater = None
        self.ui:UI = None
header:uiHeader

def ButtonYes():
    pass
def ButtonNo():
    pass
def ClosePopup():
    top = ttk.Toplevel("Are you sure you want to Quit?")
    NoButton = ttk.Button(top, "No", command=ButtonNo)
    YesButton = ttk.Button(top, "Yes", command=ButtonYes)
    NoButton.grid(row=0, sticky="SW")
    YesButton.grid(row=0, sticky="SW")
    

    

def CouldntFindPopup():
    pass
def Init():
    global header
    header = uiHeader()
    header.updater = Updater()
    header.ui = UI()

maxIn = 100
def _TkUpdate():
    ui = header.ui
    while True:
        try: 
            ui.root.winfo_exists()
        except:
            print("Couldn't find the window... Closing")
            quit()
        ui.elapsedStr = str(datetime.timedelta(seconds=int(datetime.datetime.now().timestamp()) - int(header.updater.startTime.timestamp())))
        ui._titleVar.set(cleanStr(truncateStr(ui.titleStr)))
        ui._subtitleVar.set(cleanStr(truncateStr(ui.subtitleStr)))
        if ui.waiting:
            if ui.pBar.cget("mode") != "indeterminate":
                ui.pBar.configure(mode="indeterminate")         
            ui.pValue+=1
            if ui.pValue >= 100:
                ui.pValue = -100
        else:
            if ui.pBar.cget("mode") != "determinate":
                ui.pBar.configure(mode="determinate")
            
        ui._pVar.set(ui.pValue)
        
        ui._logVar.set(cleanStr(truncateStr(ui.logStr)))
        ui._etaVar.set(cleanStr(truncateStr(ui.etaStr)))
        ui._elapsedVar.set(cleanStr(truncateStr(ui.elapsedStr)))
        ui._memVar.set(cleanStr(truncateStr(ui.memStr)))
        ui.root.title(cleanStr(truncateStr(ui.windowTitleStr)))

        #run tk update loop
        ui.root.update_idletasks()
        ui.root.update()
        #limits to 120fps
        time.sleep(0.00833)