# import required modules
from machine import ADC, Pin
import time
import network
import blynk

# use variables instead of numbers:
soil = ADC(Pin(26))  # Soil moisture PIN reference

# Calibraton values
min_moisture = 19200
max_moisture = 49300

readDelay = 2  # delay between readings

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("SSID", "Password")

# Blynk authentication token
BLYNK_AUTH = "******************************"


# connect the network
wait = 10
while wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    wait -= 1
    print("waiting for connection...")
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError("wifi connection failed")
else:
    print("connected")
    ip = wlan.ifconfig()[0]
    print("IP: ", ip)

# Initialize Blynk
blynk_client = blynk.Blynk(BLYNK_AUTH)

# Run the main loop
while True:
    # read moisture value and convert to percentage into the calibration range
    moisture = (max_moisture - soil.read_u16()) * 100 / (max_moisture - min_moisture)
    # print values
    print("moisture: " + "%.2f" % moisture + "% (adc: " + str(soil.read_u16()) + ")")

    # Send sensor data to Blynk
    blynk_client.virtual_write(0, moisture)  # virtual pin 1 for temperature

    # Run Blynk
    blynk_client.run()

    utime.sleep(readDelay)  # set a delay between readings
