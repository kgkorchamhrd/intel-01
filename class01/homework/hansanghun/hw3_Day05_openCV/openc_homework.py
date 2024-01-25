import numpy as np
import cv2
import time
cap = cv2.VideoCapture('ronaldinho.mp4')

while(cap.isOpened()):

    ret, frame = cap.read()

    if ret is False:
        print("Can't receive frame  (stream -end?). Exiting ...")
        break

    cv2.imshow("Frame",frame)

    time.sleep(1/24)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
                                     