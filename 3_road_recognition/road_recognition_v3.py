# ��py��sensor.snapshot()��������img����һ�����飩
# ��ͼͨ�������������ݴ�������ɨ�裨����ĵ����������⼰���.md����ʵ������Ҫ��

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
        rho_err = abs(line.rho())-img.width()/2 #�������õ�ֱ����ͼ�������ƫ�ƾ��롣
        if line.theta()>90:
            theta_err = line.theta()-180
        else:
            theta_err = line.theta() #���нǶ�ת��������ƫ��Ƕ�Ϊ��ֵ������ƫ��Ƕ�Ϊ��ֵ
        img.draw_line(line.line(), color =(255, 0, 0))
        if line.magnitude()>8: #���Ч���ȽϺ�
            rho_output = rho_pid.get_pid(rho_err,1)
            #theta_output = theta_pid.get_pid(theta_err,1)
            #print("ƫ�ƽǶ�:",theta_output)
            if rho_output>6:
                print("-----------------")
                print("ƫ�ƾ���:",rho_output)
                print("ƫ��")
                red_led.off()
                blue_led.on()
                green_led.off()
            elif rho_output<-6:
                print("-----------------")
                print("ƫ�ƾ���:",rho_output)
                print("ƫ��")
                red_led.on()
                blue_led.off()
                green_led.off()
            else:
                print("��ƫ��")
                red_led.off()
                blue_led.off()
                green_led.off()
        else: #���Ч������
            red_led.off()
            blue_led.off()
            green_led.off()
    else: #��Ұ��û�з�����
        red_led.off()
        blue_led.off()
        green_led.on()
        pass
    #print(clock.fps())
