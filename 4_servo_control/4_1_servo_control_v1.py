# v1 使用PWM+延时控制舵机

import time
from pyb import Servo

s1 = Servo(1) # P7
s2 = Servo(2) # P8

while(True):
    # P7连接的舵机
    for i in range(2000):
        s1.pulse_width(500 + i) # 500~2500
        time.sleep_ms(2)
    for i in range(2000):
        s1.pulse_width(2499 - i) # 2499~499
        time.sleep_ms(2)

    # P8连接的舵机
    for i in range(2000):
        s2.pulse_width(500 + i) # 500~2500
        time.sleep_ms(2)
    for i in range(2000):
        s2.pulse_width(2499 - i) # 2499~499
        time.sleep_ms(2)
