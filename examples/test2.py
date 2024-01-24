import picar_4wd as fc
import time
import sys
import tty
import termios
import asyncio

power_val = 50
key = 'status'
print("Start")
#This doe snot work as intended right now and loops until control c in the terminal, by which time the car has hit an obstacle or
# creeped under various furniture, dragging wires and wreaking havoc

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)


try:
    while True:
        key=readkey()
        if key == 'g':
            fc.stop()
            break
        else:
            fc.forward(50)
            time.sleep(1)
            fc.turn_right(50)
            time.sleep(1)
            fc.turn_right(50)
            time.sleep(1)
            fc.turn_right(50)
            time.sleep(1)
            fc.turn_right(50)
            time.sleep(1)
finally:
    fc.stop()
    time.sleep(0.2)