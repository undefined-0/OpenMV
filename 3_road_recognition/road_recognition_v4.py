# 此py中sensor.snapshot()方法传回img（是一个数组）
# 意图通过对数组中数据处理后进行扫描（详见文档：中期问题及解答.md）来实现任务要求。
# 基于v3更改为了更为简单的算法

THRESHOLD = (50,255) # 此阈值为白色部分
import sensor, image, time, json
from pyb import LED
from pid import PID
rho_pid = PID(p=0.4, i=0)
theta_pid = PID(p=0.001, i=0)

red_led   = LED(1)
green_led = LED(2)
blue_led  = LED(3)

red_led.off()
green_led.off()
blue_led.off()

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQQVGA) # 80x60 (4,800 pixels) - O(N^2) max = 2,3040,000.
#sensor.set_windowing([0,20,80,40])
sensor.skip_frames(time = 2000)     # warning: If you use QQVGA it may take seconds
clock = time.clock()                # to process a frame sometimes.

while(True):
    clock.tick()
    img = sensor.snapshot().binary([THRESHOLD]) # 截取一张图片，然后对图片进行阈值分割（二值化，将阈值内所有像素设置为白色，阈值外所有像素设置为黑色）。
    # THRESHOLD传递的值是此文件最开始设置的阈值
    # 通过在嵌套for循环中使用image.get_pixel(x, y)方法来获取每一个像素点的值
    # 每隔5行遍历5行
    for start_row in range(0, 60, 10):  # 外层循环，以10为步长遍历行
        for row in range(start_row, min(start_row + 5, 60)):  # 次外层循环，遍历接下来的5行
            for col_1 in range(80):  # 最内层循环，遍历每一列
                if (img.get_pixel(col_1-1,row) == 255) & \
                (img.get_pixel(col_1,row) == 255) & \
                (img.get_pixel(col_1+1,row) == 255) & \
                (img.get_pixel(col_1+2,row) == 0) & \
                (img.get_pixel(col_1+3,row) == 0) & \
                (img.get_pixel(col_1+4,row) == 0) :
                    x1 = col_1+3
                    for col_2 in range(col_1+3,80):
                        if (img.get_pixel(col_2-1,row) == 255) & \
                        (img.get_pixel(col_2,row) == 255) & \
                        (img.get_pixel(col_2+1,row) == 255) & \
                        (img.get_pixel(col_2+2,row) == 0) & \
                        (img.get_pixel(col_2+3,row) == 0) & \
                        (img.get_pixel(col_2+4,row) == 0) :
                            x2 = col_2+3
                            img.set_pixel(round((x1+x2)/2),row,(255,0,0))
     #print(clock.fps())
