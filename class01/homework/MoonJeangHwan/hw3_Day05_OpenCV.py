import numpt as nump
import cv2
from time import sleep

frame_for_sec = 1 / 30

cap = cv2.VideoCapture("ronaldinho.mp4")

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret is False: # homework No.1
        print("Can't receive frame (stream end?). Exiting ...")
        break
    cv2.imshow("Frame", frame)
    sleep(1/30)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindow()