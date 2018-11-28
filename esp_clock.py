import board 
import network 
import time 
import ntptime
import bitbangio as io
import adafruit_ht16k33.segments

ssid = 'SixTwentyFour'
password = 'cameronanddominique'

i2c = io.I2C(board.SCL, board.SDA)
display = adafruit_ht16k33.segments.Seg14x4(i2c)
display.fill(0)

sta_if = network.WLAN(network.STA_IF)

if not sta_if.isconnected():
    sta_if.active(True)
    sta_if.connect(ssid, password)
    while not sta_if.isconnected():
        pass
        

#TZ = 14400 # UTC to EDT
TZ = 18000 # UTC to EST

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
    zero = 0
    if hr == 0:
        hr = 12 # also for humans
        # to-do, check NTP again and reset ms offsets to keep the planes in the air without a reboot
    
    
#    if (tm-TZ)%43200 < 6: # possibly obo, but not on the skip side, to reset the display to not show the 1 in the tens column when the clock goes from 12 to 1
#        display.fill(0)
    if int(hr/10) == 0 and zero == 0:
        display.fill(0)
        zero += 1
    elif int(hr/10) == 0:
        pass
    else:
        display[0] = '1' # give me a break, its 12-hour time
        zero = 0
    display[1] = str(int(hr % 10))
    display[2] = str(int(now.tm_min/10))
    display[3] = str(int(now.tm_min % 10))
    display.show()
    time.sleep(10) # this is the counter of "how far behind can we wait to flip the minute"? 5 seconds, impacts our tens of hours reset
    
