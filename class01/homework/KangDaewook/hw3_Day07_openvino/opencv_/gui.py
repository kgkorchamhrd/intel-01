import numpy as np
import cv2

cap = cv2.VideoCapture(0)

topLeft = (50, 50)
bottomRight = (300, 300)

while(cap.isOpened()):
    ret, frame = cap.read()
    
    cv2.line(frame, topLeft, bottomRight, (0, 255, 0), 5)
    
    cv2.rectangle(frame, [pt+30 for pt in topLeft], [pt-30 for pt in bottomRight], (0, 0, 255), 5)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, 'me', [pt+80 for pt in topLeft], font, 2, (0, 255, 255), 10)
    
    cv2.imshow("Camera", frame)
    
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break    