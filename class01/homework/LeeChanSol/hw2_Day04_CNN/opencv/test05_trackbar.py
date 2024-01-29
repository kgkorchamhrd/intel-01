import cv2


cap = cv2.VideoCapture(0)

topLeft = (50, 50)
bold = 0
red = 0
blue = 0
green = 0

def on_bold_trackbar(value):
    global bold
    bold = value

def on_color_trackbar():
    pass

cv2.namedWindow("Camera")
cv2.createTrackbar("bold", "Camera", bold, 10, on_bold_trackbar)
cv2.createTrackbar("R", "Camera", red, 255, on_color_trackbar)
cv2.createTrackbar("G", "Camera", green, 255, on_color_trackbar)
cv2.createTrackbar("B", "Camera", blue, 255, on_color_trackbar)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret is False:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    red= cv2.getTrackbarPos("R","Camera")
    blue = cv2.getTrackbarPos('B', "Camera")
    green = cv2.getTrackbarPos('G', 'Camera')


    cv2.putText(frame, 'Text', topLeft, cv2.FONT_HERSHEY_SIMPLEX, 2, (blue, green, red), 1 + bold)

    cv2.imshow('Camera', frame)

    key = cv2.waitKey(1)
    if key & 0xff == ord('q'):
        break


