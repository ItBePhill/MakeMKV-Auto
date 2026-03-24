import UIV2
import time
updater:UIV2.Updater
ui:UIV2.UI
max = 100
updater, ui = UIV2.Init()
running = True
def Stop(updater, ui):
    global running
    UIV2.Cancel(updater, ui)
    running = False
while True:
    ui.update()
    if running:
        for i in range(0,max+1, 10):
            time.sleep(1)
            ui.update()
            UIV2.Update(updater, ui, "Test", "Test Subtitle", f"Log: {i}", i, "100 MB", max)
        Stop(updater,ui)
        
