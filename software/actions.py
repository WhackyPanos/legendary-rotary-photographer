### "Legendary Rotary Photographer"
# Photogrammetry turntable for 3D scanning & cinematic item shots
# Dept. of PEM, Semester 9, Mechatronics Project 2021
# by Hristos Birmpoutsakis & Panos Skoulaxinos
# https://github.com/WhackyPanos/legendary-rotary-photographer
#
### Creative Commons License (CC)
# Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
# https://creativecommons.org/licenses/by-sa/4.0/

from machine import Pin, I2C
import machine
import utime
from stepper import STEPPER
from pico_i2c_lcd import I2cLcd
from config import *
from rotary_irq_rp2 import RotaryIRQ

# Initialize components
stepper = STEPPER(motor_config)
i2c = I2C(0, sda=machine.Pin(lcd_config['sda']), scl=machine.Pin(lcd_config['scl']), freq=400000)
I2C_ADDR=i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
okBtn = machine.Pin(btnPin, machine.Pin.IN, machine.Pin.PULL_DOWN)
takePic = machine.Pin(npnPin, machine.Pin.OUT)

r = RotaryIRQ(encoder_config['clk'],
              encoder_config['dt'],
              encoder_config['min_val'],
              encoder_config['max_val'],
              encoder_config['reverse'],
              encoder_config['range_mode'],
              encoder_config['pull_up'])

def interrupt_handler(i):
    global irpt
    irpt = True

okBtn.irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)

def splash():
    # splash screen on bootup
    lcd.clear()
    lcd.putstr("Photogrammetry")
    lcd.move_to(0,1)
    lcd.putstr("SW v" + str(ver))
    utime.sleep_ms(2000)

def menu():
    # main menu
    lcd.clear()
    lcd.putstr("Photogrammetry")
    r.reset()
    r.set(value=1, min_val=1, max_val=2)
    old_val = r.value()
    lcd.move_to(0,1)
    lcd.putstr(">Scan  Cinematic")

    while okBtn.value()==0:
        new_val = r.value()

        if old_val != new_val:
            old_val = new_val
            if new_val==1:
                lcd.move_to(0,1)
                lcd.putstr(">Scan  Cinematic")

            elif new_val==2:
                lcd.move_to(0,1)
                lcd.putstr("Scan  >Cinematic")
        
        utime.sleep_ms(10)
    
    beep()

    if new_val==1:
        # scan submenu
        utime.sleep_ms(20)
        lcd.clear()
        lcd.putstr("Scan mode")
        lcd.move_to(0,1)
        r.reset()
        r.set(value=1, min_val=0, max_val=18)
        val_old = r.value()
        lcd.putstr("Set deg: " + str(val_old *5)+chr(223))
        while okBtn.value()==0:
            val_new = r.value()
            if val_old != val_new:
                val_old = val_new
                lcd.move_to(0,1)

                if val_new == 0:
                    lcd.putstr("Set deg: EXIT")
                else:
                    lcd.putstr("Set deg: " + str(val_new *5)+chr(223)+"   ")

                    #(char)223

            utime.sleep_ms(10)
        beep()


        if val_new==0:
            return
        else:
            lcd.clear()
            lcd.putstr("Select mode")
            r.reset()
            r.set(value=1,min_val=1, max_val=2,range_mode=RotaryIRQ.RANGE_BOUNDED)
            old_val = r.value()
            lcd.move_to(0,1)
            lcd.putstr(" >Auto    Manual")

            while okBtn.value()==0:
                new_val = r.value()

                if old_val != new_val:
                    old_val = new_val
                    if new_val==1:
                        lcd.move_to(0,1)
                        lcd.putstr(" >Auto    Manual")

                    elif new_val==2:
                        lcd.move_to(0,1)
                        lcd.putstr(" Auto    >Manual")
                utime.sleep_ms(10)
            beep()

            if new_val ==1: # Auto mode
                scan(_step= (val_new*5*motor_config['number_of_steps']) /360)
            elif new_val ==2: # Manual mode
                scan(_step= (val_new*5*motor_config['number_of_steps']) /360, man=True)

            return

    elif new_val==2:
        # cinematic submenu
        utime.sleep_ms(100)
        lcd.clear()
        lcd.putstr("Cinematic mode")
        lcd.move_to(0,1)
        lcd.putstr("Set turns: ")
        r.reset()
        r.set(min_val=0, max_val=21, range_mode=RotaryIRQ.RANGE_WRAP)
        val_old = r.value()

        while okBtn.value()==0:
            val_new = r.value()
            if val_old != val_new:
                val_old = val_new
                if val_new == 0:
                    lcd.move_to(0,1)
                    lcd.putstr("Set turns: EXIT ")

                elif val_new == 21:
                    lcd.move_to(0,1)
                    lcd.putstr("Set turns: Inf ")

                else:
                    lcd.move_to(0,1)
                    lcd.putstr("Set turns: " + str(val_new)+"   ")

            utime.sleep_ms(10)
        beep()

        if val_new==0:
            return
        elif val_new==21:
            cinematic(turns=-1)
        else:
            cinematic(turns=val_new)

def scan(_step, man=False):
# works like a charm
    curStep = 0


    while curStep < motor_config['number_of_steps']:
        lcd.clear()
        lcd.putstr("Rotating... ")
        if (motor_config['number_of_steps'] - curStep) < _step:
            _step = motor_config['number_of_steps'] - curStep
        lcd.move_to(0,1)
        lcd.putstr("Deg: " + str((curStep/2048) * 360)+ chr(223))
        stepper.step(_step,hold=False)
        curStep += _step
        utime.sleep_ms(1000)

        if man: # Manual mode
            lcd.clear()
            lcd.putstr("Take photo!")
            lcd.move_to(0,1)
            lcd.putstr("Deg:" + str((curStep/2048) * 360) + chr(223) + " Next?")
            beep(tone='next')
            while okBtn.value()==0:
                pass
            beep()
        else: # Auto mode
            takePic.value(1)
            utime.sleep_ms(200)
            takePic.value(0)
            utime.sleep_ms(1500) # wait 1.5sec for picture

    lcd.clear()
    lcd.putstr("Scanning done")
    lcd.move_to(0,1)
    lcd.putstr("OK for menu")
    beep(tone='done')

    while okBtn.value()==0:
        pass
    beep()

def cinematic(turns=-1):
    lcd.clear()
    lcd.putstr("Cinematic...")
    if turns == -1:
        lcd.move_to(0,1)
        lcd.putstr("OK to cancel")
        global irpt
        irpt = False
        while not irpt:
            stepper.step(2048/16,speed=motor_config['cinematic_speed']/2,hold=False)
        irpt = False

    else:
        tot_turns=turns
        while turns != 0:
            lcd.move_to(0,1)
            lcd.putstr("Turn " + str(tot_turns - turns) + "/" + str(tot_turns))
            turns -= 1
            stepper.step(2048,speed=motor_config['cinematic_speed']/2,hold=False)
    lcd.clear()
    lcd.putstr("Complete")
    lcd.move_to(0,1)
    lcd.putstr("OK for menu")
    beep(tone='done')

    while okBtn.value()==0:
        pass
    beep()

def beep(pin=spkrPin, tone='beep'):
    buzzer = machine.PWM(machine.Pin(pin))

    if tone=='beep':
        buzzer.freq(800)
        buzzer.duty_u16(12000)
        utime.sleep_ms(100)
        buzzer.duty_u16(0)

    elif tone=='next':
        buzzer.freq(800)
        buzzer.duty_u16(12000)
        utime.sleep_ms(100)
        buzzer.duty_u16(0)
        utime.sleep_ms(200)
        buzzer.freq(800)
        buzzer.duty_u16(12000)
        utime.sleep_ms(100)
        buzzer.duty_u16(0)

    elif tone=='done':
        slp = 250

        buzzer.freq(600)
        buzzer.duty_u16(12000)
        utime.sleep_ms(slp)
        buzzer.freq(1200)
        utime.sleep_ms(slp)
        buzzer.freq(1800)
        utime.sleep_ms(slp)
        buzzer.duty_u16(0)

    elif tone == 'error':
        buzzer.freq(300)
        buzzer.duty_u16(12000)
        utime.sleep_ms(300)
        buzzer.duty_u16(0)

def error(errorStr="Resetting in 5"):
    lcd.clear()
    lcd.putstr("Error occurred!")
    lcd.move_to(0,1)
    lcd.putstr(errorStr)
    beep(tone='error')
    utime.sleep_ms(5000)
    machine.reset()
