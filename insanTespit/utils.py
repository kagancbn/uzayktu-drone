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
"""Utility functions to display the pose detection results."""

import cv2
import numpy as np
from tflite_support.task import processor
import hareketler.genelHareketler as genelHareketler
from dronekit import VehicleMode
import time

# servo motor icin
import servo

_MARGIN = 10  # pixels
_ROW_SIZE = 10  # pixels
_FONT_SIZE = 1
_FONT_THICKNESS = 1
_TEXT_COLOR = (0, 0, 255)  # red

def kameraGecikmesi(iha):
  # görüntü geç geldiği için her hareket edildiğinde durma -> *todo süre test edilecek
  iha.mode = VehicleMode("BRAKE")
  time.sleep(5)
  iha.mode = VehicleMode("GUIDED") # -> *todo guided sleep üstüne eklenebilir 


def visualize(
    image: np.ndarray,
    detection_result: processor.DetectionResult,
    iha
) -> np.ndarray: #return type of the function
  """Draws bounding boxes on the input image and return it.

  Args:
    image: The input RGB image.
    detection_result: The list of all "Detection" entities to be visualize.

  Returns:
    Image with bounding boxes.
  """
  for detection in detection_result.detections:
    ## test ##
    #print(detection)
    
    # eğer araç tarama modundaysa durdur
    if(iha.mode == VehicleMode("AUTO")):
      # taramayı durdur
      genelHareketler.dur(iha)
      iha.mode = VehicleMode("GUIDED")
      time.sleep(1)
      # biraz geri git (?) ->
      genelHareketler.geri(iha,time=2, hiz=5) # -> *todo test edilecek

      #genelHareketler.dur(iha)

      
    
    ########### yakalanan cismin ortalanması ############## -> *todo test edilecek

    # # ortalamak için gereken çerçeve
    # x_top = 195.0; y_top=115.0
    # x_bottom = 445.0; y_bottom = 365.0

    # # ortalama sürecinde hareket hızları
    # buyuk_hiz=5
    # kucuk_hiz=2
    # print(detection)
    # # cismi ortalama operasyonu
    # if(bbox.origin_x<x_top):
    #   print("sola git")
    #   genelHareketler.sola(iha, time=2,hiz=buyuk_hiz)
    #   kameraGecikmesi(iha)
    #   if((bbox.origin_x + bbox.width)>x_bottom):
    #     print("az sağa git")
    #     genelHareketler.saga(iha, time=1,hiz=kucuk_hiz)
    #     kameraGecikmesi(iha)
    # elif(bbox.origin_x>x_bottom):
    #   print("sağa git")
    #   genelHareketler.saga(iha, time=2,hiz=buyuk_hiz)
    #   kameraGecikmesi(iha)
    #   if((bbox.origin_x)<x_top):
    #     print(" az sola git")
    #     genelHareketler.sola(iha, time=1,hiz=kucuk_hiz)
    #     kameraGecikmesi(iha)
    # if(bbox.origin_y>y_top):
    #   print("ileri git")
    #   genelHareketler.ileri(iha, time=2,hiz=buyuk_hiz)
    #   kameraGecikmesi(iha)
    #   if((bbox.origin_y + bbox.width)<y_bottom):
    #     print("az geri git")
    #     genelHareketler.geri(iha, time=1,hiz=kucuk_hiz)
    #     kameraGecikmesi(iha)
    # elif(bbox.origin_y<y_bottom):
    #   print("geri git")
    #   genelHareketler.geri(iha, time=2,hiz=buyuk_hiz)
    #   kameraGecikmesi(iha)
    #   if((bbox.origin_y)>y_top):
    #     print(" az ileri git")
    #     genelHareketler.ileri(iha, time=1,hiz=kucuk_hiz)
    #     kameraGecikmesi(iha)
    
    ##if ((bbox.origin_x>x_top and (bbox.origin_x + bbox.width) <x_bottom ) and (bbox.origin_y<y_top and (bbox.origin_y + bbox.height)>y_bottom)):
    servo.runServo()
    time.sleep(5)
    genelHareketler.eveDon(iha)

    
    
    # Draw bounding_box"1
    bbox = detection.bounding_box
    start_point = bbox.origin_x, bbox.origin_y
    end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
    cv2.rectangle(image, start_point, end_point, _TEXT_COLOR, 3)

    # Draw label and score
    category = detection.categories[0]
    category_name = category.category_name
    probability = round(category.score, 2)
    result_text = category_name + ' (' + str(probability) + ')'
    text_location = (_MARGIN + bbox.origin_x,
                     _MARGIN + _ROW_SIZE + bbox.origin_y)
    cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                _FONT_SIZE, _TEXT_COLOR, _FONT_THICKNESS)

  return image
