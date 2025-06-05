import time
from datetime import datetime

import board
from adafruit_seesaw.seesaw import Seesaw

SAMPLE_SIZE = 10
DELAY_BETWEEN_READS = 0.5  # seconds

i2c_bus = board.I2C()
ss = Seesaw(i2c_bus, addr=0x36)

previous_avg = None
trend = None  # "up" or "down"

def take_sample():
    readings = []
    for _ in range(SAMPLE_SIZE):
        moisture = ss.moisture_read()
        readings.append(moisture)
        time.sleep(DELAY_BETWEEN_READS)
    return sum(readings) / len(readings)

while True:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    avg_moisture = take_sample()
    temp = ss.get_temp()

    if previous_avg is not None:
        if avg_moisture > previous_avg:
            if trend == "down":
                print(f"[{now}] temp: {temp:.2f} °C  moisture avg: {previous_avg:.1f} ↓")
            trend = "up"
        elif avg_moisture < previous_avg:
            if trend == "up":
                print(f"[{now}] temp: {temp:.2f} °C  moisture avg: {previous_avg:.1f} ↑")
            trend = "down"
        # If same, no change

    previous_avg = avg_moisture