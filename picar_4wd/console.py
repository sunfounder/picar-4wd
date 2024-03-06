import os
from .utils import soft_reset, power_read, user_name
import time

# Command line interaction
# ================================================================
def usage(cmd=None):
    general = '''
Usage:  picar-4wd [Command] [option]

Commands:
    soft-reset
    power-read
    web-example
    test
'''
    web_example = '''
Usage: picar-4wd web-example [option]

Options:
      -       start web-example
    enable    Enable start on boot
    disable   Disable start on boot
'''
    test = '''
Usage: picar-4wd test [option]

Options:
    motor           test the motor
    grayscale       test the grayscale
    servo           test the servo and the ultrasonic
'''
    if cmd == None:
        print(general)
    elif cmd == "web-example":
        print(web_example)
    elif cmd == "test":
        print(test)

def destroy():
    # ... some processing
    quit()

def test_motors(mycar):
    print("Motors test start!, Ctrl+C to Stop")
    mycar.forward(50)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
    finally:
        mycar.stop()
        time.sleep(0.1)

def test_grayscale(mycar):
    print("Grayscale module test start!, Ctrl+C to Stop")
    try:
        print(f'033[K{mycar.get_grayscale_list()}')
        while True:
            print(f'\033[A\033[K{mycar.get_grayscale_list()}')
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass

def test_servo(mycar):
    print("Servo and ultrasonic test start!, Ctrl+C to Stop")
    try:
        print(f'\033[K{mycar.us.get_distance()} cm')
        while True:
            for i in range(-90, 90, 1):
                mycar.servo.set_angle(i)
                time.sleep(0.01)
                print(f'\033[A\033[K{mycar.us.get_distance():.02f} cm')

            for i in range(90, -90, -1):
                mycar.servo.set_angle(i)
                time.sleep(0.01)
                print(f'\033[A\033[K{mycar.us.get_distance():.02f} cm')

    except KeyboardInterrupt:
        pass
    finally:
        mycar.servo.set_angle(0)
        time.sleep(0.01)

def console():
    import sys
    # no command
    # ---------------------------------------------
    if len(sys.argv) < 2:
        usage()
        quit()

    # has command
    # ---------------------------------------------
    print("Welcome to SunFounder PiCar-4WD.")
    command = sys.argv[1]

    # -- soft-reset --
    if command == "soft-reset":
        print("soft-reset")
        soft_reset()

    # -- power-read --
    elif command == "power-read":
        print(f"Power voltage: {power_read():0.2f}V")

    # -- web-example --
    elif command == "web-example":
        if len(sys.argv) >= 3:
            opt = sys.argv[2]
            # enable
            if opt == "enable":
                os.system("sudo update-rc.d picar-4wd-web-example defaults")
                print("web-example start on boot is enabled")
            # enable
            elif opt == "disable":
                os.system("sudo update-rc.d picar-4wd-web-example remove")
                print("web-example start on boot is disabled")
            # error command
            else:
                usage(command)
        else:
            # run
            os.system(f"sudo python3 /home/{user_name}/picar-4wd/examples/web/start.py")
    
    # -- test --
    elif command == "test":
        # car init 
        from .car import Picar4WD
        mycar = Picar4WD()

        if len(sys.argv) >= 3:
            opt = sys.argv[2]
            # motor
            if opt == "motor":
                test_motors(mycar)
            # grayscale
            elif opt == "grayscale":
                test_grayscale(mycar)
            # servo
            elif opt == "servo":
                test_servo(mycar)
            # error command
            else:
                usage(command)
        else:
            usage(command)

    # -- error command --
    else:
        print('Command error, "%s" is not in list' % sys.argv[1])
        usage()


# test
if __name__ == '__main__':
    console()
