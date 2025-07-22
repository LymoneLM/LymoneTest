from flask import Flask, render_template_string, Response, request, jsonify
import cv2
from multiprocessing import Process, Queue, Value
import time as systime
import numpy as np
import utils.motor as motor
from face_detect_rec import FaceDetectRec, faceDetecImgDis

app = Flask(__name__)

# 摄像头参数
CAM_WIDTH = 640
CAM_HEIGHT = 480

# 电机参数
MOTOR1_MIN = -175
MOTOR1_MAX = 175
MOTOR2_MIN = -65
MOTOR2_MAX = 65
STEP = 2  # 跟踪时每步角度

# 全局变量存储电机角度，初始为0
motor1_angle = Value('i', 0)
motor2_angle = Value('i', 0)

# 摄像头帧队列
q_view = Queue(maxsize=1)

# 人脸检测与跟踪进程
def camera_face_worker(q, m1_angle, m2_angle):
    cap = cv2.VideoCapture(0)
    detector = FaceDetectRec()
    width, height = CAM_WIDTH, CAM_HEIGHT
    m1, m2 = m1_angle, m2_angle
    # 电机初始归零
    m1.value = 0
    m2.value = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.resize(frame, (width, height))
        predictions = detector.inference(frame)
        # 只跟踪第一个人脸
        if predictions and predictions[0] is not None and len(predictions[0]) > 0:
            bbox = predictions[0][0]  # x1, y1, x2, y2, ...
            x1, y1, x2, y2 = bbox[:4]
            face_cx = int((x1 + x2) / 2)
            face_cy = int((y1 + y2) / 2)
            # 画面中心
            cx, cy = width // 2, height // 2
            # 计算偏移，简单比例控制
            dx = face_cx - cx
            dy = face_cy - cy
            # 允许一定死区，避免抖动
            dead_zone = 30
            # 水平跟踪（电机1）方向修正
            if abs(dx) > dead_zone:
                if dx > 0 and m1_angle.value > MOTOR1_MIN:
                    motor.rotate(motor.motor1, -STEP)  # 方向反转
                    m1_angle.value -= STEP
                elif dx < 0 and m1_angle.value < MOTOR1_MAX:
                    motor.rotate(motor.motor1, STEP)   # 方向反转
                    m1_angle.value += STEP
            # 垂直跟踪（电机2）方向修正
            if abs(dy) > dead_zone:
                if dy > 0 and m2_angle.value > MOTOR2_MIN:
                    motor.rotate(motor.motor2, -STEP)  # 方向反转
                    m2_angle.value -= STEP
                elif dy < 0 and m2_angle.value < MOTOR2_MAX:
                    motor.rotate(motor.motor2, STEP)   # 方向反转
                    m2_angle.value += STEP
        # 标注人脸
        frame, _ = faceDetecImgDis(frame, predictions)
        # 推送到队列
        _, jpeg = cv2.imencode('.jpg', frame)
        if not q.full():
            q.put(jpeg.tobytes())
        systime.sleep(0.03)

# 视频流生成器
def gen_video_stream(q):
    while True:
        if not q.empty():
            frame = q.get()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            systime.sleep(0.01)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>人脸跟踪摄像头系统</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Microsoft YaHei', Arial, sans-serif; background: #f4f6f8; margin: 0; padding: 0; }
        .container { max-width: 600px; margin: 40px auto; background: #fff; border-radius: 10px; box-shadow: 0 2px 8px #ccc; padding: 30px; }
        h2 { text-align: center; color: #333; }
        .info { margin: 20px 0; font-size: 1.2em; }
        .label { color: #888; }
        .cam-box { text-align: center; margin: 20px 0; }
        .cam-box img { border: 1px solid #888; border-radius: 6px; }
        .angle-box { text-align: center; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h2>人脸跟踪摄像头系统</h2>
        <div class="cam-box">
            <span class="label">摄像头画面（自动跟踪人脸）：</span><br>
            <img id="cam" src="/video_feed" width="640" height="480">
        </div>
        <div class="angle-box">
            <span class="label">电机一角度：</span><span id="motor1">--°</span>
            <span class="label">范围：-175°~175°</span>
            <span class="label">电机二角度：</span><span id="motor2">--°</span>
            <span class="label">范围：-65°~65°</span>
        </div>
    </div>
    <script>
        function updateData() {
            fetch('/status').then(r => r.json()).then(data => {
                document.getElementById('motor1').innerText = data.motor1 + '°';
                document.getElementById('motor2').innerText = data.motor2 + '°';
            });
        }
        setInterval(updateData, 1000);
        window.onload = updateData;
    </script>
</body>
</html>
'''

@app.route('/status')
def status():
    return jsonify({
        'motor1': motor1_angle.value,
        'motor2': motor2_angle.value
    })

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/video_feed')
def video_feed():
    return Response(gen_video_stream(q_view), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    p_cam = Process(target=camera_face_worker, args=(q_view, motor1_angle, motor2_angle))
    p_cam.daemon = True
    p_cam.start()
    app.run(host='0.0.0.0', port=5000, debug=False)