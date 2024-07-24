# v1 使用PWM+延时控制舵机复位

import time
from pyb import Servo

s1 = Servo(1) # P7
s2 = Servo(2) # P8

while(True):
        for i in range(2000):
    # P7连接的舵机
            s1.pulse_width(1500)
    # P8连接的舵机
            s2.pulse_width(1500)
            print("set")
            time.sleep_ms(2)