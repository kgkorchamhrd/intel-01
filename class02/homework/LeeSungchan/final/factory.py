#!/usr/bin/env python3

import os
import threading
from argparse import ArgumentParser
from queue import Empty, Queue
from time import sleep

import cv2
import numpy as np
from openvino.inference_engine import IECore, ov

from iotdemo import FactoryController, MotionDetector, ColorDetector

FORCE_STOP = False


def thread_cam1(q):
    # TODO: MotionDetector
    m_detector = MotionDetector()
    # TODO: Load and initialize OpenVINO
    core = ov.Core()
    model = core.load_model(model='./resources/model.xml')
    compiled_model = core.compile_model(model=model)
    # TODO: HW2 Open video clip resources/conveyor.mp4 instead of camera device.
    cap = cv2.VideoCapture(2)
    # cap = cv2.VideoCapture('./resources/conveyot.mp4')
    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

        # TODO: HW2 Enqueue "VIDEO:Cam1 live", frame info
        q.put(('VIDEO:Cam1 live', frame))
        # TODO: Motion detect
        detected = m_detector(frame)
        if detected is None:
            continue
        # TODO: Enqueue "VIDEO:Cam1 detected", detected info.
        q.put(('VIDEO:Cam1 detected', detected))
        # abnormal detect
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        reshaped = detected[:, :, [2, 1, 0]]
        np_data = np.moveaxis(reshaped, -1, 0)
        preprocessed_numpy = [((np_data / 255.0) - 0.5) * 2]
        batch_tensor = np.stack(preprocessed_numpy, axis=0)

        # TODO: Inference OpenVINO
        
        x_ratio, circle_ratio = 

        # TODO: Calculate ratios
        print(f"X = {x_ratio:.2f}%, Circle = {circle_ratio:.2f}%")

        # TODO: in queue for moving the actuator 1
        if circle_ratio < x_ratio:
            q.put("PUSH", 1)

    cap.release()
    q.put(('DONE', None))
    exit()


def thread_cam2(q):
    # TODO: MotionDetector
    m_detector = MotionDetector()
    # TODO: ColorDetector
    c_detector = ColorDetector()
    # TODO: HW2 Open "resources/conveyor.mp4" video clip
    cap = cv2.VideoCapture(4)
    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

        # TODO: HW2 Enqueue "VIDEO:Cam2 live", frame info
        q.put(('VIDEO:Cam2 live', frame))
        # TODO: Detect motion
        detected = m_detector(frame)
        # TODO: Enqueue "VIDEO:Cam2 detected", detected info.
        q.put(('VIDEO:Cam2 detected', detected))
        # TODO: Detect color
        predict = c_detector(detected)
        name, ratio = predict[0]
        ratio = ratio * 100
        # TODO: Compute ratio
        print(f"{name}: {ratio:.2f}%")

        # TODO: Enqueue to handle actuator 2
        if name == 'blue':
            q.put("PUSH", 2)

    cap.release()
    q.put(('DONE', None))
    exit()


def imshow(title, frame, pos=None):
    cv2.namedWindow(title)
    if pos:
        cv2.moveWindow(title, pos[0], pos[1])
    cv2.imshow(title, frame)


def main():
    global FORCE_STOP

    parser = ArgumentParser(prog='python3 factory.py',
                            description="Factory tool")

    parser.add_argument("-d",
                        "--device",
                        default=None,
                        type=str,
                        help="Arduino port")
    args = parser.parse_args()

    # TODO: HW2 Create a Queue
    qFactory = Queue()
    # TODO: HW2 Create thread_cam1 and thread_cam2 threads and start them.
    thread1=threading.Thread(target=thread_cam1, args= (qFactory, ))
    thread2=threading.Thread(target=thread_cam2, args= (qFactory, ))
    thread1.start()
    thread2.start()
    
    with FactoryController(args.device) as ctrl:
        while not FORCE_STOP:
            if cv2.waitKey(10) & 0xff == ord('q'):
                break

            # TODO: HW2 get an item from the queue. You might need to properly handle exceptions.
            # de-queue name and data
            try:
                qdata = aFactory.get_nowait()
            except:
                pass
            name, data = qdata
            if name == 'Cam1 live':
                
            elif name == 'VIDEO:Cam1':
            # TODO: HW2 show videos with titles of 'Cam1 live' and 'Cam2 live' respectively.

            # TODO: Control actuator, name == 'PUSH'

            if name == 'DONE':
                FORCE_STOP = True

            q.task_done()

    cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        os._exit()
