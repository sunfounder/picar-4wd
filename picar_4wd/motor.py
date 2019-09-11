import threading

class Motor():
    STEP = 10
    DELAY = 0.1
    def __init__(self, pwm_pin, dir_pin, is_reversed=False):
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin
        self._is_reversed = is_reversed
        self._power = 0
        self._except_power = 0
    
    # def start_timer(self):
    #     self.t = threading.Timer(self.DELAY, self.adder_thread)
    #     self.t.start()

    def set_power(self, power):
        if power >= 0:
            direction = 0
        elif power < 0:
            direction = 1
        power = abs(power)
        if power != 0:
            power = int(power /2 ) + 50
        power = power

        direction = direction if not self._is_reversed else not direction  
        self.dir_pin.value(direction)
            
        self.pwm_pin.pulse_width_percent(power)

#     def adder_thread(self):
#         if self._except_power > self._power:
#             step = self.STEP
#         else:
#             step = -self.STEP
#         if abs(self._except_power - self._power) < self.STEP:
#             self._power = self._except_power
#         else:
#             self._power += step
#         self._set_power(self._power)
#         if self._power != self._except_power:
#             self.start_timer()

#     def set_power(self, power):
#         # print("Power: {}".format(power))
#         self._except_power = power
#         if self._power != self._except_power:
#             self.start_timer()

# if __name__ == "__main__":
#     import picar-4wd as fc
#     import time
#     fc.forward(100)
#     time.sleep(1)
