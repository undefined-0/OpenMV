# v2 使用angle方法控制舵机

import time
from pyb import Servo

s1 = Servo(1) # P7
s2 = Servo(2) # P8

move_time = 1000 # 1000ms

while(True):
    # P7连接的舵机
    s1.angle(90, move_time)
    time.sleep(2)
    s1.angle(-90, move_time)
    time.sleep(2)

    # P8连接的舵机
