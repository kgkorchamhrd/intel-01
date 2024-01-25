import cv2

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

topLeft = (20, 460)
bold = 0
font_size = 0

def onChange(x):
    pass

def on_bold_trackbar(value):
    global bold
    bold = value

def on_font_size_change(value):
    global font_size
    font_size = value

cv2.namedWindow("Camera")
cv2.createTrackbar("bold", "Camera", bold, 10, on_bold_trackbar)
cv2.createTrackbar("Size", "Camera", font_size, 10, on_font_size_change)

cv2.createTrackbar('R', 'Camera', 0, 255, onChange)
cv2.createTrackbar('G', 'Camera', 0, 255, onChange)
cv2.createTrackbar('B', 'Camera', 0, 255, onChange)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret is False:
        print("Can't receive frame (Stream end?). Exiting ...")
        break
    
    r = cv2.getTrackbarPos('R', 'Camera')
    g = cv2.getTrackbarPos('G', 'Camera')
    b = cv2.getTrackbarPos('B', 'Camera')

    cv2.putText(frame, "TEXT", topLeft, cv2.FONT_HERSHEY_SIMPLEX, 2 + font_size, (b, g, r), 1 + bold)

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
