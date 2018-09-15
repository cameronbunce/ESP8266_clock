import board 
import network 
import time 
import ntptime
import bitbangio as io
import adafruit_ht16k33.segments
# import adafruit_ssd1306


ssid = 'SixTwentyFour'
password = 'cameronanddominique'

i2c = io.I2C(board.SCL, board.SDA)
# oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
display = adafruit_ht16k33.segments.Seg14x4(i2c)

display.fill(0)

# oled.fill(0)
# oled.text('Circuit Python', 0, 0)
# oled.text('NTP clock', 0, 10)
# oled.show()
# time.sleep(0.25)

sta_if = network.WLAN(network.STA_IF)

# oled.fill(0)
# oled.text('Connecting to', 0, 0)
# oled.text(ssid, 0, 10)
# oled.show()

if not sta_if.isconnected():
    sta_if.active(True)
    sta_if.connect(ssid, password)
    while not sta_if.isconnected():
        pass
        
# oled.text("IP: " + sta_if.ifconfig()[0], 0, 20)
# oled.show()
# time.sleep(0.25)

TZ = 14400 # UTC to EDT
# SECS = 43200 # 12-hour time
# SECS = 86400 # 24-hour time


t = None
while not t:
    time.sleep(0.1)    
    try:
        t = ntptime.ntptime()
    except Exception:
        pass


mono_time = int(time.monotonic())

while True:
    tm = t - mono_time + int(time.monotonic())
    now = time.localtime(tm-TZ)
    hr = now.tm_hour % 12 # 12-hour time for humans
    
    if hr == 0:
        hr = 12 # also for humans
    
    
#    if (tm-TZ)%43200 < 6: # possibly obo, but not on the skip side, to reset the display to not show the 1 in the tens column when the clock goes from 12 to 1
#        display.fill(0)
    if int(hr/10) == 0:
        display[0] = ''
    else:
        display[0] = '1' # give me a break, its 12-hour time
        
    display[1] = str(int(hr % 10))
    display[2] = str(int(now.tm_min/10))
    display[3] = str(int(now.tm_min % 10))
    display.show()
    time.sleep(5) # this is the counter of "how far behind can we wait to flip the minute"? 5 seconds, impacts our tens of hours reset
    