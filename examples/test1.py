import picar_4wd as fc
import time

try:
    fc.forward(25)
    time.sleep(1)
    fc.turn_right(10)
    time.sleep(1)
    fc.turn_right(10)
    time.sleep(1)
    fc.turn_right(10)
    time.sleep(1)
    fc.turn_right(10)
    time.sleep(1)
finally:
    fc.stop()
    time.sleep(0.2)