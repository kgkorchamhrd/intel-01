import numpy as np
import cv2

cap = cv2.VideoCapture(0)

topLeft = (50, 50)
bottomRight = (300, 300)

bold = 0

def on_bold_trackbar(value):
    global bold
    bold = value

cv2.namedWindow("Camera")
cv2.createTrackbar("bold", "Camera", bold, 10, on_bold_trackbar)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret is False:
        print("Cant't receive frame (stream end?). Exiting ...")
        break
    
    cv2.putText(frame, "TEXT", topLeft, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 1 + bold)
    
    cv2.imshow("Camera", frame)
    
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break    