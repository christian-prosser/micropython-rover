import pyb


class DualMotorDriver:
    """
    SparkFun Dual Motor Driver - TB6612FNG (1A)
    https://www.sparkfun.com/products/9457

    motor A connected between A01 and A02
    motor B connected between B01 and B02
    """

    def __init__(self):
        self._stby = None  # standby
        self._pwma = None  # speed control motor A
        self._ain1 = None
        self._ain2 = None
        self._pwmb = None  # speed control motor B
        self._bin1 = None
        self._bin1 = None

        self._stby.init(pyb.Pin.OUT_PP)
        self._pwma.init(pyb.Pin.OUT_PP)


        timer = pyb.Timer(2, freq=1000)
        ch = timer.channel(1, pyb.Timer.PWM, pin=pyb.Pin('X1'))  # X1 has TIM2, CH1
        ch.pulse_width_percent(50)

        timer = pyb.Timer(2, freq=1000)
        ch2 = timer.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.X2, pulse_width=210000)
        ch3 = timer.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.X3, pulse_width=420000)

        self._ain1.init(pyb.Pin.OUT_PP)
        self._ain2.init(pyb.Pin.OUT_PP)
        self._pwmb.init(pyb.Pin.OUT_PP)
        self._bin1.init(pyb.Pin.OUT_PP)
        self._bin1.init(pyb.Pin.OUT_PP)

    def demo(self):
        self.move(1, 255, 1)  # motor 1, full speed CCW
        self.move(2, 255, 1)  # motor 2, full speed CCW

        pyb.delay(1000)  # go for 1 second
        self.stop()  # stop
        pyb.delay(250)  # hold for 250ms until move again

        self.move(1, 128, 0)  # motor 1, half speed CW
        self.move(2, 128, 0)  # motor 2, half speed CW

        pyb.delay(1000)
        self.stop()
        pyb.delay(250)

    def move(self, motor, speed, direction):
        """
        Move specific motor at speed and direction
        motor: 0 for B 1 for A
        speed: 0 is off, and 255 is full speed
        direction: 0 clockwise, 1 counter-clockwise
        """
        self._stby.high()  # disable standby

        if motor == 1:
            self._ain1.value(direction)
            self._ain2.value(not direction)
            analogWrite(PWMA, speed)
        else:
            self._bin1.value(direction)
            self._bin2.value(not direction)
            analogWrite(PWMB, speed)

    def stop(self):
        self._stby.low()  # enable standby