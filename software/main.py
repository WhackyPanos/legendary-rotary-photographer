### "Legendary Rotary Photographer"
# Photogrammetry turntable for 3D scanning & cinematic item shots
# Dept. of PEM, Semester 9, Mechatronics Project 2021
# by Hristos Birmpoutsakis & Panos Skoulaxinos
# https://github.com/WhackyPanos/legendary-rotary-photographer
#
### Creative Commons License (CC)
# Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) 
# https://creativecommons.org/licenses/by-sa/4.0/

import machine
import utime
from actions import *

splash()

try:
    while True:
        menu()
except Exception as e:
    #print(e)
    error(str(e))