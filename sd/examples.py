for x in range(100):
    for i in range(1, 5):
        led = pyb.LED(i)
        led.toggle()
        pyb.delay(1000)



for x in range(100):
    for i in range(1, 5):
        led = pyb.LED(i)
        led.on()
        pyb.delay(200)
        led.off()

leds = [pyb.LED(i) for i in range(1, 5)]
for l in leds:
    l.off()

n = 0
try:
   while True:
      n = (n + 1) % 4
      leds[n].toggle()
      pyb.delay(50)
finally:
    for l in leds:
        l.off()


led = pyb.LED(4)
intensity = 0
while True:
    intensity = (intensity + 1) % 255
    led.intensity(intensity)
    pyb.delay(20)


leds = [pyb.LED(i) for i in range(1, 5)]
def all_leds_off():
    for l in leds:
        l.off()

def bubble_level():
    while True:
        a = pyb.Accel()
        print('x={0}, y={1}, z={2}'.format(a.x(), a.y(), a.z()))
        all_leds_off()
        y = a.y()
        if y < -20:
            leds[0].on()
        elif y < -10:
            leds[0].on()
            leds[1].on()
        elif y < -5:
            leds[1].on()
        elif y > 20:
            leds[3].on()
        elif y > 10:
            leds[3].on()
            leds[2].on()
        elif y > 5:
            leds[2].on()
        else:
            leds[1].on()
            leds[2].on()
        pyb.delay(50)

try:
    bubble_level()
finally:
    all_leds_off()


sw = pyb.Switch()
sw.callback(lambda:pyb.LED(1).toggle())

xlights = (pyb.LED(2), pyb.LED(3))
ylights = (pyb.LED(1), pyb.LED(4))

accel = pyb.Accel()
SENSITIVITY = 3

while True:
    x = accel.x()
    if x > SENSITIVITY:
        xlights[0].on()
        xlights[1].off()
    elif x < -SENSITIVITY:
        xlights[1].on()
        xlights[0].off()
    else:
        xlights[0].off()
        xlights[1].off()
    y = accel.y()
    if y > SENSITIVITY:
        ylights[0].on()
        ylights[1].off()
    elif y < -SENSITIVITY:
        ylights[1].on()
        ylights[0].off()
    else:
        ylights[0].off()
        ylights[1].off()
    pyb.delay(100)


tim4 = pyb.Timer(4, freq=10)
tim7 = pyb.Timer(7, freq=20)
tim4.callback(lambda t: pyb.LED(1).toggle())
tim7.callback(lambda t: pyb.LED(2).toggle())


# main.py -- put your code here!
from pyb import UART

uart = UART(1, 9600)                         # init with given baudrate
uart.init(9600, bits=8, stop=1, parity=None) # init with given parameters
pyb.repl_uart(uart)


servo1 = pyb.Servo(1)
servo2 = pyb.Servo(2)

def check_servos(limits1=[50, -50], limits2=[5 ,-90]):
    while True:
        for i in range(2):
            servo1.angle(limits1[i])
            servo2.angle(limits2[i])
            pyb.delay(1000)



from sd.lib.bmp180 import BMP180
bmp = BMP180(side_str='X')
print('temp: {}'.format(bmp.temperature))
print('pressure: {}'.format(bmp.pressure))
print('altitude: {}'.format(bmp.altitude))



import pyb
from ultrasonic import Ultrasonic

def print_distances(trig_pin, echo_pin, count=300, delay=50):
    sonar = Ultrasonic(trig_pin, echo_pin)
    for i in range(count):
        print(sonar.distance_in_cm())
        pyb.delay(delay)

print_distances(pyb.Pin.board.Y3, pyb.Pin.board.Y4)
#print_distances(pyb.Pin.board.Y5, pyb.Pin.board.Y6)

