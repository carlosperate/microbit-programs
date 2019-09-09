from microbit import *

from nes_controller import read_nes_controller


def main():
    display.show(Image.HAPPY)
    sleep(1000)

    while True:
        nes_controller = read_nes_controller(latch=pin0, clock=pin1, data=pin2)

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
        elif nes_controller.left:
            display.show(Image.ARROW_W)
        elif nes_controller.right:
            display.show(Image.ARROW_E)
        elif nes_controller.a:
            display.show("A")
        elif nes_controller.b:
            display.show("B")
        elif nes_controller.start:
            display.show(Image(
                "99999:"
                "90090:"
                "99090:"
                "09090:"
                "99090"))
        elif nes_controller.select:
            display.show(Image(
                "99090:"
                "90090:"
                "99090:"
                "09090:"
                "99099"))

        uart.write("[U:{}] [D:{}] [L:{}] [R:{}] [ST:{}] [SL:{}] [A:{}] [B:{}]\r\n".format(
            nes_controller.up, nes_controller.down, nes_controller.left,
            nes_controller.right, nes_controller.start, nes_controller.select,
            nes_controller.a, nes_controller.b))

        sleep(200)


if __name__ == "__main__":
    main()
