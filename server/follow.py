import new_car as nc 
import time
from Obstacle_avoidance import *

direction_list = []
five_dis_direction_list = []
dir_flag = 1
bw_safe_counter = 0
fw_safe_counter = 0
# nc.soft_reset()

def dir_weight(dir_list_now):
    dir_weight_list = []
    for i in dir_list_now:
        if i < 23 and i > 0:
            dir_weight_list.append(1)
        else:
            dir_weight_list.append(0)
    return dir_weight_list



def Follow():
    direction_angle_list = [-70,-42,-14,14,42,70]
    # direction_angle_list = [-50,-30,-10,10,30,50]
    rt_angle_list = []
    rt_dis_list = []
    rt_weight_list =[]
    global dir_flag,bw_safe_counter,fw_safe_counter

    # if dir_flag == 1:
    #     for i in range(-70,71):
    #         nc.angle(i)
    #         if i in direction_angle_list:
    #             rt_angle_list.append(i)
    #             rt_dis_list.append(nc.Get_distance(0.01))
    #         time.sleep(0.005)
    #     dir_flag = -1 * dir_flag
    # else:
    #     for i in range(70,-71,-1):
    #         nc.angle(i)
    #         if i in direction_angle_list:  
    #             rt_angle_list.append(i)
    #             rt_dis_list.append(nc.Get_distance(0.01))
    #         time.sleep(0.005)
    #     dir_flag = -1 * dir_flag
    for i in [dir_flag*j for j in direction_angle_list]:
        rt_angle_list = distance_at(i)
        rt_dis_list.append(rt_angle_list[1])
        time.sleep(0.05)
    dir_flag = dir_flag *-1
    print(rt_dis_list)
    rt_weight_list = dir_weight(rt_dis_list)
    rt_weight_list = [str(i) for i in rt_weight_list]
    rt_weight_val = "".join(rt_weight_list)
    if rt_weight_val == '100000' or rt_weight_val == '110000' or rt_weight_val == '111000':
        if rt_angle_list[0] < 0:
            nc.turn_left(50)
        else:
            nc.turn_right(50)
    elif rt_weight_val == '000001' or rt_weight_val == '000011' or rt_weight_val == '000111':
        if rt_angle_list[0] < 0:
            nc.turn_right(50)
        else:
            nc.turn_left(50)
    elif rt_weight_val == '000000':
        nc.stop()
    else:
        if 0 < rt_dis_list[2] < 10 or 0 < rt_dis_list[3] < 10:
            nc.backward(1)
            # bw_safe_counter += 1
            # if bw_safe_counter >= 2:#二次触发，太快防止误操作
            #     nc.backward(1)
            #     bw_safe_counter = 0
        else:
            nc.forward(1)
            # fw_safe_counter += 1
            # if fw_safe_counter >= 2: 
            #     nc.forward(1)
            #     fw_safe_counter = 0

if __name__ == "__main__":
    while 1:
        Follow()
