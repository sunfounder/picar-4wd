# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Main script to run the object detection routine."""
import numpy as np
import picar_4wd as fc

import heapq
import argparse
import sys
import time

import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils

def run(model: str, camera_id: int, width: int, height: int, num_threads: int, 
        enable_edgetpu: bool) -> None:
    """Continuously run inference on images acquired from the camera.

    Args:
        model: Name of the TFLite object detection model.
        camera_id: The camera id to be passed to OpenCV.
        width: The width of the frame captured from the camera.
        height: The height of the frame captured from the camera.
        num_threads: The number of CPU threads to run the model.
        enable_edgetpu: True/False whether the model is an EdgeTPU model.
    """

    # Variables to calculate FPS
    counter, fps = 0, 0
    start_time = time.time()

    # Start capturing video input from the camera
    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Visualization parameters
    row_size = 20  # pixels
    left_margin = 24  # pixels
    text_color = (0, 0, 255)  # red
    font_size = 1
    font_thickness = 1
    fps_avg_frame_count = 10

    # Initialize the object detection model
    base_options = core.BaseOptions(
        file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)
    detection_options = processor.DetectionOptions(
        max_results=3, score_threshold=0.3)
    options = vision.ObjectDetectorOptions(
        base_options=base_options, detection_options=detection_options)
    detector = vision.ObjectDetector.create_from_options(options)

    # Continuously capture images from the camera and run inference
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            sys.exit(
                'ERROR: Unable to read from webcam. Please verify your webcam settings.'
            )

        counter += 1
        image = cv2.flip(image, 1)

        # Convert the image from BGR to RGB as required by the TFLite model.
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Create a TensorImage object from the RGB image.
        input_tensor = vision.TensorImage.create_from_array(rgb_image)

        # Run object detection estimation using the model.
        detection_result = detector.detect(input_tensor)

        category_name = ""
        for detection in detection_result.detections:
            # Output the predicted object and probability
            category = detection.categories[0]
            category_name = category.category_name
            probability = round(category.score, 2)
        
        # # Draw keypoints and edges on input image
        # image = utils.visualize(image, detection_result)

            # Calculate the FPS
            if counter % fps_avg_frame_count == 0:
                end_time = time.time()
                fps = fps_avg_frame_count / (end_time - start_time)
                start_time = time.time()

            # Show the FPS
            fps_text = 'FPS = {:.1f}'.format(fps)
            print(f"Detected Object: {category_name}, Probability: {probability}, FPS: {fps_text}")
            text_location = (left_margin, row_size)
            cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN, 
                    font_size, text_color, font_thickness)

        # Display the image
        # cv2.imshow('object_detector', image)
        return str(category_name)

        # Delay to achieve the desired FPS
        time.sleep(0.8)

        # Stop the program if the ESC key is pressed.
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model',
      help='Path of the object detection model.',
      required=False,
      default='efficientdet_lite0.tflite')
  parser.add_argument(
      '--cameraId', help='Id of camera.', required=False, type=int, default=0)
  parser.add_argument(
      '--frameWidth',
      help='Width of frame to capture from camera.',
      required=False,
      type=int,
      default=640)
  parser.add_argument(
      '--frameHeight',
      help='Height of frame to capture from camera.',
      required=False,
      type=int,
      default=480)
  parser.add_argument(
      '--numThreads',
      help='Number of CPU threads to run the model.',
      required=False,
      type=int,
      default=4)
  parser.add_argument(
      '--enableEdgeTPU',
      help='Whether to run the model on EdgeTPU.',
      action='store_true',
      required=False,
      default=False)
  args = parser.parse_args()

  run(args.model, int(args.cameraId), args.frameWidth, args.frameHeight,
      int(args.numThreads), bool(args.enableEdgeTPU))

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




# SLAM with ultrasonic sensor
def self_driving():
    cat_name = main()

    print(str(cat_name)+" ")

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
        self_driving()
    finally:
        fc.stop()