import picar_4wd as fc
import random
import time

# Constances
speed = 30
distance_threshold = 35 # 35 cm for now

# Function to get left or right direction randomly
def choose_random_direction():
    return random.chioce(["left"], ["right"])

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
            fc.backward(speed)
            time.sleep(1.0)
            fc.stop()
            if direction == "left":
                fc.turn_left(speed)
                time.sleep(1.0)
            else:
                fc.turn_right(speed)
                time.sleep(1.0)
                
            fc.forward(speed)
        else:
            fc.forward(speed)

if __name__ == "__main__":
    try: 
        main()
    finally: 
        fc.stop()
