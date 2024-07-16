# OpenMV 和 Arduino Uno 基本uart通信

# 1) OpenMV Cam 与 Arduino Uno 按如下连线:
#
# OpenMV Cam Ground Pin   ----> Arduino Ground
# OpenMV Cam UART3_TX(P4) ----> Arduino Uno UART_RX(0)
# OpenMV Cam UART3_RX(P5) ----> Arduino Uno UART_TX(1)

# 2) 取消注释并将以下类似代码（需要你自己编写修改）上传到Arduino:
#
# void setup() {
#   // put your setup code here, to run once:
#   Serial.begin(19200);
# }
# 
# void loop() {
#   // put your main code here, to run repeatedly:
#   if (Serial.available()) {
#     // Read the most recent byte
#     byte byteRead = Serial.read();
#     // ECHO the value that was read
#     Serial.write(byteRead);
#   }
# }

# 3) 在OpenMV IDE中运行以下代码:

import time
from pyb import UART

# UART 3, and baudrate.
uart = UART(3, 19200)

while(True):
    uart.write("Hello World!\n")
    if (uart.any()):
        print(uart.read())
    time.sleep_ms(1000)