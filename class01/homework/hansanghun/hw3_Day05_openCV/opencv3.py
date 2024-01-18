import cv2
import numpy as np
cap = cv2.VideoCapture(0)

w = 640
h = 480

cap.set(cv2.CAP_PROP_FRAME_WIDTH,w)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,h)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret is False:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv2.imshow("Camera",frame)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()