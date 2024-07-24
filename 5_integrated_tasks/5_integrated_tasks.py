import sensor, image, time, os, tf, uos, gc
from pyb import Servo     #调用库

s1=Servo(1)              #P7
s2=Servo(2)              #P8

red_threshold  = (0, 98, 37, 127, -32, 89)              #红色色素块
green_threshold  =(34, 100, -90, -14, 24, 66)           #绿色色素块
blue_threshold = (19, 71, 15, 74, -110, -65)            #蓝色色素块

move_time = 500 # 500ms

def servo_reset(): # 舵机初始化，摄像头正对前方
    s1.angle(0, move_time)
    s2.angle(0, move_time)

def servo_shake(): # 摇头
    s1.angle(-30, move_time)
    time.sleep(1)
    s1.angle(30, move_time)
    time.sleep(1)

def servo_nod(): # 点头
    s2.angle(-30, move_time)
    time.sleep(1)
    s2.angle(30, move_time)
    time.sleep(1)

sensor.reset()                         # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)    # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QQQVGA)    # Set frame size to QVGA,80*60
sensor.set_windowing((240, 240))       # Set 240x240 window.
sensor.skip_frames(time=2000)          # Let the camera adjust.
sensor.set_auto_whitebal(False)        # 关自动白平衡
sensor.set_auto_gain(False)            # 颜色跟踪必须关闭自动增益

net = None
labels = None

try:
    # load the model, alloc the model file on the heap if we have at least 64K free after loading
    net = tf.load("trained.tflite", load_to_fb=uos.stat('trained.tflite')[6] > (gc.mem_free() - (64*1024)))
except Exception as e:
    print(e)
    raise Exception('Failed to load "trained.tflite", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')
try:
    labels = [line.rstrip('\n') for line in open("labels.txt")]
except Exception as e:
    raise Exception('Failed to load "labels.txt", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

clock = time.clock()

while(True):
    servo_reset()
    time.sleep(1)
    clock.tick()
    img = sensor.snapshot()
     # 默认设置只进行一次检测...可以根据需要更改设置以搜索整个图像...
    for obj in net.classify(img, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5):
        # 打印检测到的对象的边界框
        # print("**********\nPredictions at [x=%d,y=%d,w=%d,h=%d]" % obj.rect())
        # 在图像上绘制边界框
        # img.draw_rectangle(obj.rect())
        # 将标签和置信度值组合成一个元组列表
        predictions_list = list(zip(labels, obj.output()))

        # 初始化最大值和最大值的序号
        max_value = predictions_list[0][1]
        max_index = 0

        # 遍历predictions_list以找到最大值及其序号
        for i, (label, value) in enumerate(predictions_list):
            if value > max_value:
                max_value = value
                max_index = i

        if (max_value > 0.99):
            # 输出最大值及其序号
            print("该数字最有可能是：%d\n概率为：%f\n" % (max_index, max_value))
            if(max_index > 3): # 识别到的数字是4-9
                for i in range(max_index):
                    servo_shake()
                servo_reset()
                continue # 跳出本轮while(True)

            elif  (max_index == 1): # 识别到数字1，让舵机点头1次
                for i in range(max_index):
                    servo_nod()
                time.sleep(1)
                servo_reset()
                # 间隔2秒，识别颜色是否为绿色
                img = sensor.snapshot()
                blob = img.find_blobs([red_threshold], pixels_threshold=200, area_threshold=200)
                if blob:  # 如果找到红色色素块，舵机点头两次
                    #img.draw_rectangle(blob.rect()) #用矩形标记出目标颜色区域
                    #img.draw_cross(blob.cx(), blob.cy()) #在目标颜色区域的中心画十字形标记
                    print("识别到红色\n")
                    servo_nod()
                    servo_nod()
                    time.sleep(1)
                else:
                    # 舵机摇头两次
                    print("未识别到红色\n")
                    servo_shake()
                    servo_shake()
                    time.sleep(1)
                continue

            elif  (max_index == 2): # 识别到数字2，让舵机点头2次
                for i in range(max_index):
                    servo_nod()
                time.sleep(1)
                servo_reset()
                # 间隔2秒，识别颜色是否为绿色
                img = sensor.snapshot()
                blob = img.find_blobs([green_threshold], pixels_threshold=200, area_threshold=200)
                if blob:  # 如果找到绿色色素块，舵机点头两次
                    # img.draw_rectangle(blob.rect()) #用矩形标记出目标颜色区域
                    # img.draw_cross(blob.cx(), blob.cy()) #在目标颜色区域的中心画十字形标记
                    print("识别到绿色\n")
                    servo_nod()
                    servo_nod()
                    time.sleep(1)
                else:
                    # 舵机摇头两次
                    print("未识别到绿色\n")
                    servo_shake()
                    servo_shake()
                    time.sleep(1)
                continue

            elif  (max_index == 3): # 识别到数字3，让舵机点头3次
                for i in range(max_index):
                    servo_nod()
                time.sleep(1)
                servo_reset()
                # 间隔2秒，识别颜色是否为蓝色
                img = sensor.snapshot()
                blob = img.find_blobs([blue_threshold], pixels_threshold=200, area_threshold=200)
                if blob:  # 如果找到蓝色色素块，舵机点头两次
                    # img.draw_rectangle(blob.rect()) #用矩形标记出目标颜色区域
                    # img.draw_cross(blob.cx(), blob.cy()) #在目标颜色区域的中心画十字形标记
                    print("识别到蓝色\n")
                    servo_nod()
                    servo_nod()
                    time.sleep(1)
                else:
                    # 舵机摇头两次
                    print("未识别到蓝色\n")
                    servo_shake()
                    servo_shake()
                    time.sleep(1)
                continue

        else: # 若没有识别到确切数字则开启新一轮while(True)
            continue
