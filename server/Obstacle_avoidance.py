import new_car as nc
import time
import math
from pin import Pin

dir_flag = 1
web_csb_val_list = []
add_count = 0
us_angle = 0
us_step_base = 18
us_list = []
base_speed = 30
right_speed = base_speed
left_speed = base_speed
us_scan_angle = 180


us_step = us_step_base
us_scan_angle = us_scan_angle / 2

def pre_obstacle_avoidance(motor=True, mode=0):
    # mode = 0: Ovoid Obstacle; mode = 1: follow
    global us_angle, us_step, us_list, base_speed, right_speed, left_speed
    
    if mode == 0:
        ref = 35
    elif mode == 1:
        ref = 23
    
    if us_angle >= us_scan_angle:
        us_angle = us_scan_angle
        us_step = -us_step_base
    elif us_angle <= -us_scan_angle:
        us_angle = -us_scan_angle
        us_step = us_step_base
    us_angle += us_step
    status = distance_status_at(us_angle, ref1=ref, ref2=10)#ref1避障基准值，ref2跟随小车后退时基准值
    
    if motor:#是否启动电机
        us_list.append(status)
        if us_angle == -us_scan_angle or us_angle == us_scan_angle:
            if us_step < 0:
                # print("reverse")
                us_list.reverse()
            # print(us_list)
            if mode == 0:#模式0位避障模式
                tmp = us_list[4:7]
                print(tmp)
                if tmp != [2,2,2]:
                    right_speed = -base_speed
                    left_speed = base_speed
                else:
                    right_speed = base_speed
                    left_speed = base_speed
            elif mode == 1:#模式1跟随模式
                us_list = [str(i) for i in us_list]
                us_list = "".join(us_list)
                paths = us_list.split("2")
                length_list = []
                for path in paths:
                    length_list.append(len(path))
                # print(length_list)
                if max(length_list) == 0:
                    right_speed = 0
                    left_speed = 0
                else:
                    i = length_list.index(max(length_list))
                    pos = us_list.index(paths[i])
                    pos += (len(paths[i]) - 1) / 2
                    # pos = int(pos)
                    delta = len(us_list) / 3
                    # delta *= us_step/abs(us_step)
                    if pos < delta:
                        right_speed = -base_speed
                        left_speed = base_speed
                    elif pos > 2 * delta:
                        right_speed = base_speed
                        left_speed = -base_speed
                    else:
                        if us_list[3] == "0":
                            right_speed = -base_speed
                            left_speed = -base_speed
                        else:
                            right_speed = base_speed
                            left_speed = base_speed
            us_list = []
        nc.set_motor_speed(1, left_speed)
        nc.set_motor_speed(2, right_speed)
        nc.set_motor_speed(3, left_speed)
        nc.set_motor_speed(4, -1*right_speed)

def get_dir(base_speed, delta):
    right_speed = base_speed
    left_speed = base_speed
    weight = base_speed * 2 / 5
    if delta < 0:
        right_speed += (delta * weight)
    elif delta > 0:
        left_speed -= (delta * weight)
    return left_speed, right_speed

def distance_at(angle):
    global web_csb_val_list,add_count
    web_csb_val_list = []
    distance_at_list = []
    nc.angle(angle)
    time.sleep(0.04)
    distance_at_list.append(angle)
    csb_dis = nc.Get_distance(0.01)
    distance_at_list.append(csb_dis)
    web_csb_val_list = distance_at_list
    return distance_at_list

def distance_status_at(angle, ref1=35, ref2=10):
    _, dist = distance_at(angle)
    if dist > ref1 or dist == -2:
        return 2
    elif dist > ref2:
        return 1
    else:
        return 0

def radar_screening(angle_min,angle_max):
    global dir_flag,web_csb_val_list
    # nc.angle(angle_min)
    # time.sleep(1)
    radar_screening_val = []
    # for i in range(angle_min,angle_max):
    for i in [dir_flag*j for j in range(angle_min,angle_max+6,6)]:
        null_list = distance_at(i)
        radar_screening_val.append(null_list)
    dir_flag = dir_flag *-1
    return radar_screening_val
    # else:
    #     nc.angle(angle_max)
    #     time.sleep(1)
    #     radar_screening_val = []
    #     for i in range(angle_max,angle_min,-1):
    #         null_list = []
    #         web_csb_val_list = []
    #         nc.angle(i)
    #         time.sleep(0.005)
    #         null_list.append(i)
    #         csb_dis = nc.Get_distance()
    #         null_list.append(csb_dis)
    #         web_csb_val_list.append(i)
    #         web_csb_val_list.append(csb_dis)
    #         # print(web_csb_val_list)
    #         radar_screening_val.append(null_list)
    #     dir_flag = dir_flag *-1
    #     return radar_screening_val 

def test():
    while 1:
        # print(distance_at(-50))
        pre_obstacle_avoidance(mode=1)#1
        # radar_screening(-90,90)

if __name__ == "__main__":
    test()
