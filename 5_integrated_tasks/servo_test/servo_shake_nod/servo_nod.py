# 测试舵机的“点头”
from pyb import Servo
import time

s1=Servo(1)
s2=Servo(2)
move_time = 500 # 500ms

while(True):
    # P8连接的舵机（控制上下）
    s2.angle(-30, move_time) 
    time.sleep(0.5)
    s2.angle(30, move_time)
    time.sleep(0.5)