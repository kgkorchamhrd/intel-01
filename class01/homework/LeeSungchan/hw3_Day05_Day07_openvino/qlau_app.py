import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
import cv2
from PIL import ImageGrab  # Pillow 라이브러리가 필요합니다.
import openvino as ov
import notebook_utils as utils
import numpy as np

form_window = uic.loadUiType('./qlzu.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # self.on_btn.clicked.connect(self.start_video)

        # 웹캠 연결
        self.cap = cv2.VideoCapture(0)

        # 타이머 설정 (매 30 밀리초마다 웹캠에서 새로운 프레임을 획득)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # OpenVINO Core 초기화
        self.core = ov.Core()

        # Object Detection 모델 로드
        self.object_detection_model = self.core.read_model(model='./model/ssdlite_mobilenet_v2_fp16.xml')
        self.compiled_object_detection_model = self.core.compile_model(model=self.object_detection_model, device_name='CPU')

        # Monodepth 모델 로드
        self.monodepth_model = self.core.read_model("./model/MiDaS_small.xml")
        self.compiled_monodepth_model = self.core.compile_model(model=self.monodepth_model, device_name="CPU")

        # Object Detection 모델의 입력 크기 가져오기
        self.object_detection_input_shape = list(self.compiled_object_detection_model.input(0).shape)[1:3]

        self.classes = [
            "background", "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train",
            "truck", "boat", "traffic light", "fire hydrant", "street sign", "stop sign",
            "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant",
            "bear", "zebra", "giraffe", "hat", "backpack", "umbrella", "shoe", "eye glasses",
            "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
            "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle",
            "plate", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
            "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
            "couch", "potted plant", "bed", "mirror", "dining table", "window", "desk", "toilet",
            "door", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven",
            "toaster", "sink", "refrigerator", "blender", "book", "clock", "vase", "scissors",
            "teddy bear", "hair drier", "toothbrush", "hair brush"
        ]

        num_classes = len(self.classes)
        self.object_detection_colors = np.random.randint(0, 255, size=(num_classes, 3), dtype=np.uint8)

        self.threshold_distance = 0.2

    def start_video(self):
        self.cap.release()  # 이미 실행 중인 비디오 캡처를 정지하고, 다시 시작
        self.cap = cv2.VideoCapture(0)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # 웹캠에서 프레임 크기 조절
            scale = 1280 / max(frame.shape)
            if scale < 1:
                frame = cv2.resize(
                    src=frame,
                    dsize=None,
                    fx=scale,
                    fy=scale,
                    interpolation=cv2.INTER_AREA,
                )

            # Object Detection 모델 입력 크기에 맞게 조절
            input_img = cv2.resize(
                src=frame, dsize=tuple(self.object_detection_input_shape), interpolation=cv2.INTER_AREA
            )

            # Create a batch of images (size = 1).
            input_img = input_img[np.newaxis, ...]

            # Object Detection 모델 실행 및 결과 가져오기
            object_detection_results = self.compiled_object_detection_model([input_img])[0]

            # Object Detection 결과 처리
            object_detection_boxes = self.process_results(frame=frame, results=object_detection_results)

            # Object Detection 결과를 화면에 표시
            frame = self.draw_boxes(frame=frame, boxes=object_detection_boxes, classes=self.classes, colors=self.object_detection_colors)

            # Monodepth 모델 추론 및 특정 거리 이하일 때 경고 출력
            for detection in object_detection_boxes:
                # 추론 결과에서 관심 영역(ROI) 추출
                box = detection[2]
                roi = frame[box[1]:box[1] + box[3], box[0]:box[0] + box[2]]

                # 모델 입력 전처리
                input_frame = cv2.resize(roi, (256, 256))
                input_frame = cv2.cvtColor(input_frame, cv2.COLOR_BGR2RGB)
                input_frame = np.expand_dims(np.transpose(input_frame, (2, 0, 1)), 0)

                # Monodepth 모델 추론
                depth_map = self.compiled_monodepth_model([input_frame])[0].squeeze()

                # 특정 거리 값 이하일 때 알림 출력
                if np.min(depth_map) < self.threshold_distance:
                    # print(f"Warning:  {self.classes[detection[0]]} is too close!")
                    message = f"Warning: {self.classes[detection[0]]} is too close!"
                    self.p_label.setText(message)

            # QLabel에 캡처한 화면 표시
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.c_label.setPixmap(pixmap)

    def process_results(self, frame, results, thresh=0.6):
        h, w = frame.shape[:2]
        # The 'results' variable is a [1, 1, 100, 7] tensor.
        results = results.squeeze()
        boxes = []
        labels = []
        scores = []
        for _, label, score, xmin, ymin, xmax, ymax in results:
            boxes.append(
                tuple(map(int, (xmin * w, ymin * h, (xmax - xmin) * w, (ymax - ymin) * h)))
            )
            labels.append(int(label))
            scores.append(float(score))

        indices = cv2.dnn.NMSBoxes(
            bboxes=boxes, scores=scores, score_threshold=thresh, nms_threshold=0.6
        )

        if len(indices) == 0:
            return []

        return [(labels[idx], scores[idx], boxes[idx]) for idx in indices.flatten()]

    def draw_boxes(self, frame, boxes, classes, colors):
        for label, score, box in boxes:
            # Choose color for the label.
            color = tuple(map(int, colors[label]))
            # Draw a box.
            x2 = box[0] + box[2]
            y2 = box[1] + box[3]
            cv2.rectangle(img=frame, pt1=box[:2], pt2=(x2, y2), color=color, thickness=3)

            # Draw a label name inside the box.
            cv2.putText(
                img=frame,
                text=f"{classes[label]} {score:.2f}",
                org=(box[0] + 10, box[1] + 30),
                fontFace=cv2.FONT_HERSHEY_COMPLEX,
                fontScale=frame.shape[1] / 1000,
                color=color,
                thickness=1,
                lineType=cv2.LINE_AA,
            )

        return frame

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())
