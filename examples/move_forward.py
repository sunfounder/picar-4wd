import picar_4wd as fc
import time

try:
    while True:
        fc.forward(50)
        time.sleep(1)
finally:
    fc.stop()
    time.sleep(0.2)