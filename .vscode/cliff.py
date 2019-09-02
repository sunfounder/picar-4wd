import new_car as nc
import time

cliff_adc_list =[]
speed = 0
global left_danger_flag = 0
global center_danger_flag = 0
global right_danger_flag = 0


def analog_transfrom_digital(c_list):
    danger_flag_list = []
    for i in cliff_adc_list:
        if i >= cliff_value:
            danger_flag_list.append(1)
        else:
            danger_flag_list.append(0)
    return danger_flag_list

def cliff_examine(cliff_value):
    global left_danger_flag 
    global center_danger_flag 
    global right_danger_flag 
    
    cliff_adc_list = analog_transfrom_digital(nc.Get_adc_value())

    if cliff_adc_list = [1,1,1]:
        nc.backward()
        while(max(analog_transfrom_digital(nc.Get_adc_value())))
        nc.turn_back()
    elif cliff_adc_list = [1,0,0] or cliff_adc_list = [1,1,0]:
        nc.turn_right() 
    elif cliff_adc_list = [0,0,1] or cliff_adc_list = [0,1,1]:
        nc.turn_left()    

