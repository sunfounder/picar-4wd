import new_car as nc
import time

edge_adc_list =[]
speed = 20
line_value_list = []


def follow_line_func(aim_val,ad_list):#170<x<300

    aim_val = int(aim_val)
    if ad_list[1] <= aim_val:
        nc.forward(speed)
    
    elif ad_list[0] <= aim_val:
        nc.turn_left(speed)

    elif ad_list[2] <= aim_val:
        nc.turn_right(speed)    


if __name__ == "__main__":
    while 1:
        follow_line_func(1,400)