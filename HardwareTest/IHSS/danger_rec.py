import cv2
import numpy as np
import onnxruntime as ort

YOLOV5N_MODEL_PATH = "models/yolov5n.onnx"
DANGER_CLASSES = ["fire", "gun", "knife"]  # 按照新顺序

class DangerDetectRec:
    def __init__(self, model_path=YOLOV5N_MODEL_PATH):
        self.model = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
        self.input_name = self.model.get_inputs()[0].name
        self.class_names = DANGER_CLASSES

    def preprocess(self, frame):
        img = cv2.resize(frame, (640, 640))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.transpose(2, 0, 1)  # HWC to CHW
        img = np.expand_dims(img, axis=0)
        img = img.astype(np.float32) / 255.0
        return img

    def inference(self, frame, conf_thres=0.5):
        img = self.preprocess(frame)
        outputs = self.model.run(None, {self.input_name: img})
        pred = outputs[0][0]  # (25200, 85)
        boxes = []
        for det in pred:
            obj_conf = det[4]
            class_scores = det[5:8]  # 只取前三类
            cls = np.argmax(class_scores)
            conf = obj_conf * class_scores[cls]
            if conf > conf_thres:
                x, y, w, h = det[0:4]
                x1 = int((x - w / 2) * frame.shape[1] / 640)
                y1 = int((y - h / 2) * frame.shape[0] / 640)
                x2 = int((x + w / 2) * frame.shape[1] / 640)
                y2 = int((y + h / 2) * frame.shape[0] / 640)
                boxes.append({
                    'bbox': [x1, y1, x2, y2],
                    'conf': float(conf),
                    'cls': int(cls),
                    'label': self.class_names[cls]
                })
        return boxes

