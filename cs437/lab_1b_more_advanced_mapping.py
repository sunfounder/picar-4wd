import picar_4wd as fc
import random
import time

# Constants

# Create an 100 x 100 numpy array to be able to do SLAM for advanced mapping with 
# ultrasonic sensor
def main():
    while True:
        scan_list = fc.scan_step(35)
        if not scan_list:
            continue

        tmp = scan_list[3:7]
        print(tmp)
        # If there's an obstacle in the way
        if tmp != [2,2,2,2]:
            print("Obstacle in the way.")
            fc.stop()
            direction = choose_random_direction()
            print(f"Direction selected: {direction}")
            fc.backward(travel_speed)
            time.sleep(1.0)
            fc.stop()
            if direction == "left":
                print(f"Turning {direction}")
                fc.turn_left(turn_speed)
                time.sleep(1.0)
            else:
                print(f"Turning {direction}")
                fc.turn_right(turn_speed)
                time.sleep(1.0)
                
            fc.forward(travel_speed)
        else:
            fc.forward(travel_speed)

if __name__ == "__main__":
    try: 
        main()
    finally: 
        fc.stop()
