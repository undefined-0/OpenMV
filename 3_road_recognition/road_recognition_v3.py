# ��py��sensor.snapshot()��������img����һ�����飩
# ��ͼͨ�������������ݴ�������ɨ�裨����ĵ����������⼰���.md����ʵ������Ҫ��

THRESHOLD = (32, 100, -32, 15, -25, 22) # ����ֵΪ��ɫ����
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
    img = sensor.snapshot().binary([THRESHOLD]) # ��ȡһ��ͼƬ��Ȼ���ͼƬ������ֵ�ָ��ֵ��������ֵ��������������Ϊ��ɫ����ֵ��������������Ϊ��ɫ����
    # THRESHOLD���ݵ�ֵ�Ǵ��ļ��ʼ���õ���ֵ
    # ͨ����Ƕ��forѭ����ʹ��image.get_pixel(x, y)��������ȡÿһ�����ص��ֵ
    # ÿ��5�б���һ��
    # ����img��һ���Ѿ�����õ�80�У�60�еĶ�ά����

    # ʹ��Ƕ��forѭ������img���飬ÿ��5�б���5��
    for start_row in range(0, 60, 10):  # ���ѭ������5Ϊ����������
        for row in range(start_row, min(start_row + 5, 60)):  # �����ѭ����������������5��
            flag = 0 # ���Լ���ǵڼ���ɨ�赽��ɫ���ص�
            x1_start = 0
            x1_end = 0
            x2_start = 0
            x2_end = 0
            for col in range(80):  # ���ڲ�ѭ��������ÿһ��
                pixel_tuple = img.get_pixel(row, col) #����ǰ���е�����ֵԪ�鴫��pixel_tuple
                if pixel_tuple == (0,0,0): # ��
                    flag += 1
                    if flag == 1: # ɨ�赽���ǵ�һ����ɫֱ���ϵĵ�һ����ɫ���ص�
                        x1_start = col # ��¼��ɨ���ĵ�һ����ɫ���ص����ֵ
                        x1_end = x1_start
                    else: # ���ǵ�һ��ɨ�赽��ɫ���ص�
                        x1_start += 1 # ûɨ�赽��ɫ����ɫ�Ŀ�Ⱦ�һֱ����
                if (pixel_tuple == (255,255,255)) & (flag != 0)&((x1_end-x1_start)>3): # ����ǰ��ɫ��ɨ�赽��ɫ���Һ�ɫ��ȴ���3�����أ����ٴ�ɨ�赽�İ�ɫ������һ�иտ�ʼʱ��ɨ�赽�İ�ɫ����ô�ͼ�¼��x1��ֵ
                    x1 = (x1_start + x1_end) / 2
                    flag = 0
                    # continue

                if pixel_tuple == (0,0,0): # ��
                    flag += 1
                    if flag == 1: # ɨ�赽���ǵڶ�����ɫֱ���ϵĵ�һ����ɫ���ص�
                        x2_start = col # ��¼��ɨ���ĵ�һ����ɫ���ص����ֵ
                        x1_end = x2_start
                    else: # ���ǵ�һ��ɨ�赽��ɫ���ص�
                        x2_start += 1 # ûɨ�赽��ɫ����ɫ�Ŀ�Ⱦ�һֱ����
                if (pixel_tuple == (255,255,255)) & (flag != 0)&((x2_end-x2_start)>3): # ����ǰ��ɫ��ɨ�赽��ɫ���Һ�ɫ��ȴ���3�����أ����ٴ�ɨ�赽�İ�ɫ������һ�иտ�ʼʱ��ɨ�赽�İ�ɫ����ô�ͼ�¼��x2��ֵ
                    x2 = (x2_start + x1_end) / 2

                    # ���������ϵĺڵ㶼�Ѽ�⵽���򻭳����������ڵ�����ĵ�
                    x_middle = (x1+x2)/2
                    img.draw_line(int(x_middle), int(col), int(x_middle), int(col), color=(255, 0, 0), thickness=2)




    #print(clock.fps())
