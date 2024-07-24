# 测试舵机的“摇头”
from pyb import Servo
import time
s1=Servo(1)
s2=Servo(2)
move_time = 500 # 500ms

while(True):
    # P7连接的舵机（控制左右）
    s1.angle(-30, move_time) 
    time.sleep(0.5)
    s1.angle(30, move_time)
    time.sleep(0.5)