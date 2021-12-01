from time import sleep
import board
import analogio           # import library for analog inputs
# import digitalio

sen0 = analogio.AnalogIn(board.A0)  # guess 15cm
sen1 = analogio.AnalogIn(board.A1)  # guess 30cm
sen2 = analogio.AnalogIn(board.A2)  # guess 45cm
# led = digitalio.DigitalInOut(board.LED)
# led.direction = digitalio.Direction.OUTPUT

def get_voltage(pin):
    return (pin.value * 3.3) / 65536
# a = 0
while True:
    v0 = get_voltage(sen0)
    v1 = get_voltage(sen1)
    v2 = get_voltage(sen2)
    # print(v)
    if v0 > 2.55:                   # ball less than 15 cm away
        print("x= less than 15cm, y = 15cm")
        sleep(0.2)
    elif v1 > 2.55:
        print("x= less than 15cm, y = 30cm")
        sleep(0.2)
    elif v2 > 2.55:
        print("x = less than 15cm, y = 45cm")
        sleep(0.2)
    elif v0 < 2.55 and v0 > 1.45:   # ball between 15 cm - 30m away
        print("x = 15-30cm, y = 15cm")
        sleep(0.2)
    elif v1 < 2.55 and v1 > 1.45:
        print("x = 15-30cm, y = 30cm")
        sleep(0.2)
    elif v2 < 2.55 and v2 > 1.45:
        print("x = 15-30cm, y = 45cm")
        sleep(0.2)
    elif v0 < 1.45 and v0 > 1.03:   # ball between 30 cm - 50m away
        print("x = 30-50cm, y = 15cm")
        sleep(0.2)
    elif v1 < 1.45 and v1 > 1.03:
        print("x = 30-50cm, y = 30cm")
        sleep(0.2)
    elif v2 < 1.45 and v2 > 1.03:
        print("x = 30-50cm, y = 45cm")
        sleep(0.2)
    elif v0 < 1.03 and v0 > 0.86:
        print("x= 50-70cm, y = 15cm")
        sleep(0.2)
    elif v1 < 1.03 and v1 > 0.86:
        print("x= 50-70cm, y = 30cm")
        sleep(0.2)
    elif v2 < 1.03 and v2 > 0.86:
        print("x= 50-70cm, y = 45cm")
        sleep(0.2)
    elif v0 < 0.86 and v0 > 0.75:
        print("x = 70-100cm, y = 15cm")
        sleep(0.2)
    elif v1 < 0.86 and v1 > 0.75:
        print("x = 70-100cm, y = 30cm")
        sleep(0.2)
    elif v2 < 0.86 and v2 > 0.75:
        print("x = 70-100cm, y = 45cm")
        sleep(0.2)
    elif v0 < 0.75 and v0 > 0.68:
        print("x = 100-120cm, y = 15cm")
        sleep(0.2)
    elif v1 < 0.75 and v1 > 0.68:
        print("x = 100-120cm, y = 30cm")
        sleep(0.2)
    elif v2 < 0.75 and v2 > 0.68:
        print("x = 100-120cm, y = 45cm")
        sleep(0.2)
    elif v0 < 0.68 and v0 > 0.6:
        print("x = 120-150cm, y = 15cm")
        sleep(0.2)
    elif v0 < 0.68 and v0 > 0.6:
        print("x = 120-150cm, y = 30cm")
        sleep(0.2)
    elif v0 < 0.68 and v0 > 0.6:
        print("x = 120-150cm, y = 45cm")
        sleep(0.2)
    else:
        print("no detection, out of range")
        sleep(0.1)
    # if dist >= 20 and dist <= 150:
        # a = a + 1
        # print(a, "value in cm", dist)
        # led.value = True
        # sleep(0.1)
        # led.value = False
    sleep(0.01)
    # led.value = False
