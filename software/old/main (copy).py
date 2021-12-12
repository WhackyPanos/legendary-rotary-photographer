import machine
import utime
from stepper import STEPPER
from LCD import CharLCD
from rotary_irq_rp2 import RotaryIRQ
from config import *

lcd.clear()
lcd.message("Photogrammetry", 2)
lcd.set_line(1)
lcd.message("Set deg: 00",2)
val_old = r.value()

while True:
    val_new = r.value()
    if val_old != val_new:
        val_old = val_new
        lcd.set_line(1)
        lcd.message("Set deg: " + str(val_new *10), 2)
    if okBtn.value()==1:
        deg = val_new*10
        segment = deg/360
        _step = 2048* segment
        curStep =0
        lcd.clear()
        lcd.message("Scanning...")
        lcd.set_line(1)
        lcd.message("Deg: 0.0")

        while curStep < 2048:
            stepper.step(_step)
            curStep += _step
            lcd.set_line(1)
            lcd.message("Deg: " + str((curStep/2048) * 360))
            utime.sleep_ms(1000)
