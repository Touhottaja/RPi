# Based on ssd1306_stats.py by Adafruit
# https://github.com/adafruit/Adafruit_CircuitPython_SSD1306/blob/main/examples/ssd1306_stats.py
import datetime
import time
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

DISPLAY_TIME_OFF_S = 60 * 9
DISPLAY_TIME_ON_S = 30
REFRESH_TIME_S = 0.5

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)

def clear_display() -> None:
    disp.fill(0)
    disp.show()


def main() -> None:
    while True:
        display_on_time_left = DISPLAY_TIME_ON_S
        while display_on_time_left:
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            # Shell scripts for system monitoring from here:
            # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
            #cmd = "hostname -I | cut -d' ' -f1"
            #IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
            cmd = 'cut -f 1 -d " " /proc/loadavg'
            CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
            cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB\", $3,$2}'"
            MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
            cmd = "vcgencmd measure_temp | grep  -o -E '[[:digit:]].*'"
            Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")

            # Write the text.

            #draw.text((x, top + 0), "IP: " + IP, font=font, fill=255)
            draw.text((x, top + 0), "CPU: " + CPU, font=font, fill=255)
            draw.text((x, top + 10), MemUsage, font=font, fill=255)
            draw.text((x, top + 20), "Temp: " + Temp, font=font, fill=255)

            # Display image.
            disp.image(image)
            disp.show()

            time.sleep(REFRESH_TIME_S)
            display_on_time_left -= REFRESH_TIME_S
        
        # Turn display "off"
        clear_display()
        time.sleep(DISPLAY_TIME_OFF_S)


if __name__ == "__main__":
    main()
