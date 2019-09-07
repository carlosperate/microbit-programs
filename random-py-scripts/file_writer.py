"""
Create a bunch of files until the filesystem is full-ish
"""
from microbit import display, Image
import random

display.show(Image.CHESSBOARD)
continue_looping = True
file_number = 1
while continue_looping:
    try:
        filename = "file_{}.{}".format(file_number, random.choice(["py", "txt"]))
        with open(filename, "w") as f:
            f.write("a" * random.randint(100, 2000))
    except:
        continue_looping = False
    file_number += 1
display.show(Image.HAPPY)
