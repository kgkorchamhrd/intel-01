import cv2
import time
import pygame
from roboflow import Roboflow

rf = Roboflow(api_key="ld0a5DFJl0ebJQVOjqr0")
project = rf.workspace().project("eye-detection-kso3d")
model = project.version(3).model

# 카메라 열기
cap = cv2.VideoCapture(0)  # 0은 기본 카메라를 나타냅니다.

# 비디오 프레임 크기 설정
frame_width = 640
frame_height = 480
cap.set(3, frame_width)
cap.set(4, frame_height)

# 이미지 크기 설정
new_width = 300
new_height = 200

start_time = []

while True:
    # 프레임 읽기
    ret, frame = cap.read()

    if not ret:
        print("Failed to read frame")
        break
    
    # 이미지 크기 조절
    frame_resized = cv2.resize(frame, (new_width, new_height))

    # 프레임을 이미지로 저장
    image_file = f"frame_{int(cap.get(1))}.png"
    cv2.imwrite(image_file, frame_resized)
    print(f"Saved: {image_file}")

    # 화면에 프레임 표시
    cv2.imshow('Video Capture', frame)
    
    mymodel = model.predict(image_file, confidence=40, overlap=30).json()
    if mymodel.get('predictions'):
        print(mymodel)
        elapsed_time = 0
        start_time = []
    else:
        start_time.append(time.time())
        print(f"No predictions found. Current time: {time.ctime()}")  # 시간을 더 읽기 쉽게 출력
        
        elapsed_time = time.time() - start_time[0]
        if elapsed_time >= 5:
            #알람 설정
            pygame.mixer.init()
            pygame.mixer.music.load("IU.mp3")

            #알람 실행
            pygame.mixer.music.play()
            print(f"Warning: No predictions received for {elapsed_time} seconds!")
            elapsed_time = 0
            start_time = []

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break            
    
# 작업이 끝나면 카메라 해제 및 OpenCV 창 닫기
cap.release()
cv2.destroyAllWindows()