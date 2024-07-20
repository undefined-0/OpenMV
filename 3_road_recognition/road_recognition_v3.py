# 此py中sensor.snapshot()方法传回img（是一个数组）
# 意图通过对数组中数据处理后进行扫描（详见文档：中期问题及解答.md）来实现任务要求。

THRESHOLD = (32, 100, -32, 15, -25, 22) # 此阈值为白色部分
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
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQQVGA) # 80x60 (4,800 pixels) - O(N^2) max = 2,3040,000.
#sensor.set_windowing([0,20,80,40])
sensor.skip_frames(time = 2000)     # warning: If you use QQVGA it may take seconds
clock = time.clock()                # to process a frame sometimes.

while(True):
    clock.tick()
    img = sensor.snapshot().binary([THRESHOLD]) # 截取一张图片，然后对图片进行阈值分割（二值化，将阈值内所有像素设置为白色，阈值外所有像素设置为黑色）。
    # THRESHOLD传递的值是此文件最开始设置的阈值
    # 通过在嵌套for循环中使用image.get_pixel(x, y)方法来获取每一个像素点的值
    # 每隔5行遍历一行
    # 假设img是一个已经定义好的80列，60行的二维数组

    # 使用嵌套for循环遍历img数组，每隔5行遍历5行
    for start_row in range(0, 60, 10):  # 外层循环，以5为步长遍历行
        for row in range(start_row, min(start_row + 5, 60)):  # 次外层循环，遍历接下来的5行
            flag = 0 # 用以检测是第几次扫描到黑色像素点
            x1_start = 0
            x1_end = 0
            x2_start = 0
            x2_end = 0
            for col in range(80):  # 最内层循环，遍历每一列
                pixel_tuple = img.get_pixel(row, col) #将当前行列的像素值元组传给pixel_tuple
                if pixel_tuple == (0,0,0): # 黑
                    flag += 1
                    if flag == 1: # 扫描到的是第一根黑色直线上的第一个黑色像素点
                        x1_start = col # 记录下扫到的第一个黑色像素点的列值
                        x1_end = x1_start
                    else: # 不是第一次扫描到黑色像素点
                        x1_start += 1 # 没扫描到白色，黑色的宽度就一直自增
                elif (pixel_tuple == (255,255,255)) & (flag != 0) & ((x1_end-x1_start)>3): # 若当前白色是扫描到黑色（且黑色宽度大于3个像素）后再次扫描到的白色，而非一行刚开始时就扫描到的白色，那么就记录下x1的值
                    x1 = (x1_start + x1_end) / 2
                    flag = 0
                    # continue

                if pixel_tuple == (0,0,0): # 黑
                    flag += 1
                    if flag == 1: # 扫描到的是第二根黑色直线上的第一个黑色像素点
                        x2_start = col # 记录下扫到的第一个黑色像素点的列值
                        x1_end = x2_start
                    else: # 不是第一次扫描到黑色像素点
                        x2_start += 1 # 没扫描到白色，黑色的宽度就一直自增
                elif (pixel_tuple == (255,255,255)) & (flag != 0) & ((x2_end-x2_start)>3): # 若当前白色是扫描到黑色（且黑色宽度大于3个像素）后再次扫描到的白色，而非一行刚开始时就扫描到的白色，那么就记录下x2的值
                    x2 = (x2_start + x1_end) / 2

                    # 若两根线上的黑点都已检测到，则画出该列两个黑点的中心点
                    x_middle = (x1+x2)/2
                    img.draw_line(int(x_middle), int(col), int(x_middle), int(col), color=(255, 0, 0), thickness=2)




    #print(clock.fps())
