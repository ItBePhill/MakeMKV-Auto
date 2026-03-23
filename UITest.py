import UIV2
import time

updater:UIV2.Updater, ui:UIV2.UI = UIV2.Setup("Test", "Test Sutitle", "This is a Test", i, 100, 10)

for i in range(0,100, 10):
    time.sleep(1)
    updater
        
