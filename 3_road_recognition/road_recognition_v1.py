# �߶μ������
#
# �������չʾ�������ͼ���в����߶Ρ�������ͼ�����ҵ���ÿ���߶���
# ���᷵��һ������������ת���߶���

# find_line_segments()�ҵ����޳��ȵ��ߣ����Ǻ�������
# Use find_line_segments()�ҵ������޵��ߣ������ٶȺܿ죩��

enable_lens_corr = True # turn on for straighter lines...���Ի�ø�ֱ��������

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # �Ҷȸ���
#sensor.set_pixformat(sensor.GRAYSCALE) # �Ҷȸ���
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

# �����߶ζ��� `x1()`, `y1()`, `x2()`, and `y2()` ������������ǵ��յ�
# һ�� `line()` ��������������������ĸ�Ԫ��ֵ�������� `draw_line()`.

while(True):
    clock.tick()
    img = sensor.snapshot()
    if enable_lens_corr: img.lens_corr(1.8) # for 2.8mm lens...

    # `merge_distance`���Ƹ����еĺϲ��� ��0��Ĭ�ϣ���û�кϲ���
    # ��1�����κξ�����һ����һ�����ص���߶����ϲ�...�ȵȣ�
    # ��Ϊ�����������ֵ�� ������ϣ���ϲ��߶Σ���Ϊ�߶μ����������
    # ���߶ν����

    # `max_theta_diff` ����Ҫ�ϲ����κ����߶�֮��������ת��������
    # Ĭ����������15�ȡ�

    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0

    for l in img.find_line_segments(merge_distance=10, max_theta_diff=20):
        x1 += l.x1()
        y1 += l.y1()
        x2 += l.x2()
        y2 += l.y2()
        img.draw_line(l.line(), color=(0, 0, 255))
        img.draw_line(int(x1/2), int(y1/2), int(x2/2), int(y2/2), color=(255, 0, 0), thickness=2)
        # print(l)


    print("FPS %f" % clock.fps())
