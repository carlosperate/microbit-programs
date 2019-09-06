# microbit-module: gigglebot@1.0.0
from neopixel import NeoPixel
import microbit
from micropython import const

GET_VOLTAGE_BATTERY = const(4)
SET_MOTOR_POWERS = const(10)
LEFT = const(0)
RIGHT = const(1)
BOTH = 2
FORWARD = 1
BACKWARD = -1
motor_power_left = 50
motor_power_right = 50
neopixelstrip = None

buffer = bytearray(3)
buffer[0] = SET_MOTOR_POWERS

def _read(reg, size=8, repeat=False):
    microbit.i2c.write(0x04, bytes([reg]), repeat)
    outbuf = microbit.i2c.read(0x04, 1 if size==8 else 2, repeat)
    return outbuf[0] if size==8 else outbuf[0] * 255 + outbuf[1]

def _get_sensors(reg, repeat=False):
    microbit.i2c.write(0x04, bytes([reg]), repeat)
    outbuf = []
    buf = microbit.i2c.read(0x04, 3, repeat)
    outbuf.append(1023 - ( buf[0] << 2 | ((buf[2] & 0xC0) >> 6)))
    outbuf.append(1023 - ( buf[1] << 2 | ((buf[2] & 0x30) >> 4)))
    return outbuf

def volt():
    return (_read(GET_VOLTAGE_BATTERY, size=16)/1000)

def drive(dir=FORWARD, milliseconds=-1):
    buffer[1] = motor_power_left * dir
    buffer[2] = motor_power_right * dir
    microbit.i2c.write(0x04, buffer, False)
    if milliseconds >= 0:
        microbit.sleep(milliseconds)
        stop()

def turn(dir=LEFT, milliseconds=-1):
    if dir==LEFT:
        buffer[1] = motor_power_left
        buffer[2] = 0
    if dir==RIGHT:
        buffer[1] = 0
        buffer[2] = motor_power_right
    microbit.i2c.write(0x04, buffer, False)
    if milliseconds >= 0:
        microbit.sleep(milliseconds)
        stop()

def set_speed(power_left, power_right):
    global motor_power_left, motor_power_right
    motor_power_left = power_left
    motor_power_right = power_right

def stop():
    buffer[0] = SET_MOTOR_POWERS
    buffer[1] = 0
    buffer[2] = 0
    microbit.i2c.write(0x04, buffer, False)

def set_smile(R=25,G=0,B=0):
    neopix = range(2,9)
    for i in neopix:
        neopixelstrip[i] = (R,G,B)
    neopixelstrip.show()

def set_eyes(which=BOTH, R=0, G=0, B=10):
    if which != LEFT:
        neopixelstrip[0] = (R,G,B)
    if which != RIGHT:
        neopixelstrip[1]= (R,G,B)
    neopixelstrip.show()

def set_eye_color_on_start():
    if _read(GET_VOLTAGE_BATTERY, size=16) < 3400:
        neopixelstrip[0] = (10, 0, 0)
        neopixelstrip[1]= (10, 0, 0)
    else:
        neopixelstrip[0] = (0, 0, 10)
        neopixelstrip[1]= (0, 0, 10)
    neopixelstrip.show()

def read_sensor(which_sensor, which_side):
    if (which_side == LEFT): return _get_sensors(which_sensor)[0]
    elif (which_side == RIGHT): return _get_sensors(which_sensor)[1]
    else: return _get_sensors(which_sensor)

def pixels_off():
    for i in range(9):
        neopixelstrip[i] = (0,0,0)
    neopixelstrip.show()

def init():
    global neopixelstrip
    stop()
    neopixelstrip = const(NeoPixel(microbit.pin8, 9))
    pixels_off()
    eyestrip = const(NeoPixel(microbit.pin8, 2))
    set_eye_color_on_start()