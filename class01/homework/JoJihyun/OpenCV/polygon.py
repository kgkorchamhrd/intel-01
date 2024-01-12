import cv2
import copy
import time

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

topLeft = (100, 100)
bottomRight = (200, 300)

crt_x = 0
crt_y = 0
circle = False
frame = None

def onMouse(event, x, y, flags, param):
    global crt_x, crt_y, frame, circle
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'Mouse clicked at ({x}, {y})')
        crt_x, crt_y = x, y
        # cv2.circle(frame, (x, y), 80, (0, 255, 255), 15)
        circle = True

cv2.namedWindow('Camera')
cv2.setMouseCallback('Camera', onMouse)

while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.line(frame, topLeft, bottomRight, (0, 150, 150), 10)

    cv2.rectangle(frame,
            [pt+10 for pt in topLeft], [pt+30 for pt in bottomRight], (180, 0, 180), 5)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, 'Hello!',
            [pt+50 for pt in topLeft], font, 2, (0, 255, 0), 5)
    
    if circle:
        cv2.circle(frame, (crt_x, crt_y), 80, (0, 255, 255), 15)

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
