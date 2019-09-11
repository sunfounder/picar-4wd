import asyncio
import websockets
import picar_4wd as fc



def Remote_control(control_flag,speed=50):
    speed = int(speed)
    if control_flag == 'forward':
        fc.forward(speed)
    elif control_flag == 'backward':
        fc.backward(speed)
    elif control_flag == 'turn_left':
        fc.turn_left(speed)
    elif control_flag == 'turn_right':
        fc.turn_right(speed)
    else:
        fc.stop()

# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("Canceled.")
#         cleanup()
    
        
