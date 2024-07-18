# 此py中sensor.snapshot()方法传回img（是一个数组）
# 意图通过对数组中数据处理后进行扫描（详见文档：中期问题及解答.md）来实现任务要求。

THRESHOLD = (0, 31, -9, 8, -15, 6) # Grayscale threshold for dark things...
import sensor, image, time, json
from pyb import LED
from pid import PID
rho_pid = PID(p=0.4, i=0)
theta_pid = PID(p=0.001, i=0)

red_led   = LED(1)
green_led = LED(2)
blue_led  = LED(3)

LED(1).off()
LED(2).off()
LED(3).off()

sensor.reset()
#sensor.set_vflip(True)
#sensor.set_hmirror(True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQQVGA) # 80x60 (4,800 pixels) - O(N^2) max = 2,3040,000.
#sensor.set_windowing([0,20,80,40])
sensor.skip_frames(time = 2000)     # warning: If you use QQVGA it may take seconds
clock = time.clock()                # to process a frame sometimes.

while(True):
    clock.tick()
    img = sensor.snapshot().binary([THRESHOLD])
    line = img.get_regression([(100,100)], robust = True)
    if (line):
        rho_err = abs(line.rho())-img.width()/2 #计算所得的直线与图像中央的偏移距离。
        if line.theta()>90:
            theta_err = line.theta()-180
        else:
            theta_err = line.theta() #进行角度转换，往右偏则角度为正值，往左偏则角度为负值
        img.draw_line(line.line(), color =(255, 0, 0))
        if line.magnitude()>8: #拟合效果比较好
            rho_output = rho_pid.get_pid(rho_err,1)
            #theta_output = theta_pid.get_pid(theta_err,1)
            #print("偏移角度:",theta_output)
            if rho_output>6:
                print("-----------------")
                print("偏移距离:",rho_output)
                print("偏右")
                red_led.off()
                blue_led.on()
                green_led.off()
            elif rho_output<-6:
                print("-----------------")
                print("偏移距离:",rho_output)
                print("偏左")
                red_led.on()
                blue_led.off()
                green_led.off()
            else:
                print("无偏移")
                red_led.off()
                blue_led.off()
                green_led.off()
        else: #拟合效果不好
            red_led.off()
            blue_led.off()
            green_led.off()
    else: #视野中没有发现线
        red_led.off()
        blue_led.off()
        green_led.on()
        pass
    #print(clock.fps())
