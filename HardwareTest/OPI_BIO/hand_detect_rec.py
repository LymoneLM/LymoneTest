import onnxruntime
import cv2
import numpy as np
import time

def draw_bd_handpose(img_, hand_, x, y):
    thick = 3
    colors = [(0, 215, 255), (255,115,55), (5,255,55), (25,15,255), (225,15,55)]

    cv2.line(img_, (int(hand_['0']['x']+x), int(hand_['0']['y']+y)),(int(hand_['1']['x']+x), int(hand_['1']['y']+y)), colors[0], thick, cv2.LINE_AA)
    cv2.line(img_, (int(hand_['1']['x']+x), int(hand_['1']['y']+y)),(int(hand_['2']['x']+x), int(hand_['2']['y']+y)), colors[0], thick, cv2.LINE_AA)
    cv2.line(img_, (int(hand_['2']['x']+x), int(hand_['2']['y']+y)),(int(hand_['3']['x']+x), int(hand_['3']['y']+y)), colors[0], thick, cv2.LINE_AA)
    cv2.line(img_, (int(hand_['3']['x']+x), int(hand_['3']['y']+y)),(int(hand_['4']['x']+x), int(hand_['4']['y']+y)), colors[0], thick, cv2.LINE_AA)

    cv2.line(img_, (int(hand_['0']['x']+x), int(hand_['0']['y']+y)),(int(hand_['5']['x']+x), int(hand_['5']['y']+y)), colors[1], thick, cv2.LINE_AA)
    cv2.line(img_, (int(hand_['5']['x']+x), int(hand_['5']['y']+y)),(int(hand_['6']['x']+x), int(hand_['6']['y']+y)), colors[1], thick, cv2.LINE_AA)
    cv2.line(img_, (int(hand_['6']['x']+x), int(hand_['6']['y']+y)),(int(hand_['7']['x']+x), int(hand_['7']['y']+y)), colors[1], thick, cv2.LINE_AA)
    cv2.line(img_, (int(hand_['7']['x']+x), int(hand_['7']['y']+y)),(int(hand_['8']['x']+x), int(hand_['8']['y']+y)), colors[1], thick, cv2.LINE_AA)

    cv2.line(img_, (int(hand_['0']['x']+x), int(hand_['0']['y']+y)),(int(hand_['9']['x']+x), int(hand_['9']['y']+y)), colors[2], thick, cv2.LINE_AA)
    cv2.line(img_, (int(hand_['9']['x']+x), int(hand_['9']['y']+y)),(int(hand_['10']['x']+x), int(hand_['10']['y']+y)), colors[2], thick, cv2.LINE_AA)
    cv2.line(img_, (int(hand_['10']['x']+x), int(hand_['10']['y']+y)),(int(hand_['11']['x']+x), int(hand_['11']['y']+y)), colors[2], thick, cv2.LINE_AA)
    cv2.line(img_, (int(hand_['11']['x']+x), int(hand_['11']['y']+y)),(int(hand_['12']['x']+x), int(hand_['12']['y']+y)), colors[2], thick, cv2.LINE_AA)

    cv2.line(img_, (int(hand_['0']['x']+x), int(hand_['0']['y']+y)),(int(hand_['13']['x']+x), int(hand_['13']['y']+y)), colors[3], thick, cv2.LINE_AA)
    cv2.line(img_, (int(hand_['13']['x']+x), int(hand_['13']['y']+y)),(int(hand_['14']['x']+x), int(hand_['14']['y']+y)), colors[3], thick, cv2.LINE_AA)
    cv2.line(img_, (int(hand_['14']['x']+x), int(hand_['14']['y']+y)),(int(hand_['15']['x']+x), int(hand_['15']['y']+y)), colors[3], thick, cv2.LINE_AA)
    cv2.line(img_, (int(hand_['15']['x']+x), int(hand_['15']['y']+y)),(int(hand_['16']['x']+x), int(hand_['16']['y']+y)), colors[3], thick, cv2.LINE_AA)

    cv2.line(img_, (int(hand_['0']['x']+x), int(hand_['0']['y']+y)),(int(hand_['17']['x']+x), int(hand_['17']['y']+y)), colors[4], thick, cv2.LINE_AA)
    cv2.line(img_, (int(hand_['17']['x']+x), int(hand_['17']['y']+y)),(int(hand_['18']['x']+x), int(hand_['18']['y']+y)), colors[4], thick, cv2.LINE_AA)
    cv2.line(img_, (int(hand_['18']['x']+x), int(hand_['18']['y']+y)),(int(hand_['19']['x']+x), int(hand_['19']['y']+y)), colors[4], thick, cv2.LINE_AA)
    cv2.line(img_, (int(hand_['19']['x']+x), int(hand_['19']['y']+y)),(int(hand_['20']['x']+x), int(hand_['20']['y']+y)), colors[4], thick, cv2.LINE_AA)

session = onnxruntime.InferenceSession("./models/hand_shufflenetv2.onnx",providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
ort_inputs = session.get_inputs()[0].name

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    img_width = frame.shape[1]
    img_height = frame.shape[0]

    # 输入图片预处理
    img_ = cv2.resize(frame, (256, 256),
                      interpolation=cv2.INTER_CUBIC)
    img_ = img_.astype(np.float32)
    img_ = (img_ - 128.) / 256.

    img_ = np.transpose(img_, [2, 0, 1])
    img_ = np.expand_dims(img_, axis=0)
    img_ = img_.astype(np.float32)

    s = time.time()
    output = session.run(None, {ort_inputs: img_})
    print('onnx Infer:{} ms.'.format((time.time() - s) * 1000))

    output = np.squeeze(output)

    pts_hand = {}  # 构建关键点连线可视化结构
    for i in range(int(output.shape[0] / 2)):
        x = (output[i * 2 + 0] * float(img_width))
        y = (output[i * 2 + 1] * float(img_height))

        pts_hand[str(i)] = {}
        pts_hand[str(i)] = {
            "x": x,
            "y": y,
        }

    draw_bd_handpose(frame, pts_hand, 0, 0)  # 绘制关键点连线

    # -------- 绘制关键点
    for i in range(int(output.shape[0] / 2)):
        x = (output[i * 2 + 0] * float(img_width))
        y = (output[i * 2 + 1] * float(img_height))

        cv2.circle(frame, (int(x), int(y)), 3, (255, 50, 60), -1)
        cv2.circle(frame, (int(x), int(y)), 1, (255, 150, 180), -1)

    # print(output)

    cv2.imshow("handposex", frame)
    cv2.waitKey(5)
