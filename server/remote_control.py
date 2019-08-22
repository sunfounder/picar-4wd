import asyncio
import websockets
import new_car as nc


def Remote_control(control_flag,speed):

    speed = int(speed)

    if control_flag == 'forward':
        nc.forward(speed)
    elif control_flag == 'backward':
        nc.backward(speed)
    elif control_flag == 'turn_left':
        nc.turn_left(speed)
    elif control_flag == 'turn_right':
        nc.turn_right(speed)
    else:
        nc.stop()

# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("Canceled.")
#         cleanup()
    
        
