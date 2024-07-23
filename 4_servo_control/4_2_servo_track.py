import sensor, image, time

from pid import PID
from pyb import Servo

zuoyou_servo_P7=Servo(1)
shangxia_servo_P8=Servo(2)


red_threshold  = (0, 98, 37, 127, -32, 89) # 红色区域阈值

# zuoyou_pid = PID(p=0.06,i=0.1, imax=90) #脱机运行或者禁用图像传输，使用这个PID
# shangxia_pid = PID(p=0.05,i=0.05, imax=90) #脱机运行或者禁用图像传输，使用这个PID
zuoyou_pid = PID(p=0.10,d=0.01,i=0.02, imax=100)#在线调试使用这个PID
shangxia_pid = PID(p=0.09,d=0.01,i=0.02, imax=75)#在线调试使用这个PID
    #openmv脱机运行时帧率会提高，运行性能会有所改变，所以需要设置“在线联机调试”和“脱机运行”的两个参数

# 基本参数设置
sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # use RGB565.
sensor.set_framesize(sensor.QQVGA) # 160*120
sensor.skip_frames(10) # Let new settings take affect.
sensor.set_auto_whitebal(False) # 关自动白平衡
clock = time.clock()

# 找到视野中的最大红色块
'''
blob[2]：色块的外框的宽度w
blob[3]：色块的外框的高度h
'''
def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
    return max_blob


while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # Take a picture and return the image.
    blobs = img.find_blobs([red_threshold]) # 查找红色色块
    if blobs:
        max_blob = find_max(blobs)
        zuoyou_correct = img.width()/2-max_blob.cx()# 横轴方向上的修正参数（小于零代表目标在视野中偏右，大于零则代表目标在视野中偏左）
        shangxia_correct = img.height()/2-max_blob.cy() # 纵轴方向上的修正参数
        # print("zuoyou_correct: ", zuoyou_correct) #在参数调试窗口打印色块中心坐标与视野中心坐标的偏离值，便于调试与修正

        img.draw_rectangle(max_blob.rect()) #在色块外围四周处画框
        img.draw_cross(max_blob.cx(), max_blob.cy()) # 色块中心坐标处画十字

        zuoyou_output=zuoyou_pid.get_pid(zuoyou_correct,1)/2
        shangxia_output=shangxia_pid.get_pid(shangxia_correct,1)/2
        # print("zuoyou_output",zuoyou_output)                   #在参数调试窗口打印坐标值，便于调试与修正
        zuoyou_servo_P7.angle(zuoyou_servo_P7.angle()+zuoyou_output) # 输出横轴方向上的PWM波控制云台追踪色块标志
                                                        #openmv上P7为控制云台上舵机的输出引脚（摄像头左右移动）
        shangxia_servo_P8.angle(shangxia_servo_P8.angle()-shangxia_output) # 输出纵轴方向上的PWM波控制云台追踪色块标志
                                                            #openmv上P8为控制云台下舵机的输出引脚（摄像头上下移动）
