# Source - https://stackoverflow.com/a/10019596
# Posted by Andrew Clark, modified by community. See post 'Timeline' for change history
# Retrieved 2026-03-17, License - CC BY-SA 4.0

import time
import sys

for i in range(5):
    print(i),
    sys.stdout.flush()
    time.sleep(1)
