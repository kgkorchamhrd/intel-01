import numpy as np
import cv2
import time

# Read from the recorded video file
cap = cv2.VideoCapture("ronaldinho.mp4")

while(cap.isOpened()):
    ret, frame = cap.read()
    
    if ret is False:
        print("Can't receive frame (stream end?). Exiting ...")
        
    # Display
    cv2.imshow("Frame", frame)
    time.sleep(1/30)
    
    key = cv2.waitkey(1)
    if key & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()