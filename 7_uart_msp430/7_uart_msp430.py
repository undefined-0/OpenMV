# 注：OpenMV的P4口为其TX，P5口为其RX

import time
from pyb import UART

uart = UART(3,9600)
cmd_1 = "LED1 ON\n"
cmd_2 = "LED1 OFF\n"

while(True):
    uart.write(cmd_1)
    time.sleep(5)
    uart.write(cmd_2)
    time.sleep(5)
