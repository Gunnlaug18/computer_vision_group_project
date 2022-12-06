import mediapipe as mp
import cv2 
import numpy as np
import uuid #in order to get no overlap
import os
import time

IMAGE_PATH = 'Tensorflow\\workspace\\images\\colectedimages'
labels = ['LEFT','RIGHT', 'UP', 'DOWN', 'NADA']
number_imgs = 10
counter = 0

for lable in labels:
    os.mkdir('Tensorflow\\workspace\\images\\colectedimages\\'+ lable)
    cap = cv2.VideoCapture(0)
    print('COLLECTING images for {}'.format(lable))
    time.sleep(5)
    for imgnum in range(number_imgs):
        counter += 1
        print(counter)
        if counter == 10:
            print("SWITCH signal")
        ret,frame = cap.read()
        imagename = os.path.join(IMAGE_PATH, lable, lable + '_' +'{}.jpg'.format(str(uuid.uuid1())))
        cv2.imwrite(imagename,frame)
        cv2.imshow('frame',frame)
        time.sleep(2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
cv2.destroyAllWindows()