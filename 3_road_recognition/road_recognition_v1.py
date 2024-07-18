# 线段检测例程
#
# 这个例子展示了如何在图像中查找线段。对于在图像中找到的每个线对象，
# 都会返回一个包含线条旋转的线对象。

# find_line_segments()找到有限长度的线（但是很慢）。
# Use find_line_segments()找到非无限的线（而且速度很快）。

enable_lens_corr = True # turn on for straighter lines...打开以获得更直的线条…

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # 灰度更快
#sensor.set_pixformat(sensor.GRAYSCALE) # 灰度更快
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

# 所有线段都有 `x1()`, `y1()`, `x2()`, and `y2()` 方法来获得他们的终点
# 一个 `line()` 方法来获得所有上述的四个元组值，可用于 `draw_line()`.

while(True):
    clock.tick()
    img = sensor.snapshot()
    if enable_lens_corr: img.lens_corr(1.8) # for 2.8mm lens...

    # `merge_distance`控制附近行的合并。 在0（默认），没有合并。
    # 在1处，任何距离另一条线一个像素点的线都被合并...等等，
    # 因为你增加了这个值。 您可能希望合并线段，因为线段检测会产生大量
    # 的线段结果。

    # `max_theta_diff` 控制要合并的任何两线段之间的最大旋转差异量。
    # 默认设置允许15度。

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
