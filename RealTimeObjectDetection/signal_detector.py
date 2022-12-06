import cv2 
import numpy as np
import tensorflow as tf
from object_detection.utils import config_util
from object_detection.protos import pipeline_pb2
from google.protobuf import text_format
import os
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
import pyautogui
import time


WORKSPACE_PATH = 'Tensorflow/workspace'
SCRIPTS_PATH = 'Tensorflow/scripts'
APIMODEL_PATH = 'Tensorflow/models'
ANNOTATION_PATH = WORKSPACE_PATH+'/annotations'
IMAGE_PATH = WORKSPACE_PATH+'/images'
MODEL_PATH = WORKSPACE_PATH+'/models'
PRETRAINED_MODEL_PATH = WORKSPACE_PATH+'/pre-trained-models'
CONFIG_PATH = MODEL_PATH+'/my_ssd_mobnet/pipeline.config'
CHECKPOINT_PATH = MODEL_PATH+'/my_ssd_mobnet/'


labels = [{'name':'left', 'id':1}, 
        {'name':'right', 'id':2},
        {'name':'up', 'id':3},
        {'name':'down', 'id':4},
        {'name':'nada', 'id':5}]

with open(ANNOTATION_PATH + '\label_map.pbtxt', 'w') as f:
    for label in labels:
        f.write('item { \n')
        f.write('\tname:\'{}\'\n'.format(label['name']))
        f.write('\tid:{}\n'.format(label['id']))
        f.write('}\n')

CUSTOM_MODEL_NAME = 'my_ssd_mobnet' 

CONFIG_PATH = MODEL_PATH+'/'+CUSTOM_MODEL_NAME+'/pipeline.config'
config = config_util.get_configs_from_pipeline_file(CONFIG_PATH)

# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(CONFIG_PATH)
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(CHECKPOINT_PATH, 'ckpt-6')).expect_partial()

@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections


category_index = label_map_util.create_category_index_from_labelmap(ANNOTATION_PATH+'/label_map.pbtxt')

# Setup capture
cap = cv2.VideoCapture(2)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

start_signal = "nada"
prev_frame_time = 0
new_frame_time = 0

while True: 
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    image_np = np.array(frame)
    
    input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, axis=0), dtype=tf.float32)
    # print(input_tensor)
    detections = detect_fn(input_tensor)
    
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                  for key, value in detections.items()}
    detections['num_detections'] = num_detections

    # detection_classes should be ints.
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    label_id_offset = 1
    image_np_with_detections = image_np.copy()

    viz_utils.visualize_boxes_and_labels_on_image_array(
                image_np_with_detections,
                detections['detection_boxes'],
                detections['detection_classes']+label_id_offset,
                detections['detection_scores'],
                category_index,
                use_normalized_coordinates=True,
                max_boxes_to_draw=5,
                min_score_thresh=.5,
                agnostic_mode=False)
    # print(category_index[detections['detection_classes'][0]+label_id_offset]["name"])

    hand_signal = category_index[detections['detection_classes'][0]+label_id_offset]["name"]
    if hand_signal != start_signal and detections['detection_scores'][0] > 0.5:
        start_signal = hand_signal     
        print(hand_signal)
        print(detections['detection_scores'][0])
        print(time.time())
        if hand_signal == 'up':
            pyautogui.press('up')
        elif hand_signal == 'down':
            pyautogui.press('down')
        elif hand_signal == 'left':
            pyautogui.press('left')
        elif hand_signal == 'right':
            pyautogui.press('right')
        elif hand_signal == 'nada':
            hand_signal == 'nada'
    

    # font which we will be using to display FPS
    font = cv2.FONT_HERSHEY_SIMPLEX
    # time when we finish processing for this frame
    new_frame_time = time.time()
 
    # Calculating the fps
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
 
    # converting the fps into integer
    fps = int(fps)
    # converting the fps to string so that we can display it on frame
    # putting the FPS count on the frame
    cv2.putText(image_np_with_detections,  "FPS:" + str(fps), (1, 40), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
    time_now = time.time()
    cv2.putText(image_np_with_detections,  "Time:" + str(time_now), (1, 100), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
            
    cv2.imshow('object detection',  cv2.resize(image_np_with_detections, (800, 600)))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
    
