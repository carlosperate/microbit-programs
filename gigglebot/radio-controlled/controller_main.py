from microbit import *
import radio

# Config
RADIO_CHANNEL = 17
MSG_DEYLAY = 100

# main()
radio.config(channel=RADIO_CHANNEL)
radio.on()

while True:
    # Process inputs, accelerometer is a 10 bit value
    active = 1 if button_a.is_pressed() else 0
    power = ((accelerometer.get_y() // 200) * 200) * -1
    power = max(min(power, 1000), -1000)
    direction = (accelerometer.get_x() // 100) * 100
    direction = max(min(direction, 1000), -1000)
    lights = 1 if button_b.was_pressed() else 0

    # Update display
    display.clear()
    if direction == 0:
        if power > 0:
            display.show(Image.ARROW_N)
        elif power < 0:
            display.show(Image.ARROW_S)
    elif direction > 0:
        if power > 0:
            display.show(Image.ARROW_NE)
        elif power < 0:
            display.show(Image.ARROW_SE)
    elif direction < 0:
        if power > 0:
            display.show(Image.ARROW_NW)
        elif power < 0:
            display.show(Image.ARROW_SW)

    # Send data
    msg_data = [active, power, direction, lights]
    print('[A:{}] [P:{}] [D:{}] [L:{}]'.format(*msg_data))
    radio.send('{}:{}:{}:{}'.format(*msg_data))
    sleep(MSG_DEYLAY)
