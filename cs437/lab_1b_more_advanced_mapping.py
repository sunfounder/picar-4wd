import numpy as np
import time
import picar_4wd as fc

# Initialize the map
map_width = 100
map_height = 100
picar_map = np.zeros((map_width, map_height), dtype=int)

# Initialize picar's positioning as well as its speed for movement/turning
picar_position = {
    'x': 0,
    'y':50,
    'angle': 0
}

velocity = {
    'linear': 0.1,
    'turning': 5
}

servo_step_angle = 5
current_angle = -180
us_step = servo_step_angle

def clear_console():
    # Function to clear the console (for updating the display)
    import os
    os.system('clear' if os.name == 'posix' else 'cls')

def print_map(world_map, car_position):
    # This function prints the map out for visualization and car's positioning
    for y in range(map_height):
        row = ''
        for x in range(map_width):
            if x == int(car_position['x']) and y == int(car_position['y']):
                row += 'R'  # Represent robot with 'R'
            elif world_map[-y, x] == 1:
                row += '1'  # Represent obstacles with 'X'
            else:
                row += '0'  # Empty space
        print(row)
    print(f"Car (X, Y, Angle): ({car_position['x']}, {car_position['y']}, {car_position['angle']})")

def update_car_position(current_position, velocity):
    # Update the current position of the car based on the provided velocity
    current_position['x'] += velocity['linear'] * np.cos(np.radians(current_position['angle']))
    # current_position['y'] += velocity['linear'] * np.sin(np.radians(current_position['angle']))
    # current_position['angle'] += velocity['turning']

def update_map(car_position, threshold):
    global current_angle, us_step, picar_map # Declare current_angle and us_step as global variables
    # for angle in range(-181, 181, servo_step_angle):  # Rotate the servo between 0 and 180 degrees at 5 degree increments
    # Get the distance reading from the ultrasonic sensor
    distance = fc.get_distance_at(current_angle)

    # Use distance with the radian to calculate the x and y coordinates of the detected object
    angle_rad = np.radians(current_angle)
    x = int(car_position['x'] + distance * np.cos(angle_rad))
    y = int(car_position['y'] + distance * np.sin(angle_rad))

    # Make sure x and y values are within the coordinate map that's defined
    if 0 <= x < map_width and 0 <= y < map_height:
        # If the distance is below the threshold, mark the cell as an obstacle
        if distance <= threshold:
            picar_map[y, x] = 1

    # Increment the servo angle by us_step
    current_angle += us_step

    # Check if the servo angle has reached the limits
    if current_angle >= 180:
        current_angle = 180
        us_step = -servo_step_angle  # Reverse direction
         # Clear the map at the beginning of each scan
        picar_map = np.zeros((map_width, map_height), dtype=int)
    elif current_angle <= -180:
        current_angle = -180
        us_step = servo_step_angle  # Reverse direction
         # Clear the map at the beginning of each scan
        picar_map = np.zeros((map_width, map_height), dtype=int)
        fc.forward(velocity['linear'])
        time.sleep(1)
        fc.stop()
        time.sleep(1)
        update_car_position(picar_position, velocity)

    # Clear the console and print the current state of the map and robot's pose
    clear_console()
    print_map(picar_map, picar_position)

# SLAM with ultrasonic sensor
def slam():
    threshold = 100  # Set threshold (can adjust as needed)
    while True:
        update_map(picar_position, threshold)
        # update_car_position(picar_position, velocity)
        # print(picar_position)

if __name__ == "__main__":
    try:
        slam()
    finally:
        fc.stop()
