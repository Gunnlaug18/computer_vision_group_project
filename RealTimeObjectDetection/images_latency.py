import time
# import the modules
import os
import cv2
from os import listdir




 
# get the path/directory
folder_dir = "C:\\Users\\irisf\\Documents\\HR-master\\T-COMP-GROUPS\\computer_vision_group_project\\RealTimeObjectDetection\\"
for images in os.listdir(folder_dir):
 
    # check if the image ends with png
    if (images.endswith(".jpg")):
        print(images)
        current_time = time.time()
        # im_copy = images.copy()
        print(current_time)
        while(True):
            # print(images)
            
            # t = time.localtime()
            # current_time = time.strftime("%H:%M:%S", t)
            # test = time.process_time_ns()
            
            # print(test)
            im_src=cv2.imread(images)

            # im_srv = cv2.resize(480,640)
            cv2.imshow("Source Image", im_src)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
            # time.sleep(2)
    
        # print(images)


# im_src=cv2.imread("WIN_20221204_00_03_55_Pro.jpg")
# cv2.imshow("Source Image", im_src)

