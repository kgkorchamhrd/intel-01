import cv2
import dlib
import numpy as np
from roboflow import Roboflow
import pygame
import time

# Roboflow API 키 설정
rf = Roboflow(api_key="oH052N6bPczgj5NNUPwh")
project = rf.workspace().project("drowsiness-detection-luvay")
model = project.version(1).model

# 얼굴 및 눈 랜드마크 모델 로드
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 웹캠 초기화
cap = cv2.VideoCapture(0)

# 알람 설정
pygame.mixer.init()
alarm_sound = pygame.mixer.Sound("alarm.mpga")

# 눈 감김 감지를 위한 변수
eyes_closed_frames = 0
alarm_active = False
start_time = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 그레이스케일로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 얼굴 감지
    faces = detector(gray)

    for face in faces:
        # 얼굴 랜드마크 검출
        landmarks = predictor(gray, face)

        # 눈 좌표 추출
        left_eye_coords = np.array([(landmarks.part(idx).x, landmarks.part(idx).y) for idx in range(36, 42)], dtype=np.int32)
        right_eye_coords = np.array([(landmarks.part(idx).x, landmarks.part(idx).y) for idx in range(42, 48)], dtype=np.int32)

        # 눈 주위에 박스 그리기
        cv2.polylines(frame, [left_eye_coords], isClosed=True, color=(255, 0, 0), thickness=2)
        cv2.polylines(frame, [right_eye_coords], isClosed=True, color=(255, 0, 0), thickness=2)

        # 눈 감김 여부 판단
        left_eye_ratio = cv2.contourArea(np.array(left_eye_coords)) / cv2.arcLength(np.array(left_eye_coords), True)**2
        right_eye_ratio = cv2.contourArea(np.array(right_eye_coords)) / cv2.arcLength(np.array(right_eye_coords), True)**2
        average_eye_ratio = (left_eye_ratio + right_eye_ratio) / 2

        # 5초 동안 눈을 감고 있는지 감지 로직
        if average_eye_ratio < 0.2:
            if start_time is None:
                start_time = time.time()
            else:
                elapsed_time = time.time() - start_time
                if elapsed_time >= 5:
                    pygame.mixer.Sound.play(alarm_sound)
                    time.sleep(1)
                    cv2.putText(frame, "Drowsiness Detected (5 seconds)", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    print("---- Drowsiness Detected (Blink) ----")
                    start_time = None  # 초기화
        else:
            start_time = None

    # 결과 화면에 표시
    cv2.imshow("Drowsiness Detection", frame)

    # 종료 조건
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 종료 시 비디오 스트림과 창 해제
cap.release()
cv2.destroyAllWindows()
