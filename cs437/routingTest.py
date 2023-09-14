import numpy as np
import time
import picar_4wd as fc

import heapq

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

def update_local_map():
    
    for x in range(60):
        local_map = update_map(picar_position, 100)
    car_x = picar_position['x']
    car_y = picar_position['y']

    #local_map[car_x][car_y] = '5'


    #buffered_local_map = add_buffer(add_buffer(add_buffer(local_map)))
    
    print_map(local_map, picar_position)
    #print_map(buffered_local_map, picar_position)


    
    




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
        time.sleep(1)
    elif current_angle <= -180:
        current_angle = -180
        us_step = servo_step_angle  # Reverse direction
         # Clear the map at the beginning of each scan
        picar_map = np.zeros((map_width, map_height), dtype=int)
       # fc.forward(velocity['linear'])
        time.sleep(1)
        #fc.stop()
        #time.sleep(1)
        #update_car_position(picar_position, velocity)

    # Clear the console and print the current state of the map and robot's pose
    clear_console()
    #print_map(picar_map, picar_position)
    return picar_map


movements = [(1, 0, "down"), (-1, 0, "up"), (0, 1, "right"), (0, -1, "left")]



def heuristic(current, goal):
    # Calculate the Manhattan distance as the heuristic
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

def astar_search(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_set = []  # Priority queue of nodes to be evaluated
    closed_set = set()  # Set of nodes already evaluated
    came_from = {}  # Dictionary to store the path
    move_directions = {}  # Dictionary to store moves
    
    # Initialize the open set with the starting node
    heapq.heappush(open_set, (0, start))
    
    # Initialize scores for each node to infinity
    g_score = {position: float('inf') for row in grid for position in row}
    g_score[start] = 0
    
    # Main A* loop
    while open_set:
        current_g, current_node = heapq.heappop(open_set)
        
        if current_node == goal:
            # Reconstruct the path if the goal is reached
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start)
            path = path[::-1]  # Return the path in the correct order
            return path, move_directions
        
        closed_set.add(current_node)
        
        for dr, dc, direction in movements:
            r, c = current_node[0] + dr, current_node[1] + dc
            neighbor = (r, c)
            
            c = int(c)
            
            if 0 <= r < rows and 0 <= c < cols and grid[r][c] != 1 and neighbor not in closed_set:
                tentative_g_score = g_score[current_node] + 1
                
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))
                    
                    # Store the move direction
                    move_directions[neighbor] = direction
    
    return None, None  # If no path is found

def add_buffer(grid):
    rows, cols = len(grid), len(grid[0])
    new_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                # Set the current cell to 1
                new_grid[r][c] = 1

                # Set neighboring cells to 1 (within bounds)
                for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        new_grid[nr][nc] = 1

    return new_grid



def test():
    update_local_map()

# SLAM with ultrasonic sensor
def run():
    threshold = 100  # Set threshold (can adjust as needed)
    while True:
        updated_map = update_map(picar_position, threshold)
        
        buffered_map = add_buffer(add_buffer(add_buffer(updated_map)))
        
        for row in buffered_map:
            for elem in row:
                print(elem,end="")
            print()

        start = (map_height-1,map_width/2)
        goal = (0,map_width/2)
        
        
        if current_angle == 180:
            path, move_directions = astar_search(buffered_map, start, goal)
            if path:
                moves = list(move_directions.values())
                moves = moves[0:3]
                print(moves)
                for move in moves:
                    if move == "up":
                        print("move forward")
                        fc.forward(3)
                        time.sleep(1)
                        fc.stop()
                    elif move == "down":
                        print("move backward")
                        fc.backward(3)
                        time.sleep(1)
                        fc.stop()
                    elif move == "left":
                        print("turn left")
                        fc.turn_left(20)
                        time.sleep(1)
                        print("move forward")
                        fc.forward(20)
                        time.sleep(1)
                        fc.stop()
                    elif move == "right":
                        print("turn right")
                        fc.turn_right(20)
                        time.sleep(1)
                        print("move forward")
                        fc.forward(20)
                        time.sleep(1)
                        fc.stop()
                time.sleep(5)

        
       # update_car_position(picar_position, velocity)
        #(picar_position)

if __name__ == "__main__":
    try:
        test()
    finally:
        fc.stop()
