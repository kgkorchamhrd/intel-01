import numpy as np
import cv2
import time

target_frame = 30
cap = cv2.VideoCapture("video_name.mp4")

while(cap.isOpened()):
    ret, frame = cap.read()
    
    if ret is False:
        print("Can't receive frame (stream end?). Exitint ...")
        break
    
    cv2. imshow()
    time.sleep(1 / target_frame)
    
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()