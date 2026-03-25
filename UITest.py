import time
import threading
import UIV2
def run(max):
    global running
    i = 0
    while True:
        if UIV2.header.running and i <= max:
            UIV2.Update("Test", "Test Subtitle", f"Log: {i}", i, "100 MB", max)
            i+=10
            time.sleep(1)
        else:
            UIV2.Cancel()

def Start():
    max = 100
    UIV2.Init()
    UIV2.header.running = True
    thread = threading.Thread(target=run, args=[max], name="run")
    thread.start()
    while True:
        UIV2._TkUpdate()

Start()

        
