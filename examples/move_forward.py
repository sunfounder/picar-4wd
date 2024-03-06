from picar_4wd import Picar4WD
import time

mycar = Picar4WD()

try:
    while True:
        mycar.forward(50)
        time.sleep(1)
finally:
    mycar.stop()
    time.sleep(0.2)