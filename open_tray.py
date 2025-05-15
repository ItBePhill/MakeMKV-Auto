#script taken and edited from: https://gist.github.com/TakesTheBiscuit/a2e3d36c1d20731821fdb41b3831406e#file-open_and_close_cd_tray-py

from platform import system as platform_name
from os import system
import ctypes
def Run(driveLetter):
    platforms_dictionary = {
    "Windows": {                              
                "open" : f'ctypes.windll.WINMM.mciSendStringW(u"open {driveLetter}: type CDAudio alias {driveLetter}_drive", None, 0, None); ctypes.windll.WINMM.mciSendStringW(u"set {driveLetter}_drive door open", None, 0, None)',
                "close": f'ctypes.windll.WINMM.mciSendStringW(u"open {driveLetter}: type CDAudio alias {driveLetter}_drive", None, 0, None); ctypes.windll.WINMM.mciSendStringW(u"set {driveLetter}_drive door closed", None, 0, None)'
               },
    "Darwin":  {
                "open" : 'system("drutil tray open")',
                "close": 'system("drutil tray closed")'
               },
    "Linux":   {
                "open" : 'system("eject cdrom")',
                "close": 'system("eject -t cdrom")'
               },
    "NetBSD":  {
                "open" : 'system("eject cd")',
                "close": 'system("eject -t cd")'
               },
    "FreeBSD": {
                "open" : 'system("sudo cdcontrol eject")',
                "close": 'system("sudo cdcontrol close")'
               }
}
    if platform_name() in platforms_dictionary:
        print('Opening Disc Tray... ')
        exec(platforms_dictionary[platform_name()]["open"])
    else:
        print("Sorry, no OS found")