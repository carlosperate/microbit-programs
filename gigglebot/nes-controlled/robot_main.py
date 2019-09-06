from microbit import *
import radio
from random import randint

import gigglebot
from shared_config import RADIO_CHANNEL, MSG_DEYLAY


def apply(direction, turn):
    if direction == 0:
        if turn > 0:
            gigglebot.turn(gigglebot.RIGHT)
        elif turn < 0:
            gigglebot.turn(gigglebot.LEFT)
        else:
            stop()
        return

    if direction > 0:
        d = gigglebot.FORWARD
    elif direction < 0:
        d = gigglebot.BACKWARD

    left_power = right_power = 100
    if turn < 0:
        # Going left, reduce right speed
        right_power //= 2
    elif turn > 0:
        # Going right, reduce left speed
        left_power //= 2
    print('\t[D:{}] [L:{}] [R:{}]'.format(d, left_power, right_power))
    gigglebot.set_speed(left_power, right_power)
    gigglebot.drive(dir=d)


def random_leds():
    gigglebot.set_eyes(which=gigglebot.BOTH, R=randint(0,255), G=randint(0,255), B=randint(0,255))
    # gigglebot.set_smile(R=randint(0,255), G=randint(0,255), B=randint(0,255))
    for i in range(2,9):
        gigglebot.neopixelstrip[i] = (randint(0,255), randint(0,255), randint(0,255))
    gigglebot.neopixelstrip.show()


def stop():
    try:
        gigglebot.stop()
    except:
        pass


def main():
    radio.config(channel=RADIO_CHANNEL)
    radio.on()

    try:
        gigglebot.init()
        gigglebot.set_smile(255,0,0)
    except:
        display.show(Image.ARROW_S)

    silence_count = 0
    half_sec_count = 500 // MSG_DEYLAY

    while True:
        try:
            msg = radio.receive()
        except:
            msg = None
        if msg is not None:
            direction, turn, active, leds = [int(data) for data in msg.split(':')]
            print("[D:{}] [T:{}] [A:{}] [B:{}]".format(direction, turn, active, leds))
            if active:
                try:
                    apply(direction, turn)
                except:
                    pass
            else:
                stop()
            if leds:
                try:
                    random_leds()
                except:
                    pass
        else:
            # process_radio_silence
            silence_count += 1
            if silence_count >= half_sec_count:
                silence_count = 0
                stop()
        sleep(MSG_DEYLAY)


if __name__ == "__main__":
    main()
