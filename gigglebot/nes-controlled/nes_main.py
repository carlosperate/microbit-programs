from microbit import *
import radio

from nes_controller import read_nes_controller
from shared_config import RADIO_CHANNEL, MSG_DEYLAY


def main():
    radio.config(channel=RADIO_CHANNEL)
    radio.on()

    while True:
        nes_controller = read_nes_controller(latch=pin0, clock=pin1, data=pin2)

        # Update display
        display.clear()
        if nes_controller.up:
            if nes_controller.left:
                display.show(Image.ARROW_NW)
            elif nes_controller.right:
                display.show(Image.ARROW_NE)
            else:
                display.show(Image.ARROW_N)
        elif nes_controller.down:
            if nes_controller.left:
                display.show(Image.ARROW_SW)
            elif nes_controller.right:
                display.show(Image.ARROW_SE)
            else:
                display.show(Image.ARROW_S)
        else:
            if nes_controller.left:
                display.show(Image.ARROW_W)
            elif nes_controller.right:
                display.show(Image.ARROW_E)

        # Prepare data to send
        direction = 0
        if nes_controller.up:
            direction = 1
        elif nes_controller.down:
            direction = -1
        turn = 0
        if nes_controller.right:
            turn = 1
        elif nes_controller.left:
            turn = -1

        print("[D:{}] [T:{}] [A:{}] [B:{}]".format(
                direction, turn, int(nes_controller.a), int(nes_controller.b)))
        radio.send('{}:{}:{}:{}'.format(
                direction, turn, int(nes_controller.a), int(nes_controller.b)))
        sleep(MSG_DEYLAY)


if __name__ == "__main__":
    main()
