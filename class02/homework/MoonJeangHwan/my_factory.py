#!/usr/bin/env python3

import os
import threading
from argparse import ArgumentParser
from queue import Empty, Queue
from time import sleep

import cv2
import numpy as np
from openvino.inference_engine import IECore
import subprocess

from iotdemo import FactoryController, MotionDetector, ColorDetector
import ipywidgets as widgets
import openvino as ov


# 파라미터들

FORCE_STOP = False

def thread_cam1(q : Queue) -> None :
    my_md = MotionDetector()    
    my_md.load_preset('./motion.cfg')
    
    # TODO: Load and initialize OpenVINO    
    core = ov.Core()
    model = core.read_model(model='./resources/model.xml')
    compiled_model = core.compile_model(model=model, device_name='CPU')
 
    # TODO: HW2 Open video clip resources/conveyor.mp4 instead of camera device.
    my_video = './resources/conveyor.mp4'
    cap = cv2.VideoCapture(my_video)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

    while not FORCE_STOP:
        sleep(0.03)
        _ , frame = cap.read()
        if frame is None:
            break
        
        # TODO: HW2 Enqueue "VIDEO:Cam1 live", frame info
        q.put(('VIDEO:Cam1 live', frame))

        # TODO: Motion detect
        detected = my_md.detect(frame)
        if detected is None:
            continue

        # TODO: Enqueue "VIDEO:Cam1 detected", detected info.
        q.put(('VIDEO:Cam1 live', detected))

        # abnormal detect
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        reshaped = detected[:, :, [2, 1, 0]]
        np_data = np.moveaxis(reshaped, -1, 0)
        preprocessed_numpy = [((np_data / 255.0) - 0.5) * 2]
        batch_tensor = np.stack(preprocessed_numpy, axis=0)

        # TODO: Inference OpenVINO
        name, ratio = compiled_model.output(detected)

        # TODO: Calculate ratios
        if name == 'Circle':
            print(f'Circle {ratio:.2f}%')
        else:
            print(f'X = {ratio:.2f}%')

        # TODO: in queue for moving the actuator 1
        q.put(('PUSH', 1))

    cap.release()
    q.put(('DONE', None))
    exit()


def thread_cam2(q : Queue) -> None :
    my_md = MotionDetector()
    my_cd = ColorDetector()
    my_md.load_preset('./motion.cfg')
    my_cd.load_preset('./resources/color.cfg')

    # TODO: Load and initialize OpenVINO    
    core = ov.Core()
    model = core.read_model(model='./resources/model.xml')
    compiled_model = core.compile_model(model=model, device_name='CPU')

    # TODO: HW2 Open video clip resources/conveyor.mp4 instead of camera device.
    my_video = './resorces/conveyor.mp4'
    cap = cv2.VideoCapture(my_video)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break
        
        # TODO: HW2 Enqueue "VIDEO:Cam2 live", frame info
        q.put(('VIDEO:Cam2 live', frame))

        # TODO: Detect motion
        detected = my_md.detect(frame)
        if detected is None:
            continue

        # TODO: Enqueue "VIDEO:Cam2 detected", detected info.
        q.put(('VIDEO:Cam2 live', detected))

        # TODO: Detect color
        color_predict = my_cd.detect(detected)

        # TODO: Inference OpenVINO
        color, ratio = compiled_model.output(color_predict)

        # TODO: Compute ratio
        print(f"{color}: {ratio:.2f}%")

        # TODO: in queue for moving the actuator 1
        q.put(('PUSH', 2))

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
    my_fc = FactoryController()

    parser = ArgumentParser(prog='python3 factory.py',
                            description="Factory tool")

    parser.add_argument("-d",
                        "--device",
                        default=None,
                        type=str,
                        help="Arduino port")
    args = parser.parse_args()

    # TODO: HW2 Create a Queue
    my_q = Queue()

    # TODO: HW2 Create thread_cam1 and thread_cam2 threads and start them.
    thread1 = threading.Thread(target=thread_cam1, args=(my_q,))
    thread2 = threading.Thread(target=thread_cam2, args=(my_q,))
    thread1.start()
    thread2.start()

    with FactoryController(args.device) as ctrl:
        while not FORCE_STOP:
            if cv2.waitKey(10) & 0xff == ord('q'):
                break

            # TODO: HW2 get an item from the queue. You might need to properly handle exceptions.
            # de-queue name and data
            name, data = my_q.get()

            # TODO: HW2 show videos with titles of 'Cam1 live' and 'Cam2 live' respectively.
            if name == 'VIDEO:Cam1 live':
                cv2.imshow(data)
            elif name == 'VIDEO:Cam2 live':
                cv2.imshow(data)
            # TODO: Control actuator, name == 'PUSH'
            elif name == 'PUSH':
                my_fc.push_actuator(data)

            if name == 'DONE':
                FORCE_STOP = True

            q.task_done()

    cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        os._exit()
