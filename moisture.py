# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
from datetime import datetime

import board
from adafruit_seesaw.seesaw import Seesaw

i2c_bus = board.I2C()  # uses board.SCL and board.SDA
ss = Seesaw(i2c_bus, addr=0x36)

while True:
    # Get current date and time
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Read moisture and temperature
    touch = ss.moisture_read()
    temp = ss.get_temp()

    # Print with timestamp
    print(f"[{now}] temp: {temp:.2f} °C  moisture: {touch}")
    
    time.sleep(1)