from micropython import const
from constants import ZERO, ONE, TWO
try:
    from settings_prod import Settings
except:
    from settings_default import Settings

# Network
WLAN_HOST = Settings.WLAN_HOST
WLAN_PASSWORD = Settings.WLAN_PASSWORD
MQTT_BROKER_HOST = Settings.MQTT_BROKER_HOST
MQTT_BROKER_PORT = Settings.MQTT_BROKER_PORT
# Systems & other apps
API_URL = Settings.API_URL

# Ticks == 60 per sec == 60 per 1000ms
TICK_RATE_MS = const(1000 // 60)
TICK_RATE_SEC = 1 / 60

# Sleep = 3 seconds
SLEEP_DURATION_MS = const(3000)

# Pins
# ############
SDA = const(23)
SCL = const(22)
TX = const(17)
RX = const(16)
RED_LED = const(14)
GREEN_LED = const(15)
BLUE_LED = const(13)
BUTTON_PIN = None
# UART_BAUDRATE = const(38400)
UART_BAUDRATE = const(115200)
PROXY_TRIGGER_PIN = None
PROXY_ECHO_PIN = None
THERMOMETER_PIN = const(34)
FAN_PIN = const(21)

# Adapter configs
BUTTON_PIN_ADAPTER = ZERO
BUTTON_QWIIC_ADAPTER = ONE
BUTTON_ADAPTER = BUTTON_QWIIC_ADAPTER

PROXY_PIN_ADAPTER = ZERO
PROXY_QWIIC_ADAPTER = ONE
PROXY_ADAPTER = PROXY_QWIIC_ADAPTER

# Proxy thresholds, etc
PROXY_DISTANCE_THRESHOLD_CM = const(400)
# Cooling mechanism thresholds (aka fan)
FAN_MIN_THRESHOLD_CELSIUS = const(35)
