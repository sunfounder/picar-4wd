import numpy as np
import picar_4wd as fc

# Initialize the map
map_width = 100
map_height = 100
picar_map = np.zeros((map_width, map_height), dtype=int)

def print_map(world_map):
    # This function prints the map out for visualization
    for row in world_map:
        print("".join(["#" if cell == 1 else " " for cell in row]))

def update_map(picar_map, car_position, threshold):
    for angle in range(0, 181, 5):  # Rotate the servo between 0 and 180 degrees at 5 degree increments
        # Get the distance reading from the ultrasonic sensor
        distance = fc.get_distance_at(angle)
        
        # Use distance w/ the radian to calulate the x and y coordinates of the detected object
        angle_rad = np.radians(angle)
        x = int(car_position[0] + distance * np.cos(angle_rad))
        y = int(car_position[1] + distance * np.sin(angle_rad))

        # Make sure x and y values are within coordinate map that's defined
        if 0 <= x < map_width and 0 <= y < map_height:
            # If the distance is below the threshold, mark the cell as an obstacle
            if distance <= threshold:
                picar_map[y, x] = 1
    
        # Prints out the map for users to see waht the sensor sees
        print_map(picar_map)

# SLAM with ultrasonic sensor
def slam():
    # Initialize picar's position
    car_position = (0, 0)
    threshold = 100  # Set threshold (can adjust as needed)
    while True:
        update_map(picar_map, car_position, threshold)

if __name__ == "__main__":
    try: 
        slam()
    finally: 
        fc.stop()
