from utime import time, sleep

from components.led import Led
from components.shared import Buses
from settings import BLUE_LED
from .rylr_modules import Rylr


uart = Buses().uart
rylr = Rylr(uart)
led = Led(BLUE_LED)


def test_rylr_receiver():
    led.off()
    print('Begin test_rylr_receiver')
    data = rylr.receive()
    if data:
        print('Received data:')
        print(data)
        success_flash_sequence()
    else:
        print('Did not receive data =(')
        error_flash_sequence()


def success_flash_sequence():
    led.on()
    sleep(2)
    led.off()


def error_flash_sequence():
    led.on()
    sleep(0.2)
    led.off()
    sleep(0.1)
    led.on()
    sleep(0.1)
    led.off()


def test_lora():
    print('Start test_lora()')
    test_rylr_sender()
    print('Lora Tests complete...')
    return True
