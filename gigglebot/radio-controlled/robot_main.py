from microbit import *
import radio
from random import randint
import gigglebot

# Config
RADIO_CHANNEL = 17
MSG_DELAY = 20
CTRL_MSG_DEYLAY = 100
DRIVE_DELAY = CTRL_MSG_DEYLAY // 2

robot_running = False


def apply(power, direction):
    global robot_running
    robot_running = True
    # Calculate is power forward or backwards
    d = gigglebot.FORWARD if power >= 0 else gigglebot.BACKWARD
    power = abs(power) // 10
    left_power = right_power = power
    if direction < 0:
        # Going left, reduce right speed
        left_power = max(100, power - (direction * -2))
    else:
        # Going right, reduce left speed
        right_power = max(100, power - (direction * 2))
    print('\t\t\t\t[D:{}] [L:{}] [R:{}]'.format(d, left_power, right_power))
    gigglebot.set_speed(left_power, right_power)
    gigglebot.drive(dir=d)


def random_leds():
    gigglebot.set_eyes(which=gigglebot.BOTH, R=randint(0,255), G=randint(0,255), B=randint(0,255))
    # gigglebot.set_smile(R=randint(0,255), G=randint(0,255), B=randint(0,255))
    for i in range(2,9):
        gigglebot.neopixelstrip[i] = (randint(0,255), randint(0,255), randint(0,255))
    gigglebot.neopixelstrip.show()


def stop():
    global robot_running
    robot_running = False
    try:
        gigglebot.stop()
    except:
        pass

silence_count = 0
one_sec_count = 500 // MSG_DELAY
def process_radio_silence():
    global silence_count
    silence_count += 1
    if silence_count >= one_sec_count and robot_running:
        silence_count = 0
        stop()
    

# Main
radio.config(channel=RADIO_CHANNEL)
radio.on()
try:
    gigglebot.init()
    gigglebot.set_smile(255,0,0)
except:
    display.show(Image.ARROW_S)
    sleep(1000)

while True:
    try:
        msg = radio.receive()
    except:
        msg = None
    if msg is not None:
        active, power, direction, leds = [int(data) for data in msg.split(':')]
        print('[A:{}] [P:{}] [D:{}] [L:{}]'.format(active, power, direction, leds))
        if active:
            try:
                apply(power, direction)
            except:
                pass
        else:
            stop()
        if leds:
            random_leds()
    else:
        process_radio_silence()
    sleep(MSG_DELAY)