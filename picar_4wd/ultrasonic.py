import time
from picar_4wd.servo import Servo
from picar_4wd.pwm import PWM
from picar_4wd.pin import Pin

class Ultrasonic():
    ANGLE_RANGE = 180
    STEP = 18

    def __init__(self, trig, echo, timeout=0.01):
        self.timeout = timeout
        self.trig = trig
        self.echo = echo
        # Init Servo
        self.servo = Servo(PWM("P0"), offset=10)
        self.angle_distance = [0,0]
        self.current_angle = 0
        self.max_angle = self.ANGLE_RANGE/2
        self.min_angle = -self.ANGLE_RANGE/2
        self.scan_list = []

    def get_distance(self):
        self.trig.low()
        time.sleep(0.01)
        self.trig.high()
        time.sleep(0.000015)
        self.trig.low()
        pulse_end = 0
        pulse_start = 0
        timeout_start = time.time()
        while self.echo.value()==0:
            pulse_start = time.time()
            if pulse_start - timeout_start > self.timeout:
                return -1
        while self.echo.value()==1:
            pulse_end = time.time()
            if pulse_end - timeout_start > self.timeout:
                return -2
        during = pulse_end - pulse_start
        cm = round(during * 340 / 2 * 100, 2)
        #print(cm)
        return cm

    # def get_distance_at(self, angle):
    #     self.servo.set_angle(angle)
    #     time.sleep(0.04)
    #     distance = self.get_distance()
    #     self.angle_distance = [angle, distance]
    #     return distance

    # def get_status_at(self, angle, ref1=35, ref2=10):
    #     dist = self.get_distance_at(angle)
    #     if dist > ref1 or dist == -2:
    #         return 2
    #     elif dist > ref2:
    #         return 1
    #     else:
    #         return 0

    # def scan_step(self, ref):
    #     if self.current_angle >= self.max_angle:
    #         self.current_angle = self.max_angle
    #         us_step = -self.STEP
    #     elif self.current_angle <= self.min_angle:
    #         self.current_angle = self.min_angle
    #         us_step = self.STEP
    #     self.current_angle += us_step
    #     status = self.get_status_at(self.current_angle, ref1=ref)#ref1避障基准值，ref2跟随小车后退时基准值

    #     self.scan_list.append(status)
    #     if self.current_angle == self.min_angle or self.current_angle == self.max_angle:
    #         if us_step < 0:
    #             # print("reverse")
    #             self.scan_list.reverse()
    #         # print(self.scan_list)
    #         self.scan_list = []
    #         return self.scan_list
    #     else:
    #         return False
