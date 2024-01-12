import numpy as np
import cvw

cap = cv2.VideoCapture("@@.mp4")

while(cap.isOpened()):
    ret, frame = cap.read()
    time.sleep(3)
    if ret is False:
        print("can't receive frame (stream end?). Exiting ...")
        break

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
