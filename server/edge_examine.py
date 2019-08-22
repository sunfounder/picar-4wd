import new_car as nc
import time

edge_adc_list =[]
speed = 0

        
def Edge_examine_func(edge_value,ed_list):
    edge_value = int(edge_value)
   

    if ed_list[2] <= edge_value or ed_list[1] <= edge_value or ed_list[0] <= edge_value:
        nc.backward(20)
        time.sleep(0.5)
        nc.stop()

if __name__ == "__main__":
    while 1:
        nc.forward(1)
        Edge_examine_func(110)