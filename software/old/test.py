import machine
import utime
from stepper import STEPPER

motor_config = {
    'In1':0,
    'In2':1,
    'In3':2,
    'In4':3,
    'number_of_steps': 2048,
    'max_speed': 9
}

stepper = STEPPER(motor_config)

while True:
    stepper.step(2048)
    utime.sleep_ms(1000)
    stepper.step(-200)
    utime.sleep_ms(1000)