import time
import os
import random
#this script is just for testing the ui
#will simulate stdout for the real program
#Name
print(f"INF0|Test Disc")
#Length
print(f"INF1|1:00:00", )
#path
print(f"INF2|/path/to/output/TEST_DISC")
#
print(f"INF3|1")
print("MSG|oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
max=9999
print(f"TINF|1")
for i in range(0,max, 20):
    
    print(f"MSG|This is a test message {i}")
    print(f"PG|{i}/{max}")
    time.sleep(random.randint(0, 100)/100)
    