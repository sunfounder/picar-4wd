import time
from math import pi
from threading import Thread, Timer
from gpiozero import Button

class Speed():
    PERIOD = 0.2 # 200ms
    HOLE_NUM = 20 # Number of code plate holes
    WHEEL_D = 6.6 # wheel diameter / cm
    WHEEL_C =  pi*WHEEL_D # wheel circumference
    # print(f'wheel circumference: {WHEEL_C}')

    def __init__(self, pin):
        self.count = 0
        self.speed = 0

        self.pin_num = pin
        self.pin = Button(self.pin_num, pull_up=True)
        self.pin.when_pressed = self.irq_falling_handler
        self.timer = Timer(interval=self.PERIOD, function=self.timer_callback)
        self.timer.daemon = True

    def irq_falling_handler(self):
        # print("irq_falling")
        self.count += 1

    def timer_callback(self):
        # print(f"timer_callback {time.time()}")
        # laps: rounds / s
        rps = self.count / float(self.HOLE_NUM) / self.PERIOD
        # print(f"rps: {rps}")
        # speed: cm/s
        self.speed = rps * self.WHEEL_C
        # clear count
        self.count = 0
        # repeat
        self.timer = Timer(interval=self.PERIOD, function=self.timer_callback)
        self.timer.daemon = True
        self.timer.start()

    def start(self):
        self.timer.start()

    def __call__(self):
        return self.speed

    def deinit(self):
        self.pin.when_pressed = None
        self.pin.close()
        self.pin.pin_factory.close()


if __name__ == '__main__':
    from picar_4wd import forward, stop
    from picar_4wd import  left_rear_speed, start_speed_thread

    # l_speed = Speed(25)
    # l_speed.start()
    # r_speed = Speed(4)
    # r_speed.start()

    start_speed_thread()
    forward(50)
    try:
        while True:
            # print(l_speed, r_speed)
            print(f"{left_rear_speed():0.2f} cm/s")
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        stop()

