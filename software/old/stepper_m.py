import machine
import utime

def step():

    pins = [
        machine.Pin(0,machine.Pin.OUT),
        machine.Pin(1,machine.Pin.OUT),
        machine.Pin(2,machine.Pin.OUT),
        machine.Pin(3,machine.Pin.OUT)
    ]

    step_seq = [
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [0,0,0,1]
    ]

    for step in step_seq:
        for i in range(len(pins)):
            pins[i].value(step[i])
            utime.sleep(0.001)
