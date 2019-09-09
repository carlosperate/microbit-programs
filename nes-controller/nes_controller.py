# microbit-module: nes_controller@0.1.0
from ucollections import namedtuple

NesController = namedtuple(
    "NesController",
    ("a", "b", "select", "start", "up", "down", "left", "right")
)

def read_nes_controller(latch, clock, data):
    tempData = 0x00

    if data.read_digital() == 0:
        return NesController(*([False] * 8))

    latch.write_digital(1)
    latch.write_digital(0)
    for button in range(0, 8):
        if (data.read_digital() == 0):
            tempData = tempData | (1 << button)
        clock.write_digital(1)
        clock.write_digital(0)

    return NesController(
        bool(tempData & (1 << 0)),
        bool(tempData & (1 << 1)),
        bool(tempData & (1 << 2)),
        bool(tempData & (1 << 3)),
        bool(tempData & (1 << 4)),
        bool(tempData & (1 << 5)),
        bool(tempData & (1 << 6)),
        bool(tempData & (1 << 7))
    )
