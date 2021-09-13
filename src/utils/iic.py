from machine import I2C


def parse(iic_value: bytes) -> int:
    iic_int = bytes_to_int(iic_value)
    left = iic_int << 8
    return left | iic_int


def get_register(iic: I2C, address, register, length: int = EIGHT) -> int:
    return parse(iic.readfrom_mem(address, register, length))


def write_register(iic: I2C, address, register):
    def _write_register(value: bytearray):
        return iic.writeto_mem(address, register, value)

    return _write_register
