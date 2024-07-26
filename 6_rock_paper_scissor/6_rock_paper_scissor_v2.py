# v2
# 在v1的基础上，实现两两组队，通过串口通信来比赛。
# 赢的一方摆动舵机，输的闪烁红灯。
# 注：OpenMV的P4口为其TX，P5口为其RX

import sensor, image, time
from pyb import Pin, Servo, ExtInt, LED, Timer
from machine import UART
import json

MODE = True # 双人游戏时，选择True -> 我方使用按键输入；选择False -> 我方使用二维码输入
# 思路：类似于C/C++中的条件编译

uart = UART(3, 19200) # 使用UART(3)实例化一个19200波特率的串口

red_led   = LED(1)
green_led = LED(2)
blue_led  = LED(3)

# 关闭所有灯
red_led.off()
green_led.off()
blue_led.off()

s1=Servo(1)              # P7
s2=Servo(2)              # P8

move_time = 500 # 500ms

def servo_reset(): # 舵机初始化，摄像头正对前方
    s1.angle(0, move_time)
    s2.angle(0, move_time)

def servo_shake(): #舵机摇头
    s1.angle(-30, move_time)
    time.sleep(0.5)
    s1.angle(30, move_time)
    time.sleep(0.5)

def servo_nod(): # 舵机点头
    s2.angle(-30, move_time)
    time.sleep(0.5)
    s2.angle(30, move_time)
    time.sleep(0.5)

tim_red = Timer(2, freq=4)      # 使用定时器2创建定时器对象—以4Hz触发

def red_LED_flash(timer):       # 定时器中断回调函数
    red_led.toggle()

# 初始化传感器
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)
clock = time.clock()

# 定义游戏规则
rules = {
    'scissor': 'paper',
    'paper': 'rock',
    'rock': 'scissor'
}

# 初始化按键
pins = {
    'P_scissor': Pin('P0', Pin.IN, Pin.PULL_UP),  # scissor
    'P_rock': Pin('P1', Pin.IN, Pin.PULL_UP),  # rock
    'P_paper': Pin('P2', Pin.IN, Pin.PULL_UP)   # paper
}

# 舵机复位
servo_reset()
print("舵机复位完成，游戏开始\n")

# 游戏主循环
while True:
    clock.tick()
    img = sensor.snapshot()
    img.lens_corr(1.8)
    my_choice = None
    op_choice = None

    if MODE:
        # 检测按键输入
        for pin_name, pin in pins.items():
            if not pin.value(): # 如果按键被按下（IO口状态为低电平）
                time.sleep_ms(80) #等待80毫秒进行消抖
                if not pin.value(): # 如果按键仍为按下状态
                    my_choice = pin_name[2:]  # 去掉'P_'得到字符串
                    print("我方选择了：%s\n" % my_choice)
    else:
        # 检测二维码输入
        img = sensor.snapshot()
        for code in img.find_qrcodes():
            my_choice = code.payload().lower() # 获取二维码内容并转为全小写字母
            img.draw_rectangle(code.rect(), color=(255, 0, 0)) # 框选出二维码
            print("我方选择了：%s\n" % my_choice)

    if(my_choice):
        uart.write(str(my_choice)) # 强转为字符串
        time.sleep(1) # 等待1秒后再去检测对方选择
        if uart.any(): # 检测到我方已经做出选择后再去读取串口
            op_choice=uart.read().decode()
            print("对方选择了：%s\n" % op_choice)

    # 如果我和对方都做出了选择，判断输赢
    if my_choice and op_choice:
        if rules[my_choice] == op_choice: # 我方赢了
            red_led.off()
            tim_red.callback(None) # 失能能定时器中断，使LED不再闪烁
            print("我方赢了，舵机摆动\n")
            print("——————————————————————————————————————\n")
            servo_shake()
            servo_reset()

        elif rules[op_choice] == my_choice: # 对方赢了
            green_led.off()
            blue_led.off()
            tim_red.callback(red_LED_flash) # 使能定时器中断，将回调设置为red_LED_flash函数
            print("对方赢了，LED闪烁\n")
            print("——————————————————————————————————————\n")

        else: # 平局
            tim_red.callback(None) # 失能能定时器中断，使LED不再闪烁
            print("平局\n")
            print("——————————————————————————————————————\n")

    if((my_choice != None) & (op_choice == None)):
        print("对方未及时应答，本轮游戏结束，重新开始\n")
        print("——————————————————————————————————————\n")
