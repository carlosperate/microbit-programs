from microbit import display, Image, accelerometer, sleep

while True:
    if accelerometer.was_gesture("shake"):
        display.show(Image.ANGRY)
        sleep(2000)
    else:
        display.show(Image.HAPPY)