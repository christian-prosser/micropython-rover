import pyb

MOTOR_A = 0
MOTOR_B = 1
MOTOR_AB = 2
DIR_CW = 0
DIR_CCW = 1
HIGH = 1
LOW = 0
MAX_SPEED = 100


class DualMotorDriver:
    """
    SparkFun Dual Motor Driver - TB6612FNG (1A)
    https://www.sparkfun.com/products/9457

    motor A connected between A01 and A02
    motor B connected between B01 and B02
    """

    def __init__(self, stby_pin=pyb.Pin.board.X17, ain1_pin=pyb.Pin.board.Y6, ain2_pin=pyb.Pin.board.Y5, pwma_pin=pyb.Pin.board.Y7, bin1_pin=pyb.Pin.board.X11, bin2_pin=pyb.Pin.board.X12, pwmb_pin=pyb.Pin.board.Y8):
        self._stby = stby_pin  # standby

        # Motor A
        self._ain1 = ain1_pin
        self._ain2 = ain2_pin
        self._pwma = pwma_pin

        # Motor B
        self._bin1 = bin1_pin
        self._bin2 = bin2_pin
        self._pwmb = pwmb_pin

        self._stby.init(pyb.Pin.OUT_PP)

        self._ain1.init(pyb.Pin.OUT_PP)
        self._ain2.init(pyb.Pin.OUT_PP)

        self._bin1.init(pyb.Pin.OUT_PP)
        self._bin2.init(pyb.Pin.OUT_PP)

        timer = pyb.Timer(12, freq=1000)
        self._pwma_ch = timer.channel(1, pyb.Timer.PWM, pin=self._pwma, pulse_width=210000)
        self._pwmb_ch = timer.channel(2, pyb.Timer.PWM, pin=self._pwmb, pulse_width=420000)

    def demo(self):
        self.move(MOTOR_A, 255, DIR_CCW)  # motor 1, full speed CCW
        self.move(MOTOR_B, 255, DIR_CCW)  # motor 2, full speed CCW

        pyb.delay(1000)  # go for 1 second
        # self.standby()  # enter standby
        # pyb.delay(250)  # hold for 250ms until move again
        #
        self.move(MOTOR_A, 255, DIR_CW)  # motor A, half speed CW
        self.move(MOTOR_B, 255, DIR_CW)  # motor B, half speed CW

        pyb.delay(1000)
        self.stop(MOTOR_AB)
        self.standby()

# | Input                         | Output
# | IN1     IN2     PWM     STBY  | OUT1    OUT2         Mode
# |-------------------------------|---------------------------------
# | H       H       H/L     H     | L       L            Short brake
# | L       H       L       H     | L       L            Short brake
# | H       L       L       H     | L       L            Short brake
# | L       H       H       H     | L       H            CCW
# | H       L       H       H     | H       L            CW
# | L       L       H       H     | OFF (High impedance) Stop
# | H/L     H/L     H/L     L     | OFF (High impedance) Standby

    def start_up(self):
        self._stby.high()  # disable standby

    def short_brake(self, motor):
        self._stby.high()
        if motor in [MOTOR_A, MOTOR_AB]:
            self._ain1.high()
            self._ain2.high()
            self._pwma_ch.pulse_width_percent(LOW)
        if motor in [MOTOR_B, MOTOR_AB]:
            self._bin1.high()
            self._bin2.high()
            self._pwmb_ch.pulse_width_percent(LOW)

    def stop(self, motor, brake_for=50):
        self.short_brake(motor)
        pyb.delay(brake_for)
        if motor in [MOTOR_A, MOTOR_AB]:
            self._ain1.low()
            self._ain2.low()
            self._pwma_ch.pulse_width_percent(100)
        if motor in [MOTOR_B, MOTOR_AB]:
            self._bin1.low()
            self._bin2.low()
            self._pwmb_ch.pulse_width_percent(100)

    def standby(self):
        self._stby.low()  # enable standby

    def move(self, motor, speed, direction=DIR_CW):
        """
        Move specific motor at speed and direction (defaults to clockwise)
        :param motor: 0 for A 1 for B, 2 for both A and B
        :param speed: 0 is off, and 100 is full speed (-ve speed reverses direction)
        :param direction: 0 clockwise, 1 counter-clockwise
        :return:
        """
        self.start_up()

        # -ve speed reverses direction
        if speed < 0:
            direction = not direction
            speed = abs(speed)

        if speed == 0:
            self.short_brake(motor)
            self.stop(motor)
        elif speed > MAX_SPEED:
            speed = MAX_SPEED

        if motor in [MOTOR_A, MOTOR_AB]:
            self._ain1.value(direction)
            self._ain2.value(not direction)
            self._pwma_ch.pulse_width_percent(speed)
        if motor in [MOTOR_B, MOTOR_AB]:
            self._bin1.value(direction)
            self._bin2.value(not direction)
            self._pwmb_ch.pulse_width_percent(speed)
