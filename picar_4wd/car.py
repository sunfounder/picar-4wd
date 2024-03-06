from .pwm import PWM
from .adc import ADC
from .pin import Pin
from .motor import Motor
from .servo import Servo
from .ultrasonic import Ultrasonic
from .speed import Speed
from .filedb import FileDB
import time


class Picar4WD():
    RADAR_ANGLE_RANGE = 180
    RADAR_STEP = 18
    RADAR_MAX_ANGLE = RADAR_ANGLE_RANGE / 2
    RADAR_MIN_ANGLE = -RADAR_MAX_ANGLE

    def __init__(self):

        # soft_reset
        # print('soft_reset mcu')
        from .utils import soft_reset
        soft_reset()
        time.sleep(0.2)

        # -- variables --
        self.angle_distance = [0, 0]
        self.current_angle = 0
        self.scan_list = []
        self.radar_direction = 1

        # -- offset config --
        config = FileDB("config")
        self.left_front_reverse = config.get('left_front_reverse',
                                             default_value=False)
        self.right_front_reverse = config.get('right_front_reverse',
                                              default_value=False)
        self.left_rear_reverse = config.get('left_rear_reverse',
                                            default_value=False)
        self.right_rear_reverse = config.get('right_rear_reverse',
                                             default_value=False)
        self.servo_offset = int(
            config.get('ultrasonic_servo_offset', default_value=0))

        # -- motors init ---
        self.left_front = Motor(PWM("P13"),
                                Pin("D4"),
                                is_reversed=self.left_front_reverse)  # motor 1
        self.right_front = Motor(
            PWM("P12"), Pin("D5"),
            is_reversed=self.right_front_reverse)  # motor 2
        self.left_rear = Motor(PWM("P8"),
                               Pin("D11"),
                               is_reversed=self.left_rear_reverse)  # motor 3
        self.right_rear = Motor(PWM("P9"),
                                Pin("D15"),
                                is_reversed=self.right_rear_reverse)  # motor 4

        # -- servo init --
        self.servo = Servo(PWM("P0"), offset=self.servo_offset)

        # -- speed measurement module init --
        self.left_rear_speed = Speed(25)
        self.right_rear_speed = Speed(4)

        # -- grayscale module init --
        self.gs0 = ADC('A5')
        self.gs1 = ADC('A6')
        self.gs2 = ADC('A7')

        # -- ultrasonic module init --
        self.us = Ultrasonic(Pin('D8'), Pin('D9', pull=Pin.PULL_UP))

    # motors control
    # =================================================================
    def forward(self, power):
        self.left_front.set_power(power)
        self.left_rear.set_power(power)
        self.right_front.set_power(power)
        self.right_rear.set_power(power)

    def backward(self, power):
        self.left_front.set_power(-power)
        self.left_rear.set_power(-power)
        self.right_front.set_power(-power)
        self.right_rear.set_power(-power)

    def turn_left(self, power):
        self.left_front.set_power(-power)
        self.left_rear.set_power(-power)
        self.right_front.set_power(power)
        self.right_rear.set_power(power)

    def turn_right(self, power):
        self.left_front.set_power(power)
        self.left_rear.set_power(power)
        self.right_front.set_power(-power)
        self.right_rear.set_power(-power)

    def stop(self):
        self.left_front.set_power(0)
        self.left_rear.set_power(0)
        self.right_front.set_power(0)
        self.right_rear.set_power(0)

    def set_motor_power(self, motor, power):
        if motor == 1:
            self.left_front.set_power(power)
        elif motor == 2:
            self.right_front.set_power(power)
        elif motor == 3:
            self.left_rear.set_power(power)
        elif motor == 4:
            self.right_rear.set_power(power)

    # speed measurement
    # =================================================================
    def start_speed_thread(self):
        self.left_rear_speed.start()
        self.right_rear_speed.start()

    def speed_val(self):
        return (self.left_rear_speed() + self.right_rear_speed()) / 2.0

    # grayscale
    # =================================================================
    def get_grayscale_list(self):
        adc_value_list = []
        adc_value_list.append(self.gs0.read())
        adc_value_list.append(self.gs1.read())
        adc_value_list.append(self.gs2.read())
        return adc_value_list

    def is_on_edge(self, ref, gs_list):
        ref = int(ref)
        if gs_list[2] <= ref or gs_list[1] <= ref or gs_list[0] <= ref:
            return True
        else:
            return False

    def get_line_status(self, ref, fl_list):
        ref = int(ref)
        if fl_list[1] <= ref:
            return 0

        elif fl_list[0] <= ref:
            return -1

        elif fl_list[2] <= ref:
            return 1

    # radar (servo + ultrasonic)
    # =================================================================
    def get_distance_at(self, angle):
        self.servo.set_angle(angle)
        time.sleep(0.04)
        self.current_angle = angle
        self.distance = self.us.get_distance()
        self.angle_distance = [angle, self.distance]
        return self.distance

    def get_status_at(self, angle, ref1=35, ref2=10):
        dist = self.get_distance_at(angle)
        if dist > ref1:
            return 2
        elif dist > ref2:
            return 1
        else:
            return 0

    def scan_step(self, ref):
        # -- calculate angle --
        self.current_angle += self.radar_direction * self.RADAR_STEP
        if self.current_angle >= self.RADAR_MAX_ANGLE:
            self.current_angle = self.RADAR_MAX_ANGLE
            self.radar_direction = -1
        elif self.current_angle <= self.RADAR_MIN_ANGLE:
            self.current_angle = self.RADAR_MIN_ANGLE
            self.radar_direction = 1

        # -- get status --
        status = self.get_status_at(self.current_angle, ref1=ref)

        # -- scan_list --
        self.scan_list.append(status)
        # scan compelete
        if self.current_angle == self.RADAR_MIN_ANGLE or self.current_angle == self.RADAR_MAX_ANGLE:
            if self.radar_direction < 0:
                self.scan_list.reverse()
            tmp = self.scan_list.copy()
            self.scan_list = []
            return tmp
        else:
            return False

    # __del__ handler
    # =================================================================
    def all_pins_deinit(self):
        print("all_pins_deinit")
        self.left_rear_speed.deinit()
        self.right_rear_speed.deinit()
        self.us.deinit()
        self.left_front.deinit()
        self.right_front.deinit()
        self.left_rear.deinit()
        self.right_rear.deinit()

    # def __del__(self) -> None:
    #     print(f"del Picar4WD = 0x{id(self):x}")
    #     self.all_pins_deinit()
