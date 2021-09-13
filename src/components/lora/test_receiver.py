from utime import sleep_ms

from components.led import Led
from components.shared import Buses
from settings import BLUE_LED
from .rylr_modules import Rylr


uart = Buses().uart
rylr = Rylr(uart)
led = Led(BLUE_LED)

BOARD_ID = 123
STATUS = 1

ERR_DELAY = 200
SUCCESS_DELAY = 500


def test_main():
    led.on()
    sleep_ms(500)
    led.off()
    sleep_ms(50)
    try:
        print('Initializing...')
        rylr.init()
        print('...Initialization complete')
    except Exception as err:
        error_flash_sequence()
        raise err
    print('\n=============================')
    print('\nBegin test_rylr_receiver loop')
    while True:
        test_rylr_receiver()


def test_rylr_receiver():
    data = rylr.receive()
    if data:
        print('Received data:')
        print(data)
        success_flash_sequence()
    else:
        print('Did not receive data =(')
        error_flash_sequence()
    sleep_ms(1000)
    return True


def success_flash_sequence():
    for _ in range(2):
        led.on()
        sleep_ms(SUCCESS_DELAY)
        led.off()


def error_flash_sequence():
    for _ in range(10):
        led.on()
        sleep_ms(ERR_DELAY)
        led.off()
