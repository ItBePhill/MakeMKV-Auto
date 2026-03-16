from tkinter import *
import ttkbootstrap as ttk
from tkinter import font
root = ttk.Window(themename='darkly', iconphoto=None)
root.title("MakeMKV-Auto")
Width = 500
Height = 100
root.minsize(Width,Height)
root.maxsize(Width,Height)
titleFont = font.Font(root=root, name="title", family="Segoe UI", size=12, weight='bold')
subtitleFont = font.Font(root=root, name="subtitle", family="Segoe UI", size=9, weight='normal')
defaultFont = font.Font(root=root, name="default", family="Segoe UI", size=9, weight='normal')
frame = ttk.Frame(root)
frame.pack(anchor=W, padx=10, pady=10)

otherFrame = ttk.Frame(frame)
otherFrame.grid(row=1, sticky=SW, pady=5)
titleframe = ttk.Frame(frame)
titleframe.grid(row=0, sticky=NW, pady=5)
title = ttk.Label(titleframe, text = "Guardians of The Galaxy - Bluray", font = titleFont)
title.grid(sticky=NW, row=0)
subtitle =  ttk.Label(titleframe, text = "Saving 1 of 1 title(s) to: /path/to/folder/GUARDIANS_OF_THE_GALAXY", font=subtitleFont)
subtitle.grid(stick=NW, row=1)

prgbar = ttk.Progressbar(otherFrame, value=40, length=400)
prgbar.grid(sticky=W, row=2, pady=2)
log = ttk.Label(otherFrame, text = "Operation Completed Successfully", font=defaultFont)

log.grid(sticky=W, row=3, pady=2)
eta = ttk.Label(otherFrame, text="ETA: 10:47", font=defaultFont)
eta.grid(sticky=E, row=3)
percent = ttk.Label(otherFrame, text="40%", font=defaultFont)

root.mainloop()