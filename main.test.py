import time
import os
import random
#this script is just for testing the ui
#will simulate stdout for the real program
discname="Test Disc"
discpath="/path/to/output/TEST_DISC"
disclength="1:00:00"
print("ST|Waiting for a disc...")
time.sleep(5)
#Name
print(f"INF0|{discname}")
#Length
print(f"INF1|{disclength}")
#path
print(f"INF2|{discpath}")
print(f"INF3|1")
print("MSG|This is a really long message for testing if the length of the subtitle is correct lorem ipsum doloret")
max=9999
print(f"TINF|1")
print(f"ST|Ripping {discname}")
for i in range(0,max, 20):
    
    print(f"MSG|This is a test message {i}")
    print(f"PG|{i}/{max}")
    time.sleep(random.randint(0, 100)/100)
    