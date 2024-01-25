import numpy as np
import cv2
import time

# 동영상 파일 읽기
cap = cv2.VideoCapture("ronaldinho.mp4")

# 동영상의 frame rate 확인
fps = cap.get(cv2.CAP_PROP_FPS)

# 동영상이 열려있는 동안 반복
while(cap.isOpened()):
    # 한 프레임 읽기
    ret, frame = cap.read()
    
    if not ret:
        print("프레임을 받아올 수 없습니다. 동영상 종료 또는 오류 발생.")
        break

    # 프레임 표시
    cv2.imshow("프레임", frame)

    # 동영상의 frame rate에 맞게 대기
    time.sleep(1 / fps)

    # 'q' 입력 시 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 동영상 재생 종료 후 해제
cap.release()
cv2.destroyAllWindows()
