from smbus2 import SMBus, i2c_msg
import time

I2C_BUS = 1  # Use 1 for most Raspberry Pi models
DEVICE_ADDRESS = 0x12  # 7-bit I2C address of the IS3750

# IS3750 register map
REGISTER_SHOW = 0x00
REGISTER_LED1_RED = 0x01
REGISTER_LED1_GREEN = 0x02
REGISTER_LED1_BLUE = 0x03
REGISTER_LED2_RED = 0x04
REGISTER_LED2_GREEN = 0x05
REGISTER_LED2_BLUE = 0x06
REGISTER_LED3_RED = 0x07
REGISTER_LED3_GREEN = 0x08
REGISTER_LED3_BLUE = 0x09

def write_register(start_register, data_bytes):
    """
    Write a block of data starting at a 16-bit register address.
    
    :param start_register: The 16-bit register address to start writing to.
    :param data_bytes: A list of bytes to write.
    """
    high_addr = (start_register >> 8) & 0xFF
    low_addr = start_register & 0xFF
    with SMBus(I2C_BUS) as bus:
        msg = i2c_msg.write(DEVICE_ADDRESS, [high_addr, low_addr] + data_bytes)
        bus.i2c_rdwr(msg)

def show_leds():
    """Send the 'show' command to apply the LED updates."""
    write_register(REGISTER_SHOW, [1])

def clear_all_led_registers():
    """Clear all LED registers by sending 3600 zero bytes."""
    data = [0] * (1200 * 3)
    write_register(REGISTER_LED1_RED, data)

# Example usage loop
while True:
    clear_all_led_registers()
    write_register(REGISTER_LED1_GREEN, [5])
    show_leds()
    time.sleep(1)

    clear_all_led_registers()
    write_register(REGISTER_LED2_RED, [5])
    write_register(REGISTER_LED2_GREEN, [5])
    show_leds()
    time.sleep(1)

    clear_all_led_registers()
    write_register(REGISTER_LED3_RED, [5])
    show_leds()
    time.sleep(1)
