import picar_4wd as fc

Track_line_speed = 20

def Track_line():
    gs_list = fc.get_grayscale_list()
    if fc.get_line_status(400,gs_list) == 0:
        fc.forward(Track_line_speed) 
    elif fc.get_line_status(400,gs_list) == -1:
        fc.turn_left(Track_line_speed)
    elif fc.get_line_status(400,gs_list) == 1:
        fc.turn_right(Track_line_speed) 

if __name__=='__main__':
    try:
        while True:
            Track_line()
    finally:
        fc.stop()
        print('Program stop')