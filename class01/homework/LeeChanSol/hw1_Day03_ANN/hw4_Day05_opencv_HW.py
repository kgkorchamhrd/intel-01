import numpy as np
import time
import cv2


cap = cv2.VideoCapture('test1.mp4')

while(cap.isOpened()):

    ret, frame = cap.read()
    time.sleep(0.05)
    if ret is False:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv2.imshow('Frame', frame)

    key = cv2.waitKey(1)
    if key &0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
