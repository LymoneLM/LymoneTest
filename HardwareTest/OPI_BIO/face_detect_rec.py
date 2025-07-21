from components.utils import getFaceBoxs
from components.onnx_infer import OnnxRun
from components.config import ai_cfg
import numpy as np
import cv2
import time

FACE_DET_PATH = "models/scrfd.onnx"

class FaceDetectRec(object):
    def __init__(self, face_det_path=FACE_DET_PATH):
        self.onnx_run = OnnxRun(model_path=face_det_path)
        self.predictions = []

    def imgPreprocessing(self, img):
        im_ratio = float(img.shape[0]) / img.shape[1]
        model_ratio = float(ai_cfg.INPUT_SIZE[1]) / ai_cfg.INPUT_SIZE[0]
        if im_ratio > model_ratio:
            new_height = ai_cfg.INPUT_SIZE[1]
            new_width = int(new_height / im_ratio)
        else:
            new_width = ai_cfg.INPUT_SIZE[0]
            new_height = int(new_width * im_ratio)

        resized_img = cv2.resize(img, (new_width, new_height))
        det_img = np.zeros((ai_cfg.INPUT_SIZE[1], ai_cfg.INPUT_SIZE[0], 3), dtype=np.uint8)
        det_img[:new_height, :new_width, :] = resized_img

        input_size = tuple(det_img.shape[0:2][::-1])
        input_data = cv2.dnn.blobFromImage(det_img, 1.0 / 128, input_size,
                                           (127.5, 127.5, 127.5), swapRB=True)
        return input_data

    def inference(self, img):
        input_data = self.imgPreprocessing(img)
        net_outs = self.onnx_run.inference(input_data)
        bboxes, kpss = getFaceBoxs(img, net_outs, input_size=(ai_cfg.INPUT_SIZE))

        tracked_boxes = bboxes
        self.predictions = [tracked_boxes, kpss]
        return self.predictions


def faceDetecImgDis(img, predictions):
    img = img.copy()
    face_name = 0
    if predictions:
        tracked_boxes, kpss = predictions
        for i, bbox in enumerate(tracked_boxes):
            x, y, w, h, trk_id = bbox

            trk_id = i + 1
            if face_name < trk_id:
                face_name = trk_id
            cv2.rectangle(img, (int(x), int(y)), (int(w), int(h)), (255, 255, 0), 2)

            # cv2.putText(img, str(trk_id), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX,
            #             1, (0, 0, 255), 2, cv2.LINE_AA)
        for kps in kpss:
            for kp in kps:
                kp = kp.astype(np.int16)
                cv2.circle(img, tuple(kp), 1, (0, 0, 255), 2)
    return img, face_name

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    face_mask_rec = FaceDetectRec()

    while True:
        ret, img = cap.read()
        img = cv2.resize(img, (640, 480))
        st = time.time()
        face_mask_pricet = face_mask_rec.inference(img)
        img, face_num = faceDetecImgDis(img, face_mask_pricet)
        print("onnx_time{}ms".format((time.time() - st) * 1000))

        cv2.imshow("face_detect", img)
        cv2.waitKey(1)

