import cv2

cap = cv2.VideoCapture(0)
xyList = []
topLeft = (50, 50)
bottomRight = (300, 300)
cv2.namedWindow("Camera")
def onMouse(event,x,y,flag,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xyList.append((x,y))
cv2.setMouseCallback("Camera",onMouse)
while(cap.isOpened()):

    ret, frame = cap.read()

    cv2.line(frame, topLeft, bottomRight,(0, 255, 0),5)

    cv2.rectangle(frame,[pt+30 for pt in topLeft],[pt-30 for pt in bottomRight],(0,0,255),5)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, 'me', [pt+80 for pt in topLeft],font,2,(0,255,255),10)

    

    #circle
    cv2.circle(frame,[pt+120 for pt in topLeft],50,(255,255,0),5)
    for x,y in xyList:
        cv2.circle(frame,(x,y),10,(255,0,0),-1)


    cv2.imshow("Camera",frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()