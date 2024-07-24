# v2 使用角度方法控制舵机复位（最终选择此方法）

import time
from pyb import Servo

s1 = Servo(1) # P7
s2 = Servo(2) # P8
move_time = 1000 # 1000ms

    # P7连接的舵机
s1.angle(0, move_time)
    # P8连接的舵机
s2.angle(0, move_time)
while(True):
    pass