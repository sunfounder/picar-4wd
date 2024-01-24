# Test 3 - keeps doing action until you hit enter
import picar_4wd as fc
import time, sys, select

power = 10

actions= [fc.forward, fc.turn_right, fc.forward, fc.turn_right, fc.forward, fc.turn_right, fc.forward, fc.turn_right]

num = 0 
while True:
    time.sleep(1)
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = input()
        break
    actions[num](power)
    num +=1
    if num == 8:
        num = 0

fc.stop()
print("All done")
    