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
    'y': 0,
    'angle': 0   
}

velocity = {
    'linear': 0.1,    
    'turning': 5     
}

servo_step_angle = 5

def print_map(world_map, car_position):
    # This function prints the map out for visualization and car's positioning
    for row in world_map:
        print("".join(["#" if cell == 1 else " " for cell in row]))
    print(f"Car (X, Y, Angle): ({car_position['x']}, {car_position['y']}, {car_position['angle']})")

def update_car_position(current_position, velocity):
    # Update the current position of the car based on the provided velocity
    current_position['x'] += velocity['linear'] * np.cos(np.radians(current_position['angle']))
    current_position['y'] += velocity['linear'] * np.sin(np.radians(current_position['angle']))
    current_position['angle'] += velocity['turning']

def update_map(picar_map, car_position, threshold):
    for angle in range(0, 181, servo_step_angle):  # Rotate the servo between 0 and 180 degrees at 5 degree increments
        # Get the distance reading from the ultrasonic sensor
        distance = fc.get_distance_at(angle)
        
        # Use distance w/ the radian to calulate the x and y coordinates of the detected object
        angle_rad = np.radians(angle)
        x = int(car_position['x'] + distance * np.cos(angle_rad))
        y = int(car_position['y'] + distance * np.sin(angle_rad))

        # Make sure x and y values are within coordinate map that's defined
        if 0 <= x < map_width and 0 <= y < map_height:
            # If the distance is below the threshold, mark the cell as an obstacle
            if distance <= threshold:
                picar_map[y, x] = 1
    
        # Update car's positioning based on how far it drove
        update_car_position(picar_position, velocity)
        
        # Prints out the map for users to see waht the sensor sees
        print_map(picar_map, picar_position)

# SLAM with ultrasonic sensor
def slam():
    threshold = 100  # Set threshold (can adjust as needed)
    while True:
        update_map(picar_map, picar_position, threshold)
        fc.forward()
        time.sleep(1)
        fc.stop()
        time.sleep(1)

if __name__ == "__main__":
    try: 
        slam()
    finally: 
        fc.stop()
