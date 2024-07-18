# ��py��sensor.snapshot()��������img����һ�����飩
# ��ͼͨ�������������ݴ�������ɨ�裨����ĵ����������⼰���.md����ʵ������Ҫ��
# ����v3����Ϊ�˸�Ϊ�򵥵��㷨

THRESHOLD = (50,255) # ����ֵΪ��ɫ����
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
    img = sensor.snapshot().binary([THRESHOLD]) # ��ȡһ��ͼƬ��Ȼ���ͼƬ������ֵ�ָ��ֵ��������ֵ��������������Ϊ��ɫ����ֵ��������������Ϊ��ɫ����
    # THRESHOLD���ݵ�ֵ�Ǵ��ļ��ʼ���õ���ֵ
    # ͨ����Ƕ��forѭ����ʹ��image.get_pixel(x, y)��������ȡÿһ�����ص��ֵ
    # ÿ��5�б���һ��
    # ����img��һ���Ѿ�����õ�80�У�60�еĶ�ά����

    # ʹ��Ƕ��forѭ������img���飬ÿ��5�б���5��
    for start_row in range(0, 60, 10):  # ���ѭ������5Ϊ����������
        for row in range(start_row, min(start_row + 5, 60)):  # �����ѭ����������������5��
            for col_1 in range(80):  # ���ڲ�ѭ��������ÿһ��
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
