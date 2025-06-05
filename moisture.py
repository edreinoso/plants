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

def moisture_to_percentage(value, min_val=200, max_val=2000):
    percent = (value - min_val) / (max_val - min_val) * 100
    return max(0, min(100, percent))  # clamp between 0 and 100

while True:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    avg_moisture = take_sample()
    temp = ss.get_temp()

    if previous_avg is not None:
        if avg_moisture > previous_avg:
            if trend == "down":
                moisture_pct = moisture_to_percentage(previous_avg)
                print(f"[{now}] temp: {temp:.2f} °C  moisture avg: {moisture_pct:.1f}%")
            trend = "up"
        elif avg_moisture < previous_avg:
            if trend == "up":
                moisture_pct = moisture_to_percentage(previous_avg)
                print(f"[{now}] temp: {temp:.2f} °C  moisture avg: {moisture_pct:.1f}%")
            trend = "down"
        # If same, no change

    previous_avg = avg_moisture