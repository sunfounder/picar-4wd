# Testing increasing power increments for straight ahead
# interrupt using enter or control C
import picar_4wd as fc
import time, sys, select

power = 5

while True:
    print(f"forward with {power} power")
    time.sleep(5)
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = input()
        break
    fc.forward(power)
    fc.stop()
    power += 5
    if power == 25:
        power = 0

fc.stop()
print("All done")