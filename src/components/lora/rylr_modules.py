"""
RYLRxx6 (RYLR896 in this case) LoRa UART modules
Manufacturer: Reyax
Product: RYLR896
Product Page: http://reyax.com/products/rylr896/
Command Datasheet: https://reyax.com/wp-content/uploads/2020/01/Lora-AT-Command-RYLR40x_RYLR89x_EN.pdf
Module Datasheet: https://reyax.com/wp-content/uploads/2019/12/RYLR896_EN-1.pdf

==============

Source: https://github.com/wybiral/micropython-rylr/blob/master/rylr.py

"""
from utime import sleep_ms


class Packet:
    def __init__(self, data, address=0, rssi=0, snr=0):
        self.data = data
        self.address = address
        self.rssi = rssi
        self.snr = snr

    def __str__(self):
        return self.data


def uart_to_packet(resp: str) -> Packet:
    """
    TypeError: can't convert 'str' object to bytes implicitly
    :param resp:
    :return:

    Example (decoded) UART response:  +RCV=0,9,123,1,578,-50,42\r\n
    """
    payload = resp[5:-2]  # '+RCV=0,9,123,1,578,-50,42\r\n' => '0,9,123,1,578,-50,42'
    # '0,9,123,1,578,-50,42' => ['0', '9', '123,1,578,-50,42']
    address, length, rest = payload.split(',', 2)
    # '123,1,578,-50,42' => ['123,1,578', '-50', '42']
    data, rssi, snr = rest.rsplit(',', 2)
    return Packet(data, int(address), int(rssi), int(snr))


def chill():
    sleep_ms(10)


class Rylr:
    def __init__(self, uart, **kwargs):
        self.uart = uart
        self._packet = None
        self._frequency = kwargs.get('frequency', 915.0)
        self._bandwidth = kwargs.get('bandwidth', 250000)
        self._spreading_factor = kwargs.get('spreading_factor', 10)
        self._coding_rate = kwargs.get('coding_rate', 8)
        self._preamble_length = kwargs.get('preamble_length', 4)
        self.is_ready = False

    def init(self):
        if self.is_ready:
            return self
        self.reset()
        can_communicate = self.heartbeat()
        if not can_communicate:
            raise RuntimeError('Cannot connect to RYLR Module')
        self.set_frequency(self._frequency)
        self._set_parameters()
        self.is_ready = True
        return self

    def heartbeat(self):
        uart = self.uart
        self.write('AT')
        count = 0
        while count < 2000:
            count = count + 1
            chill()
            if uart.any():
                resp = uart.readline()
                print('heartbeat -> resp: ')
                print(resp)
                return resp
        return None

    def send(self, message, address=0):
        return self._cmd('AT+SEND=%i,%i,%s' % (address, len(message), message))

    def write(self, payload: str):
        self.uart.write(payload + '\r\n')

    def _cmd(self, payload: str):
        print('cmd start: ')
        print(payload)
        self.write(payload)
        count = 0
        while count < 2000:
            count = count + 1
            resp = self.uart.read()
            if resp:
                return resp
            else:
                chill()
        print('\n-- Cmd Failed:')
        print(ValueError(payload))

    def receive(self):
        uart = self.uart
        count = 0
        while count < 2000:
            count = count + 1
            x = uart.readline()
            decoded = (
                x.decode()
                if x else None
            )
            if decoded and decoded.startswith('+RCV='):
                print('self._receive...')
                self._packet = uart_to_packet(decoded)
                return self._packet
            elif decoded is not None:
                print('Unexpected message: ' + decoded)
        return None

    def reset(self):
        uart = self.uart
        self.write('AT+RESET')
        count = 0
        while count < 2000:
            count = count + 1
            chill()
            if uart.any() and uart.read() is not None:
                return True
        print('Reset failed')

    def get_baud_rate(self):
        x = self._cmd('AT+IPR?')
        return int(x[5:])

    def set_baud_rate(self, x):
        return self._cmd('AT+IPR=' + x)

    def get_frequency(self):
        x = self._cmd('AT+BAND?')
        return int(x[6:]) / 1000000.0

    def set_frequency(self, x):
        return self._cmd('AT+BAND=' + str(round(x * 1000000)))

    def _set_parameters(self):
        sf = self._spreading_factor
        bws = (7800, 10400, 15600, 20800, 31250, 41700, 62500, 125000, 250000)
        bw = 9
        for i in range(len(bws)):
            if self._bandwidth <= bws[i]:
                bw = i
                break
        cr = self._coding_rate - 4
        pl = self._preamble_length
        return self._cmd('AT+PARAMETER=%i,%i,%i,%i' % (sf, bw, cr, pl))

    def get_address(self):
        x = self._cmd('AT+ADDRESS?')
        return int(x[9:])

    def set_address(self, addr):
        return self._cmd('AT+ADDRESS=' + str(addr))

    def get_bandwidth(self):
        return self._bandwidth

    def set_bandwidth(self, bw):
        self._bandwidth = bw
        return self._set_parameters()

    def get_coding_rate(self):
        return self._coding_rate

    def set_coding_rate(self, cr):
        self._coding_rate = cr
        return self._set_parameters()

    def get_preamble_length(self):
        return self._preamble_length

    def set_preamble_length(self, pl):
        self._preamble_length = pl
        return self._set_parameters()

    def get_spreading_factor(self):
        return self._spreading_factor

    def set_spreading_factor(self, sf):
        self._spreading_factor = sf
        return self._set_parameters()

    def get_network(self):
        x = self._cmd('AT+NETWORKID?')
        return int(x[11:])

    def set_network(self, n):
        return self._cmd('AT+NETWORKID=' + str(n))

    def get_aes_key(self):
        x = self._cmd('AT+CPIN?')
        return x[6:]

    def set_aes_key(self, key):
        return self._cmd('AT+CPIN=' + key)
