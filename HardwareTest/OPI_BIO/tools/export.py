import onnxruntime as ort
import numpy as np
from PIL import Image, ImageDraw
import sys
import os

def preprocess(img_path, img_size=640):
    img = Image.open(img_path).convert('RGB')
    img = img.resize((img_size, img_size))
    img_np = np.array(img).astype(np.float32)
    img_np = img_np / 255.0  # 归一化
    img_np = np.transpose(img_np, (2, 0, 1))  # HWC to CHW
    img_np = np.expand_dims(img_np, axis=0)   # Add batch dim
    return img_np, img

def postprocess(pred, conf_thres=0.25, iou_thres=0.45):
    # pred: [1, num_boxes, 85] (YOLOv5 ONNX输出)
    pred = np.squeeze(pred, axis=0)
    boxes = []
    for det in pred:
        conf = det[4]
        if conf < conf_thres:
            continue
        x1, y1, x2, y2 = det[:4]
        cls = np.argmax(det[5:])
        boxes.append([x1, y1, x2, y2, conf, cls])
    # 简单NMS（可用更优实现）
    boxes = sorted(boxes, key=lambda x: x[4], reverse=True)
    keep = []
    while boxes:
        box = boxes.pop(0)
        keep.append(box)
        boxes = [b for b in boxes if iou(box, b) < iou_thres]
    return keep

def iou(box1, box2):
    # 计算两个框的IoU
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union = area1 + area2 - inter
    return inter / union if union > 0 else 0

def save_results(boxes, save_path):
    with open(save_path, 'w') as f:
        for box in boxes:
            f.write(f"{box[0]:.2f},{box[1]:.2f},{box[2]:.2f},{box[3]:.2f},{box[4]:.4f},{int(box[5])}\n")

def draw_boxes(img, boxes, save_path):
    draw = ImageDraw.Draw(img)
    for box in boxes:
        draw.rectangle([box[0], box[1], box[2], box[3]], outline='red', width=2)
        draw.text((box[0], box[1]), f"{int(box[5])}:{box[4]:.2f}", fill='red')
    img.save(save_path)

if __name__ == "__main__":
    # 参数
    onnx_path = "models/safe_detect.onnx"
    img_path = "data/131.jpg"
    result_txt = "results.txt"
    result_img = "results.jpg"
    img_size = 640

    # 1. 预处理
    input_tensor, orig_img = preprocess(img_path, img_size)

    # 2. ONNX推理
    session = ort.InferenceSession(onnx_path, providers=['CPUExecutionProvider'])
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    pred = session.run([output_name], {input_name: input_tensor})[0]

    # 3. 后处理
    boxes = postprocess(pred)

    # 4. 保存结果
    save_results(boxes, result_txt)
    draw_boxes(orig_img, boxes, result_img)
    print(f"检测结果已保存到 {result_txt} 和 {result_img}")