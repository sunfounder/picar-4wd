import picar_4wd as fc
import time
from enum import Enum


# Define enum for holding driving direction, in relation to the destination, which can be defined
# as infinity in the direction of car at its starting position.
class DrivingDirection (Enum):
    towards_destination = 1
    right = 2
    left =3
    away_from_destination = 4

# Set speed of car
speed = 20

# Set starting direction of car as toward destination
direction = DrivingDirection.towards_destination

# Initialise counter for measuring distance
distance_counter = 0

# Execute turn of car
def turn(turning_direction):

    global distance_counter

    # Set time for turning action for a period in seconds which gives a 90 degree turn angle.
    # Different timers needed for left and right turns to maintain consistent turning angle
    turn_left_timer = 0.9
    turn_right_timer = 1

    # Execute turn in direction received in function call and wait for specific time 
    # before stopping
    if turning_direction == 'right':
        fc.turn_right(speed)
        time.sleep(turn_right_timer)

    else:
        fc.turn_left(speed)
        time.sleep(turn_left_timer)
    
    # Stop turn
    fc.stop()

    # Reset distance counter as this is used to ensure car moves a certain distance
    # forward after each turn before attempting a turn towards destination
    distance_counter = 0
    return

# Move car forward and update distance counter each time function is called
def move_forward():
    global distance_counter
    fc.forward(speed)
    distance_counter += 1
    return

# Check ultrasonic scan. Assessing left, centre and right parts of scan for obstacles
# return blocked state object
def check_scan(scan_list, blocked_state):
    if scan_list[0:3] != [ 2, 2, 2]:
        blocked_state['left'] = True
        print("Blocked left")
    else:
        blocked_state['left'] = False

    if scan_list[3:7] != [2, 2, 2, 2]:
        blocked_state['centre'] = True
        print("Blocked centre")
    else:
        blocked_state['centre'] = False
    
    if scan_list[7:10] != [2, 2, 2]:
        blocked_state['right'] = True
        print ("Blocked right")
    else:
        blocked_state['right'] = False
    return blocked_state

# Decide on the action based on the blocked state and the direction of the car
# in relation to the destination
def decide_on_action(blocked_state):

    # Use global variable
    global direction

    # Inital filter on driving direction
    if direction == DrivingDirection.towards_destination:

        if blocked_state['centre']:

            # Check if left or right appears to be clear and
            # if so attempt turn in that direction
            if not blocked_state['left']:
                turn('left')
                direction = DrivingDirection.left
                print("Turning left")
                return

            elif not blocked_state['right']:
                turn('right')
                direction = DrivingDirection.right
                print("Turning right")
                return
        
            else:
                # If no preferred direction then attempt to turn left
                turn('left')
                direction = DrivingDirection.left
                print("Turning left - default action")
                return

        else:
            #If clear in front then drive forward
            move_forward()


    elif direction == DrivingDirection.right:

        # Want to turn left towards destination if possible and car has travelled at least 
        # about a car length forward
        if not blocked_state['left'] and distance_counter >= 2:
            turn('left')
            direction = DrivingDirection.towards_destination
            print("Turning left")
            return
        
        # If cannot turn left continue if possible and if not then turn
        if blocked_state['centre']:

            if not blocked_state['right']:
                turn('right')
                direction = DrivingDirection.away_from_destination
                print("Turning right")
                return
        
            else:
                turn('left')
                direction = DrivingDirection.towards_destination
                print("Turning left - default action")
                return

        else:
            #If clear in front then drive forward
            move_forward()

    elif direction == DrivingDirection.left:
        print("In driving direction left")

        # Want to turn right towards destination if possible and car has travelled at least 
        # about a car length forward
        if not blocked_state['right'] and distance_counter >= 2:
            turn('right')
            direction = DrivingDirection.towards_destination
            print("Turning right")
            return

        # If cannot turn right continue if possible and if not then turn
        if blocked_state['centre']:

            if not blocked_state['left']:
                turn('left')
                direction = DrivingDirection.away_from_destination
                print("Turning left")
                return
        
            else:
                turn('right')
                direction = DrivingDirection.towards_destination
                print("Turning right - default action")
                return

        else:
            #If clear in front then drive forward
            move_forward()

    elif direction == DrivingDirection.away_from_destination:
        print("In driving direction - away from destination")

        # Want to turn right or left back towards destination if possible and car has travelled at least 
        # about a car length forward
        if not blocked_state['right'] and distance_counter >= 2:
            turn('right')
            direction = DrivingDirection.left
            print("Turning right")
            return

        if not blocked_state['left'] and distance_counter >= 2:
            turn('left')
            direction = DrivingDirection.right
            print("Turning left")
            return

        # If cannot turn right continue if possible and if not then turn
        if blocked_state['centre']:
            turn('right')
            direction = DrivingDirection.towards_destination
            print("Turning right - default action")
            return

        else:
            #If clear in front then drive forward
            move_forward()
    else:
        return 

def main():

    # Initate dictionary to hold detected obstacle location in front of car
    blocked_state = {
        'left': False,
        'centre': False,
        'right': False
    }

    # Start loop to perform scan and take respective actions
    while True:
        # Get ultrasonic scan input 
        scan_list = fc.scan_step(35)
        if not scan_list:
            continue
        # Wait for full scan to be received from the sensor
        if len(scan_list) != 10:
            continue
        
        # Check for obstacles
        blocked_state = check_scan(scan_list, blocked_state)
        print ("Blocked state ", blocked_state)

        #Decide on actions based on obstacles and current driving direction
        decide_on_action(blocked_state)


if __name__ == "__main__":

    try: 
        main()
    finally: 
        fc.stop()
