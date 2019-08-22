from pin import Pin
import time

#复位引脚
soft_reset_pin = Pin("D16")

def soft_reset():
    print('sr')
    soft_reset_pin.low()
    time.sleep(0.001)
    soft_reset_pin.high()
    time.sleep(0.001)

if __name__ == "__main__":
    soft_reset()
    # while 1:
    #     soft_reset()