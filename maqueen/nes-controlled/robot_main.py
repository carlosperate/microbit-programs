from microbit import *
from neopixel import NeoPixel
from random import randint
import radio

from shared_config import RADIO_CHANNEL, MSG_DEYLAY

class MaqueenRobot:

    DIR_FORWARD = 0
    DIR_BACKWARD = 1

    def __init__(self, i2c, led_left, led_right, leds_rgb):
        self._i2c = i2c
        self._buffer_left = bytearray(3)
        self._buffer_right = bytearray(3)
        self.leds = [led_left, led_right]
        self.leds_rgb = NeoPixel(leds_rgb, 4, bpp=4)

    def leds_rgb_random(self):
        for i in range(len(self.leds_rgb)):
            self.leds_rgb[i] = (randint(0,255), randint(0,255), randint(0,255), 0)
            self.leds_rgb.show()

    def led_animation(self, rounds=1):
        for _ in range(rounds):
            for led in self.leds:
                self.leds_rgb_random()
                led.write_digital(1)
                sleep(150)
                self.leds_rgb_random()
                led.write_digital(0)
                sleep(150)

    def motor_left(self, direction, speed):
        self._buffer_left[0] = 0x00
        self._buffer_left[1] = direction
        self._buffer_left[2] = speed
        self._i2c.write(0x10, self._buffer_left)

    def motor_right(self, direction, speed):
        self._buffer_right[0] = 0x02
        self._buffer_right[1] = direction
        self._buffer_right[2] = speed
        self._i2c.write(0x10, self._buffer_right)

    def turn_left(self):
        self.motor_left(robot.DIR_FORWARD, 0)
        self.motor_right(robot.DIR_FORWARD, 255)

    def turn_right(self):
        self.motor_right(robot.DIR_FORWARD, 0)
        self.motor_left(robot.DIR_FORWARD, 255)

    def stop(self):
        self._buffer_left[1] = 0
        self._buffer_left[2] = 0
        self._buffer_right[1] = 0
        self._buffer_right[2] = 0
        self._i2c.write(0x10, self._buffer_left)
        self._i2c.write(0x10, self._buffer_right)


robot = MaqueenRobot(i2c, pin8, pin12, pin15)

def move_robot(direction, turn):
    if direction == 0:
        if turn > 0:
            robot.turn_left()
        elif turn < 0:
            robot.turn_right()
        else:
            robot.stop()
        return


    d = robot.DIR_FORWARD
    if direction < 0:
        d = robot.DIR_BACKWARD

    left_power = right_power = 255
    if turn < 0:
        # Going left, reduce right speed
        right_power //= 2
    elif turn > 0:
        # Going right, reduce left speed
        left_power //= 2
    print('\t[D:{}] [L:{}] [R:{}]'.format(d, left_power, right_power))
    robot.motor_left(direction=d, speed=left_power)
    robot.motor_right(direction=d, speed=right_power)

def main():
    robot.led_animation(rounds=2)
    radio.config(channel=RADIO_CHANNEL)

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
                    move_robot(direction, turn)
                except:
                    pass
            else:
                robot.stop()
            if leds:
                try:
                    robot.leds_rgb_random()
                except:
                    pass
        else:
            # process_radio_silence
            silence_count += 1
            if silence_count >= half_sec_count:
                silence_count = 0
                robot.stop()
        sleep(MSG_DEYLAY)

if __name__ == "__main__":
    main()
