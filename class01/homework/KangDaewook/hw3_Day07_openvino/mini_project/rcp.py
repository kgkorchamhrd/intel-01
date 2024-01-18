import random
import tensorflow.keras
import numpy as np
import cv2
import time
import speech_recognition as sr
import threading
from queue import Queue

model_rcp = tensorflow.keras.models.load_model('model_rcp/rcp.h5')
model_pt = tensorflow.keras.models.load_model('model_pt/pt.h5')

speech_queue = Queue()

global count
count = 0

global flag
flag = 0

Faker = 'light.png'

drawing_circle = True


def draw_circle():
    global drawing_circle, circle_position

    if drawing_circle:
        cv2.circle(img, circle_position, 30, (200, 50, 30), -1)


size = (224, 224)

classes_rcp = ['Scissors', 'Rock', 'Paper']
classes_pt = ['Left Up', 'Right Up', 'Left Down', 'Right Down']

def recognize_and_chat():
    recognizer = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="ko-KR")
            print("인식된 텍스트:", text)
            speech_queue.put(text)

        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            pass

speech_thread = threading.Thread(target=recognize_and_chat)
speech_thread.daemon = True
speech_thread.start()

def rcp_img(pred, cnt):
    rand_num = random.randint(0, 2) # 0:가위, 1:바위, 2:보
    rand_num = str(rand_num)
    rand_img = f'img_jpg/{rand_num}.jpg'

    road_img = cv2.imread(rand_img)

    cv2.namedWindow("Output Image", cv2.WINDOW_NORMAL)
    cv2.imshow("Output Image", road_img)

    if rand_num == '0' and np.argmax(pred) == 0:
        pass
    elif rand_num == '1' and np.argmax(pred) == 1:
        pass
    elif rand_num == '2' and np.argmax(pred) == 2:
        pass
    elif rand_num == '0' and np.argmax(pred) == 1:
        cnt = cnt + 1

    elif rand_num == '0' and np.argmax(pred) == 2:
        cnt = cnt - 1

    elif rand_num == '1' and np.argmax(pred) == 2:
        cnt = cnt + 1

    elif rand_num == '1' and np.argmax(pred) == 0:
        cnt = cnt - 1

    elif rand_num == '2' and np.argmax(pred) == 0:
        cnt = cnt + 1

    elif rand_num == '2' and np.argmax(pred) == 1:
        cnt = cnt - 1

    return cnt

Q = ''

cap = cv2.VideoCapture(0)
while cap.isOpened():

    flag = 0
    if flag == 0:
        cv2.destroyAllWindows()
    if flag == 1:
        pass
    # Q = input("command : ")
    # Q = recognize_and_chat()
    if not speech_queue.empty():
        Q = speech_queue.get()

    if Q == '가위바위보':
        while True:
            # recognize_and_chat()
            if flag == 1:
                break
            end_time = time.time() + 4
            while time.time() < end_time:
                remaining_time = round(float(end_time - time.time()), 2)
                ret, img = cap.read()
                if not ret:
                    break

                h, w, _ = img.shape
                cx = h / 2
                img = img[:, 200:200 + img.shape[0]]
                img = cv2.flip(img, 1)

                img_input = cv2.resize(img, size)
                img_input = cv2.cvtColor(img_input, cv2.COLOR_BGR2RGB)
                img_input = (img_input.astype(np.float32) / 127.0) - 1
                img_input = np.expand_dims(img_input, axis=0)

                prediction = model_rcp.predict(img_input)
                idx = np.argmax(prediction)

                cv2.putText(img, text=classes_rcp[idx], org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(0, 0, 0), thickness=2)
                cv2.putText(img, text=str(count), org=(300, 450), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(0, 0, 255), thickness=2)
                cv2.putText(img, text=f"Time left: {remaining_time}", org=(10, 70), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(0, 255, 0), thickness=2)
                cv2.imshow('result', img)
                if not speech_queue.empty():
                    Q = speech_queue.get()
                if Q == '종료' or Q == '그만':
                    flag = 1
                    break
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    flag = 1
                    break


            count = rcp_img(prediction, count)

    elif Q == '인터랙션' or Q == 'interaction' or Q == 'infection' or Q == '임프레션' or Q == 'inflection':
        while True:
            if flag == 2:
                break

            circle_positions = [
                (50, 80),  # 왼상
                (400, 80),  # 오상
                (50, 400),  # 왼아
                (400, 400)  # 오아
            ]
            circle_position = random.choice(circle_positions)

            end_time = time.time() + 2
            while time.time() < end_time:
                remaining_time = round(float(end_time - time.time()), 2)
                ret, img = cap.read()
                if not ret:
                    break

                h, w, _ = img.shape
                cx = h / 2
                img = img[:, 200:200 + img.shape[0]]
                img = cv2.flip(img, 1)

                img_input = cv2.resize(img, size)
                img_input = cv2.cvtColor(img_input, cv2.COLOR_BGR2RGB)
                img_input = (img_input.astype(np.float32) / 127.0) - 1
                img_input = np.expand_dims(img_input, axis=0)

                prediction = model_pt.predict(img_input)
                idx = np.argmax(prediction)

                cv2.putText(img, text=classes_pt[idx], org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(0, 0, 0), thickness=2)
                cv2.putText(img, text=str(count), org=(300, 450), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(0, 0, 255), thickness=2)
                cv2.putText(img, text=f"Time left: {remaining_time}", org=(80, 450), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(0, 255, 0), thickness=2)
                draw_circle()
                cv2.imshow('result', img)
                if not speech_queue.empty():
                    Q = speech_queue.get()
                if Q == '종료' or Q == '그만':
                    flag = 2
                    break
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    flag = 2
                    break

            # (50, 80),  # 왼상
            # (400, 80),  # 오상
            # (50, 400),  # 왼아
            # (400, 400)  # 오아
            if circle_position == (50, 80): # 0:왼상, 1:오상, 2:왼아, 3:오아
                if idx == 0:
                    count = count + 1
                else:
                    count = count - 1
            if circle_position == (400, 80):
                if idx == 1:
                    count = count + 1
                else:
                    count = count - 1
            if circle_position == (50, 400):
                if idx == 2:
                    count = count + 1
                else:
                    count = count - 1
            if circle_position == (400, 400):
                if idx == 3:
                    count = count + 1
                else:
                    count = count - 1

    elif Q == '불 좀 꺼 줄래' or Q == '불 좀 꺼 줄래요':
        image = cv2.imread(Faker)
        image = cv2.resize(image, (1500, 800))
        cv2.imshow('Image', image)
        cv2.waitKey(5000)
        cv2.destroyAllWindows()
        exit()
    else:
        pass