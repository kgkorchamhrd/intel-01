import cv2


cap = cv2.VideoCapture(0)

topLeft = (50, 50)
bottomRight = (300, 300)

while(cap.isOpened()):
    ret, frame = cap.read()

    cv2.line(frame, topLeft, bottomRight, (0, 255, 0), 5)

    cv2.rectangle(frame, [pt+30 for pt in topLeft], [pt-30 for pt in bottomRight], (0, 0, 255), 5)
    cv2.circle(frame, [pt+20 for pt in topLeft], 30, (0,0,255), 5)

    font = cv2.FONT_ITALIC
    cv2.putText(frame, 'you', [pt+150 for pt in topLeft], font, 6, (255, 1, 55), 5)


    cv2.imshow('Camera', frame)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

