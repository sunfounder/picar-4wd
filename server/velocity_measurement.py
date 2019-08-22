import new_car as nc 
import RPi.GPIO as GPIO
import time

# speed_counter_1 = 0
# speed_counter_2 = 0
speed_counter_3 = 0
speed_counter_4 = 0

# now_time_1 = 0
# now_time_2 = 0
now_time_3 = 0
now_time_4 = 0

# angular_speed_1 = 0
# angular_speed_2 = 0
angular_speed_3 = 0
angular_speed_4 = 0

GPIO.setmode(GPIO.BCM)
# GPIO.setup(25, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)#MOTOR 1
# GPIO.setup(4, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)#MOTOR 2
GPIO.setup(16, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)#MOTOR 3
GPIO.setup(12, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)#MOTOR 4

# def my_callback_1(channel):
#     global speed_counter_1,now_time_1,angular_speed_1
#     speed_counter_1 +=1

#     if speed_counter_1 >= 20:
#         last_time_1 = now_time_1
#         now_time_1 = time.time()
#         sub_time_1 = float(now_time_1) - float(last_time_1)
#         angular_speed_1 = 6.28*33 / sub_time_1
#         speed_counter_1 = 0
        
# def my_callback_2(channel):
#     global speed_counter_2,now_time_2,angular_speed_2
#     speed_counter_2 +=1
#     if speed_counter_2 >= 20:
#         last_time_2 = now_time_2
#         now_time_2 = time.time()
#         sub_time_2 = float(now_time_2) - float(last_time_2)
#         angular_speed_2 = 6.28*33 / sub_time_2
#         speed_counter_2 = 0

def my_callback_3(channel):
    global speed_counter_3,now_time_3,angular_speed_3
    speed_counter_3 +=1

    if speed_counter_3 >= 20:
        last_time_3 = now_time_3
        now_time_3 = time.time()
        sub_time_3 = float(now_time_3) - float(last_time_3)
        angular_speed_3 = 6.28*33 / sub_time_3
        speed_counter_3 = 0

def my_callback_4(channel):
    global speed_counter_4,now_time_4,angular_speed_4
    speed_counter_4 +=1

    if speed_counter_4 >= 20:
        last_time_4 = now_time_4
        now_time_4 = time.time()
        sub_time_4 = float(now_time_4) - float(last_time_4)
        angular_speed_4 = 6.28*33 / sub_time_4
        speed_counter_4 = 0

# GPIO.add_event_detect(25, GPIO.RISING, callback=my_callback_1)
# GPIO.add_event_detect(4, GPIO.RISING, callback=my_callback_2)
GPIO.add_event_detect(16, GPIO.RISING, callback=my_callback_3)
GPIO.add_event_detect(12, GPIO.RISING, callback=my_callback_4)


def speed_val():
    speed_list = []
    global angular_speed_3,angular_speed_4
#     speed_list.append(angular_speed_1)
#     speed_list.append(angular_speed_2)
    speed_list.append(int(angular_speed_3))
    speed_list.append(int(angular_speed_4))
    aver_sp = int(sum(speed_list)/2.0)
    speed_list.append(aver_sp)
#     print(speed_list)
    return speed_list

def test():
    print("速度：",speed_val())

if __name__ == "__main__":
    nc.forward(1)
    # nc.stop()
    while 1:
        # speed_counter = 0
        time.sleep(1)
        test()
        

    