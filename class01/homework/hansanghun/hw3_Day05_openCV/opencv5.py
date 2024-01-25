import cv2

cap = cv2.VideoCapture(0)


topLeft = (50, 50)
bold = 5
rgb = [0,0,0]
def on_bold_trackbar(value):

    global bold
    bold = value
def onChange_R(value):
    rgb[0]=value
def onChange_G(value):
    rgb[1]=value
def onChange_B(value):
    rgb[2]=value
    
cv2.namedWindow("Camera")
cv2.createTrackbar("bold","Camera",bold,10,on_bold_trackbar)
cv2.createTrackbar('R', "Camera",0,255, onChange_R)
cv2.createTrackbar('G', "Camera", 0, 255, onChange_G)
cv2.createTrackbar('B', "Camera", 0, 255, onChange_B)


while(cap.isOpened()):

    ret, frame = cap.read()
    if ret is False:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv2.putText(frame, "TEXT",topLeft,cv2.FONT_HERSHEY_SIMPLEX,2, tuple(rgb),1+bold)

    cv2.imshow("Camera",frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()