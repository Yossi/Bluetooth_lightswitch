from machine import UART, Pin
import time

def pulse(pin):
    pin.toggle()
    time.sleep(0.1)
    pin.toggle()

# if your relay board needs a constant signal to remain switched, connect it to pin 28
relay1 = Pin(28, Pin.OUT)
relay1.off()
# if your relay board needs a pulse to toggle
# connect it to pin 27 for always low or 26 for always high
relay2 = Pin(27, Pin.OUT)
relay2.off()
relay3 = Pin(26, Pin.OUT)
relay3.on()

# optional manual toggle button. button momentarily connects pin 22 to V+
button = Pin(22, Pin.IN, Pin.PULL_DOWN)
# you can also optionally put a button between RUN and GND to reset the pico and usually reset the relay too.

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

''' # this gets flashed to the HC-06 so only needs to happen once
# HC-06 is receptive to AT commands so long as nothing is connected to it over Bluetooth

name = b'lights'
pin = b'1111'

uart.read(uart.write(b'AT+NAME%s\r\n' % name))
uart.read(uart.write(b'AT+PIN%s\r\n' % pin))
'''

uart.write("Starting Application\r\n")

while True:
    if button.value():
        relay1.toggle()
        pulse(relay2)
        pulse(relay3)
        time.sleep(0.5)
        print("Button toggle")

    if uart.any() > 0:
        rxData = uart.read(1);
        if "1" in rxData:
            uart.write("Toggling\r\n")
            relay1.toggle()
            pulse(relay2)
            pulse(relay3)
            print("Bluetooth Toggle")
