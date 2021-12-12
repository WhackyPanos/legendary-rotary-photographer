### "Legendary Rotary Photographer"
# Photogrammetry turntable for 3D scanning & cinematic item shots
# Dept. of PEM, Semester 9, Mechatronics Project 2021
# by Hristos Birmpoutsakis & Panos Skoulaxinos
# https://github.com/WhackyPanos/legendary-rotary-photographer
#
### Creative Commons License (CC)
# Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
# https://creativecommons.org/licenses/by-sa/4.0/


## Photogrammetry table configuration file
from rotary_irq_rp2 import RotaryIRQ

ver = 1.1

# ULN2003 Motor Driver
motor_config = {
    'In1':9,
    'In2':8,
    'In3':7,
    'In4':6,
    'number_of_steps': 1*32*64, # 1:1 final drive, 32 steps/rev, 64:1 internal gear ratio
    'max_speed': 5 # rpm
}

# Hitachi HD44780 16*2 character lcd
# lcd_config = {
#     'en':4, # Enable
#     'rs':5, # Register select
#     'd4':6,
#     'd5':7,
#     'd6':8,
#     'd7':9
# }

lcd_config = {
    'sda':4,
    'scl':5
    #i2c0
}

btnPin = 11

encoder_config = {
    'clk':12,
    'dt':13,
    'min_val':1,
    'max_val':9,
    'reverse':True,
    'range_mode':RotaryIRQ.RANGE_BOUNDED,
    'pull_up':True
}

npnPin = 13

spkrPin = 20
