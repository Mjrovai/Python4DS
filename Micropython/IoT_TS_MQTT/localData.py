# import general libraries
from machine import Pin
import time
from time import sleep

# Define constants
PUB_TIME_SEC = 30 

# define pin 0 (LED) as output
led = Pin(0, Pin.OUT)

# DHT
from dht import DHT22
dht22 = DHT22(Pin(12))

# Function to read DHT
def readDht():
    dht22.measure()
    return dht22.temperature(), dht22.humidity()

# DS18B20 
import onewire, ds18x20

# Define which pin the 1-wire device will be connected ==> pin 2 (D4)
dat = Pin(2)

# Create the onewire object
ds = ds18x20.DS18X20(onewire.OneWire(dat))

# scan for devices on the bus
sensors = ds.scan()

# function to read DS18B20 
def readDs(): 
    ds.convert_temp()
    time.sleep_ms(750)
    return round(ds.read_temp(sensors[0]), 1)

# LDR
from machine import ADC

# Define object
adc = ADC(0)

#function to read luminosity
def readLdr():
    lumPerct = (adc.read()-40)*(10/86) # convert in percentage ("map")
    return round(lumPerct)

# define pin 13 as an input and activate an internal Pull-up resistor:
button = Pin(13, Pin.IN, Pin.PULL_UP)

# Function to read button state:
def readBut():
        return button.value()

# Function to read all data:
def colectData():
    temp, hum, = readDht()
    extTemp = readDs()
    lum = readLdr()
    butSts = readBut()
    return temp, hum, extTemp, lum, butSts

# import library and create object i2c
from machine import I2C
i2c = I2C(scl=Pin(5), sda=Pin(4))

# import library and create object oled
import ssd1306
i2c = I2C(scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c)

# create a function do display all data:
def displayData(temp, hum, extTemp, lum, butSts):
    oled.fill(0)
    oled.text("Temp:    " + str(temp) + "oC", 0, 4)
    oled.text("Hum:     " + str(hum) + "%",0, 16)
    oled.text("ExtTemp: " + str(extTemp) + "oC", 0, 29)
    oled.text("Lumin:   " + str(lum) + "%", 0, 43)
    oled.text("Button:  " + str(butSts), 0, 57)
    oled.show()


''' ------ general functions ----'''

# Clear display :
def displayClear():
    oled.fill(0)
    oled.show()
    
# create a blink function
def blinkLed(num):
    for i in range(0, num):
        led.on()
        sleep(0.5)
        led.off()
        sleep(0.5)

'''------ main function --------'''
def main():
    while button.value():
        led.on()
        temp, hum, extTemp, lum, butSts = colectData()
        displayData(temp, hum, extTemp, lum, butSts)
        led.off()
        time.sleep(PUB_TIME_SEC)
    blinkLed(3)
    displayClear()


'''------ run main function --------'''
main()
