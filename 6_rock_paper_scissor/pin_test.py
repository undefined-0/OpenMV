# 测试P0、P1、P2引脚作普通IO口使用

from pyb import Pin

# 连接一个开关到Pin0，当开关闭合的时候，引脚置低。然后Pin1会点亮
pin0 = Pin('P0', Pin.IN, Pin.PULL_DOWN)
pin2 = Pin('P2', Pin.OUT_PP, Pin.PULL_NONE)

while(True):
    pin2.value(pin0.value())