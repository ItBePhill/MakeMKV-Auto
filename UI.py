from tkinter import *
from tkinter import ttk
root = Tk()
root.title("MakeMKV-Auto")
root.minsize(700,100)
title = ttk.Label(text = "Guardians of The Galaxy - Bluray").grid(row=0,column=0,sticky=NW)
subtitle =  ttk.Label(text = "Saving 1 title to: /path/to/folder/GUARDIANS_OF_THE_GALAXY").grid(row=1,column=0,sticky=NW)
prg = ttk.Progressbar(value=40, length=600).grid(row=2,column=0, sticky=W)
Log = ttk.Label(text = "Operation Completed Successfully").grid()
root.mainloop()