# 色块监测 例子
#
# 这个例子展示了如何通过find_blobs()函数来查找图像中的色块

import sensor, image, time, json
import time
from pyb import LED
from machine import UART
red_led   = LED(1)
green_led = LED(2)
blue_led  = LED(3)

# 颜色追踪的例子，一定要控制环境的光，保持光线是稳定的。
green_threshold   =  (0, 100, -128, 127, 30, 74)
red_threshold   =  (29, 68, 39, 127, 32, 65)
blue_threshold   =  (59, 82, -31, 6, -88, -26)
#设置绿色的阈值，括号里面的数值分别是L A B 的最大值和最小值（minL, maxL, minA,
# maxA, minB, maxB），LAB的值在图像左侧三个坐标图中选取。如果是灰度图，则只需
#设置（min, max）两个数字即可。

uart = UART(3, 115200)

sensor.reset() # 初始化摄像头
sensor.set_pixformat(sensor.RGB565) # 格式为 RGB565.
sensor.set_framesize(sensor.QQVGA) # 使用 QQVGA 速度快一些
sensor.skip_frames(time = 2000) # 跳过2000s，使新设置生效,并自动调节白平衡
sensor.set_auto_gain(False) # 关闭自动自动增益。默认开启的，在颜色识别中，一定要关闭白平衡。
sensor.set_auto_whitebal(False)
#关闭白平衡。白平衡是默认开启的，在颜色识别中，一定要关闭白平衡。
clock = time.clock() # 追踪帧率

while(True):
    time.sleep(1)
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # 从感光芯片获得一张图像

    blob_green = img.find_blobs([green_threshold])
    blob_red = img.find_blobs([red_threshold])
    blob_blue = img.find_blobs([blue_threshold])
    #find_blobs(thresholds, invert=False, roi=Auto),thresholds为颜色阈值，
    #是一个元组，需要用括号［ ］括起来。invert=1,反转颜色阈值，invert=False默认
    #不反转。roi设置颜色识别的视野区域，roi是一个元组， roi = (x, y, w, h)，代表
    #从左上顶点(x,y)开始的宽为w高为h的矩形区域，roi不设置的话默认为整个图像视野。
    #这个函数返回一个列表，[0]代表识别到的目标颜色区域左上顶点的x坐标，［1］代表
    #左上顶点y坐标，［2］代表目标区域的宽，［3］代表目标区域的高，［4］代表目标
    #区域像素点的个数，［5］代表目标区域的中心点x坐标，［6］代表目标区域中心点y坐标，
    #［7］代表目标颜色区域的旋转角度（是弧度值，浮点型，列表其他元素是整型），
    #［8］代表与此目标区域交叉的目标个数，［9］代表颜色的编号（它可以用来分辨这个
    #区域是用哪个颜色阈值threshold识别出来的）。
    if blob_green:
    #如果找到了目标颜色
        red_led.off()
        blue_led.off()
        green_led.on()
        data_green=[]
        for b in blob_green:
        #迭代找到的目标颜色区域
            # Draw a rect around the blob.
            img.draw_rectangle(b[0:4]) # rect
            #用矩形标记出目标颜色区域
            img.draw_cross(b[5], b[6]) # cx, cy
            #在目标颜色区域的中心画十字形标记
            data_green.append((b.cx(),b.cy())) # cx, cy
            #存储中心点坐标

        data_green_out = json.dumps(set(data_green))
        uart.write(data_green_out +'\n')
        print('coordinate_green:',data_green_out)
    else:
        print("not found green patch!")


    if blob_red:
    #如果找到了目标颜色
        red_led.on()
        blue_led.off()
        green_led.off()
        data_red=[]
        for b in blob_red:
        #迭代找到的目标颜色区域
            # Draw a rect around the blob.
            img.draw_rectangle(b[0:4]) # rect
            #用矩形标记出目标颜色区域
            img.draw_cross(b[5], b[6]) # cx, cy
            #在目标颜色区域的中心画十字形标记
            data_red.append((b.cx(),b.cy())) # cx, cy
            #存储中心点坐标

        data_red_out = json.dumps(set(data_red))
        uart.write(data_red_out +'\n')
        print('coordinate_red:',data_red_out)
    else:
        print("not found red patch!")

    if blob_blue:
    #如果找到了目标颜色
        red_led.off()
        blue_led.on()
        green_led.off()
        data_blue=[]
        for b in blob_blue:
        #迭代找到的目标颜色区域
            # Draw a rect around the blob.
            img.draw_rectangle(b[0:4]) # rect
            #用矩形标记出目标颜色区域
            img.draw_cross(b[5], b[6]) # cx, cy
            #在目标颜色区域的中心画十字形标记
            data_blue.append((b.cx(),b.cy())) # cx, cy
            #存储中心点坐标

        data_blue_out = json.dumps(set(data_blue))
        uart.write(data_blue_out +'\n')
        print('coordinate_blue:',data_blue_out)
    else:
        print("not found blue patch!")
    print(clock.fps()) # 注意: 你的OpenMV连到电脑后帧率大概为原来的一半
    #如果断开电脑，帧率会增加