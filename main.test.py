import time
#this script is just for testing the ui
#will simulate stdout for the real program
print(f"INF0|Test Disc")
print(f"INF1|1:00:00")
print(f"INF2|/path/to/output/TEST_DISC")
for i in range(0,6000, 50):
    print(f"MSG|This is a test message {i}")
    print(f"PG|{i}/6000")
    time.sleep(.15)