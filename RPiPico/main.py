from machine import UART, Pin
import time

def pulse(pin):
    pin.off()
    time.sleep(0.1)
    pin.on()

# if your relay board needs a constant signal, connect it to pin 27
# if your relay board needs a pulse to toggle, connect it to pin 26
relay1 = Pin(27, Pin.OUT)
relay1.off()
relay2 = Pin(26, Pin.OUT)
relay2.on()

# optional manual toggle button. button momentarily connects pin 28 to V+
button = Pin(28, Pin.IN, Pin.PULL_DOWN)

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
        time.sleep(0.5)
        print("Button toggle")

    if uart.any() > 0:
        rxData = uart.read(1);
        if "1" in rxData:
            uart.write("Toggling\r\n")
            relay1.toggle()
            pulse(relay2)
            print("Bluetooth Toggle")
