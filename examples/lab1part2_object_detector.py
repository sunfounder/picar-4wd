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

# Adapted for use in UIUC CS 437 IOT under the Apache 2.0 licence

import sys
import time
import numpy as np
import cv2
import atexit
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision

class Object_detector:
  def __init__(self, model: str, camera_id: int, width: int, height: int, num_threads: int,
        enable_edgetpu: bool):
    """
    Args:
      model: Name of the TFLite object detection model.
      camera_id: The camera id to be passed to OpenCV.
      width: The width of the frame captured from the camera.
      height: The height of the frame captured from the camera.
      num_threads: The number of CPU threads to run the model.
      enable_edgetpu: True/False whether the model is a EdgeTPU model.
    """
    # Store parameters as class members
    self.model = model
    self.camera_id = camera_id
    self.width = width
    self.height = height
    self.num_threads = num_threads
    self.enable_edgetpu = enable_edgetpu

    # Variables to calculate FPS
    self.counter, self.fps = 0, 0
    self.start_time = time.time()

    # Create capture object
    self.cap = cv2.VideoCapture(self.camera_id)
    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Stream visualization parameters
    self.row_size = 20  # pixels
    self.left_margin = 24  # pixels
    self.text_color = (0, 0, 255)  # red
    self.font_size = 2
    self.font_thickness = 2
    self.fps_avg_frame_count = 10

    # Bounding box visualization parameters
    self._MARGIN = 10  # pixels
    self._ROW_SIZE = 10  # pixels
    self._FONT_SIZE = 2
    self._FONT_THICKNESS = 2
    self._TEXT_COLOR = (0, 0, 255)  # red

    # Initialize the object detection model
    base_options = core.BaseOptions(
        file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)
    detection_options = processor.DetectionOptions(
        max_results=3, score_threshold=0.3)
    options = vision.ObjectDetectorOptions(
        base_options=base_options, detection_options=detection_options)
    self.detector = vision.ObjectDetector.create_from_options(options)

    # Register the cleanup method to make sure
    # that we release the capture when object exits
    atexit.register(self.cleanup)

  def process_frame(self):
    """
    Process a single frame of the camera input stream for object
      detection. Requires that camera capture is already open.
    """
    # Make sure capture is open
    assert (self.cap.isOpened()),'ERROR: Cannot process frame; Capture not open.'

    # Make sure capture is open
    success, image = self.cap.read()
    assert (success),'ERROR: Unable to read from webcam. Please verify your webcam settings.'

    # increment frame counter
    self.counter += 1
    image = cv2.flip(image, 1)

    # Convert the image from BGR to RGB as required by the TFLite model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create a TensorImage object from the RGB image.
    input_tensor = vision.TensorImage.create_from_array(rgb_image)

    # Run object detection estimation using the model.
    detection_result = self.detector.detect(input_tensor)

    # Draw keypoints and edges on input image
    image = self.draw_bounding_box(image, detection_result)

    # Calculate the FPS
    if self.counter % self.fps_avg_frame_count == 0:
      end_time = time.time()
      self.fps = self.fps_avg_frame_count / (end_time - self.start_time)
      self.start_time = time.time()

    # Show the FPS
    fps_text = 'FPS = {:.1f}'.format(self.fps)
    text_location = (self.left_margin, self.row_size)
    cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                self.font_size, self.text_color, self.font_thickness)

    cv2.imshow('object_detector', image)
    cv2.waitKey(1)

  def draw_bounding_box(
      self, image: np.ndarray,
      detection_result: processor.DetectionResult,
  ) -> np.ndarray:
    """Draws bounding boxes on the input image and returns it.

    Args:
      image: The input RGB image.
      detection_result: The list of all "Detection" entities to be visualized.

    Returns:
      Image with bounding boxes.
    """
    for detection in detection_result.detections:
      # Draw bounding_box
      bbox = detection.bounding_box
      start_point = bbox.origin_x, bbox.origin_y
      end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
      cv2.rectangle(image, start_point, end_point, self._TEXT_COLOR, 3)

      # Draw label and score
      category = detection.categories[0]
      category_name = category.category_name
      probability = round(category.score, 2)
      result_text = category_name + ' (' + str(probability) + ')'
      text_location = (self._MARGIN + bbox.origin_x,
                      self._MARGIN + self._ROW_SIZE + bbox.origin_y)
      cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                  self._FONT_SIZE, self._TEXT_COLOR, self._FONT_THICKNESS)

    return image

  def cleanup(self):
    self.cap.release()
    cv2.destroyAllWindows()
