import pyb

leds = [pyb.LED(i) for i in range(1, 5)]

def main():
    print('rover main')
    for i in range(100):
        for led in leds:
            led.toggle()
            pyb.delay(50)
            led.toggle()
        for led in reversed(leds):
            led.toggle()
            pyb.delay(50)
            led.toggle()
    all_leds_off()


def all_leds_off():
    for l in leds:
        l.off()