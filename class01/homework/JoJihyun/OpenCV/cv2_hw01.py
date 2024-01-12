import numpy as np
import cv2
import time

cap = cv2.VideoCapture("ronaldinho.mp4")
w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

forc = cv2.VideoWriter_fourcc(*'DIVX')
delay = round(600/fps)
out = cv2.VideoWriter('output.avi', forc, fps, (w, h))

while(cap.isOpened()):
    ret, frame = cap.read()
    
    if ret is False:
        print("can't receive frame (stream end?). Exiting ...")
        break

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(delay)
    if key & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
