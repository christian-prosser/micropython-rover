import pyb

from motor_driver import DualMotorDriver

leds = [pyb.LED(i) for i in range(1, 5)]
driver = DualMotorDriver()


def demo_motor():
    driver.demo()


def main():
    print('rover main')
    for i in range(3):
        for led in leds:
            led.toggle()
            pyb.delay(50)
            led.toggle()
        for led in reversed(leds):
            led.toggle()
            pyb.delay(50)
            led.toggle()
    all_leds_off()
    usr_switch = pyb.Switch()
    usr_switch.callback(demo_motor)
    demo_motor()


def all_leds_off():
    for l in leds:
        l.off()
