import cv2

cap = cv2.VideoCapture(0)

w = 1920
h = 1080
cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
fps = cap.get(cv2.CAP_PROP_FPS)

forc = cv2.VideoWriter_fourcc(*'DIVX')
delay = round(fps)
out = cv2.VideoWriter('record_output.avi', forc, fps, (w, h))


if not cap.isOpened():
    print('Error')
    cap.release()
    exit()

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret is False:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    cv2.imshow("Camera", frame)

    key = cv2.waitKey(delay)
    if key & 0xFF == ord('q'):
        break
