import network
import secrets
import time
import urequests
import ujson
from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.SSID, secrets.PASSWORD)
time.sleep(5)
print(wlan.isconnected())


YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3/channels'
try:
    while True:
        url = f'{YOUTUBE_API_URL}?part=statistics&id={secrets.CHANNEL_ID}&key={secrets.API_KEY2}'
        response = urequests.get(url)
        if response.status_code == 200:
            data = ujson.loads(response.text)
            subscriber_count = data['items'][0]['statistics']['subscriberCount']
            print("Subscriber count: " + subscriber_count)
            lcd.backlight_on()
            lcd.putstr("Subscribers\n")
            lcd.putstr(subscriber_count)
        else:
            print('Error fetching data from YouTube API')
        time.sleep(3600)
        lcd.clear()
except Exception as e:
    print(f'An error occurred: {e}')
