import asyncio
import websockets
import fwd_car as fc



def Remote_control(control_flag,speed=50):
    # control_flag = #$#$%
    speed = int(speed)
    if control_flag == 'forward':
        fc.forward(speed)
    elif control_flag == 'backward':
        fc.backward(speed)
        # mode_choice_func()
    elif control_flag == 'turn_left':
        fc.turn_left(speed)
        # mode_choice_func()
    elif control_flag == 'turn_right':
        fc.turn_right(speed)
        # mode_choice_func()
    else:
        fc.stop()

# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("Canceled.")
#         cleanup()
    
        
