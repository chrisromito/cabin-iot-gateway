from utime import time, sleep_ms

from components.led import Led
from components.shared import Buses
from settings import BLUE_LED
from .rylr_modules import Rylr


uart = Buses().uart
lora = Rylr(uart)
led = Led(BLUE_LED)

BOARD_ID = 123
STATUS = 1

ERR_DELAY = 100
SUCCESS_DELAY = 500


def test_main():
    led.on()
    sleep_ms(500)
    led.off()
    sleep_ms(50)
    lora.init()
    while True:
        test_send_message()


def test_send_message():
    message = ','.join(
        [
            str(BOARD_ID),
            str(STATUS),
            str(time())
        ]
    )
    print('Sending message: ' + message + ' ...')
    success = lora.send(message)
    if success:
        print('... Message successfully sent')
        success_flash_sequence()
    else:
        print('... NO! The message didnt get sent =(')
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
