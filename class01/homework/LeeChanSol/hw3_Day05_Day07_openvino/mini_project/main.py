# Fetch `notebook_utils` module
import urllib.request
urllib.request.urlretrieve(
    url='https://raw.githubusercontent.com/openvinotoolkit/openvino_notebooks/main/notebooks/utils/notebook_utils.py',
    filename='notebook_utils.py'
)

import collections
import time

import cv2
import numpy as np
from pathlib import Path
from IPython import display
from ipywidgets import interactive, ToggleButtons
import openvino as ov
import matplotlib.pyplot as plt

import notebook_utils as utils
 
import ipywidgets as widgets

import subprocess
import threading


file_path = '/opt/intel/openvino_2023.0.2/open_model_zoo/demos/intel64/Release/interactive_face_detection_demo'

run_argument= ['-i', '1', '-m', '/opt/intel/openvino_2023.0.2/open_model_zoo/demos/interactive_face_detection_demo/cpp/intel/face-detection-adas-0001/FP16/face-detection-adas-0001.xml', 
               '--mag', '//opt/intel/openvino_2023.0.2/open_model_zoo/demos/interactive_face_detection_demo/cpp/intel/age-gender-recognition-retail-0013/FP16/age-gender-recognition-retail-0013.xml',
               '--mhp', '/opt/intel/openvino_2023.0.2/open_model_zoo/demos/interactive_face_detection_demo/cpp/intel/head-pose-estimation-adas-0001/FP16/head-pose-estimation-adas-0001.xml', 
               '--mem', '/opt/intel/openvino_2023.0.2/open_model_zoo/demos/interactive_face_detection_demo/cpp/intel/emotions-recognition-retail-0003/FP16/emotions-recognition-retail-0003.xml',
               '--mlm', '/opt/intel/openvino_2023.0.2/open_model_zoo/demos/interactive_face_detection_demo/cpp/intel/facial-landmarks-35-adas-0002/FP16/facial-landmarks-35-adas-0002.xml', 
               '--mam', '/opt/intel/openvino_2023.0.2/open_model_zoo/demos/interactive_face_detection_demo/cpp/public/anti-spoof-mn3/anti-spoof-mn3.onnx', '-d', 'CPU', '-r', '--noshow']


emotion = ['happy', 'sad', 'surprise', 'anger', 'neutral']
dict_options = {'happy': 'MOSAIC', 'anger': 'RAIN-PRINCESS', 'surprise': 'UDNIE', 'sad': 'POINTILISM'}
state = 'happy'
save_image = []

def init(state='happy'):
    effect = dict_options[state].lower()

    # base_model_dir = "model"
    # base_url = "https://github.com/onnx/models/raw/69d69010b7ed6ba9438c392943d2715026792d40/archive/vision/style_transfer/fast_neural_style/model"

    # Selected ONNX model will be downloaded in the path
    model_path = Path(f"{effect}-9.onnx")
    # print(model_path)

    # style_url = f"{base_url}/{model_path}"
    # utils.download_file(style_url, directory=base_model_dir)

    # ov_model = ov.convert_model(f"model/{effect}-9.onnx")
    # ov.save_model(ov_model, f"model/{effect}-9.xml")

    ir_path = Path(f"model/{effect}-9.xml")
    onnx_path = Path(f"model/{model_path}")

    core = ov.Core()

    model = core.read_model(model=ir_path)

    device = widgets.Dropdown(
        options=core.available_devices + ["AUTO"],
        value='AUTO',
        description='Device:',
        disabled=False,
    )

    compiled_model = core.compile_model(model=model, device_name=device.value)

    input_layer = compiled_model.input(0)
    output_layer = compiled_model.output(0)
    
    return input_layer, output_layer, compiled_model


input_layer, output_layer, compiled_model = init()
N, C, H, W = list(input_layer.shape)


def preprocess_images(frame, H, W):
    """
    Preprocess input image to align with network size

    Parameters:
        :param frame:  input frame 
        :param H:  height of the frame to style transfer model
        :param W:  width of the frame to style transfer model
        :returns: resized and transposed frame
    """
    image = np.array(frame).astype('float32')
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image = cv2.resize(src=image, dsize=(H, W), interpolation=cv2.INTER_AREA)
    image = np.transpose(image, [2, 0, 1])
    image = np.expand_dims(image, axis=0)
    return image


def convert_result_to_image(frame, stylized_image) -> np.ndarray:
    """
    Postprocess stylized image for visualization

    Parameters:
        :param frame:  input frame 
        :param stylized_image:  stylized image with specific style applied
        :returns: resized stylized image for visualization
    """
    h, w = frame.shape[:2]
    stylized_image = stylized_image.squeeze().transpose(1, 2, 0)
    stylized_image = cv2.resize(src=stylized_image, dsize=(w, h), interpolation=cv2.INTER_CUBIC)
    stylized_image = np.clip(stylized_image, 0, 255).astype(np.uint8)
    stylized_image = cv2.cvtColor(stylized_image, cv2.COLOR_BGR2RGB)
    return stylized_image


def run_style_transfer(source=0, flip=False, use_popup=False, skip_first_frames=0):
    global save_image
    save_image = []
    count = 0
    try:
        player = utils.VideoPlayer(source=source, flip=flip, fps=30, skip_first_frames=skip_first_frames)
        # Start video capturing.
        player.start()
        if use_popup:
            title = "Press ESC to Exit"
            cv2.namedWindow(winname=title, flags=cv2.WINDOW_GUI_NORMAL | cv2.WINDOW_AUTOSIZE)

        processing_times = collections.deque()
        
        temp = None
        while True:
            emo = state #emotion[count]
            if emo != 'neutral' and emo != temp:
                input_layer, output_layer, compiled_model = init(emo)
                N, C, H, W = list(input_layer.shape)
                temp = emo
            
            # Grab the frame.
            frame = player.next()
            if frame is None:
                print("Source ended")
                break
            # If the frame is larger than full HD, reduce size to improve the performance.
            scale = 720 / max(frame.shape)
            if scale < 1:
                frame = cv2.resize(src=frame, dsize=None, fx=scale, fy=scale,
                                   interpolation=cv2.INTER_AREA)
            # Preprocess the input image.

            image = preprocess_images(frame, H, W)
           
            # Measure processing time for the input image.
            start_time = time.time()
            # Perform the inference step.
            stylized_image = compiled_model([image])[output_layer]
            stop_time = time.time()

            # Postprocessing for stylized image.
            result_image = convert_result_to_image(frame, stylized_image)

            processing_times.append(stop_time - start_time)
            # Use processing times from last 200 frames.
            if len(processing_times) > 200:
                processing_times.popleft()
            processing_time_det = np.mean(processing_times) * 1000

            # Visualize the results.
            f_height, f_width = frame.shape[:2]
            fps = 1000 / processing_time_det
            
            if use_popup:
                cv2.imshow(title, result_image)
                key = cv2.waitKey(1)
                # escape = 27   ESC
                if key == 27 or count >= 4:
                    break
                elif key == 115:   # 's'
                    count = count+1
                    # save_image = np.append(save_image, result_image, axis=0)
                    save_image.append(result_image)
                    print("save", count)
                elif key == 101:   # 'e'
                    print('record end')
            else:
                # Encode numpy array to jpg.
                _, encoded_img = cv2.imencode(".jpg", result_image, params=[cv2.IMWRITE_JPEG_QUALITY, 90])
                # Create an IPython image.
                i = display.Image(data=encoded_img)
                # Display the image in this notebook.
                display.clear_output(wait=True)
                display.display(i)
                
    # ctrl-c
    except KeyboardInterrupt:
        print("Interrupted")
    # any different error
    except RuntimeError as e:
        print(e)
    finally:
        if player is not None:
            # Stop capturing.
            player.stop()
        if use_popup:
            cv2.destroyAllWindows()
            global flag
            flag = False
            
def dect():
    global flag
    
    process = subprocess.Popen([file_path] + run_argument, stdout=subprocess.PIPE, universal_newlines=True)
    # if flag == False:
    #     process.terminate()
    emotion = ['neutral', 'happy', 'sad', 'surprise', 'anger']

    try:
        # 실시간으로 표준 출력을 읽어와서 확인
        for line in iter(process.stdout.readline, ''):            
            if "happy" in line:
                split_by_comma = line.split(',')
                result = [item.split('=') for item in split_by_comma]
                max = result[0][1]
                max_value = 0
                for i in range(5):
                    if result[i][1]>max:
                        max = result[i][1]
                        max_value = i
                # print(max, end=' ')
                # print(emotion[max_value])
                # print(line)
                global state
                state = emotion[max_value]
                print(state)
                if flag == False:                    
                    process.terminate()
                    break
        time.sleep(0.1)
    finally:
        # subprocess가 종료되면 반환 코드 확인
        return_code = process.wait()
        print(f"Subprocess exited with return code: {return_code}")
        
USE_WEBCAM = True

cam_id = 3
video_file = "https://storage.openvinotoolkit.org/repositories/openvino_notebooks/data/data/video/Coco%20Walking%20in%20Berkeley.mp4"
source = cam_id if USE_WEBCAM else video_file

flag = True

# thread1 = threading.Thread(target=dect)
# thread1.start()
# thread1.join()
thread2_arg = (source, isinstance(source, int), True)
thread2 = threading.Thread(target=run_style_transfer, args=thread2_arg)
thread2.start()

dect()
thread2.join()

for i in range(4):
    plt.subplot(4, 1, i + 1)
    plt.imshow(save_image[i], cmap='gray')
    plt.axis('off')
plt.show()
    
# run_style_transfer(source=source, flip=isinstance(source, int), use_popup=True)