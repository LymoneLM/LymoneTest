import cv2
import mediapipe as mp
import numpy as np
import time
from flask import Flask, render_template_string, Response, request, jsonify
from multiprocessing import Process, Lock, Value, RawArray
from ctypes import c_char_p, c_bool
import utils.motor as motor
import utils.temp_hum as temp_hum
import utils.time as time_utils
from face_detect_rec import FaceDetectRec, faceDetecImgDis

# ----------------- 配置参数 -----------------
CAM_WIDTH = 640
CAM_HEIGHT = 480
MOTOR1_MIN = -175
MOTOR1_MAX = 175
MOTOR2_MIN = -65
MOTOR2_MAX = 65
MOTOR_STEP = 5

# ----------------- 共享内存与锁 -----------------
frame_lock = Lock()
landmarks_lock = Lock()

frame_dims = RawArray('i', [0, 0, 0])  # [H, W, C]
frame_buffer = RawArray('B', CAM_HEIGHT * CAM_WIDTH * 3)
landmarks_buffer = RawArray('d', 21 * 3)
shared_direction = Value(c_char_p, b"center")
show_hand_overlay = Value(c_bool, True)
show_face_overlay = Value(c_bool, True)
enable_face_tracking = Value(c_bool, False)
enable_hand_control = Value(c_bool, True)
motor1_angle = Value('i', 0)
motor2_angle = Value('i', 0)
last_motor_activity = Value('d', time.time())
motor_sleep_status = Value(c_bool, False)
# 移除palm_open_detected和palm_open_time
last_face_toggle_time = Value('d', 0.0)  # 新增：记录上次切换人脸追踪的时间

# ----------------- 摄像头进程 -----------------
def camera_process(frame_lock, frame_buffer, frame_dims):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
    with frame_lock:
        frame_dims[0], frame_dims[1], frame_dims[2] = CAM_HEIGHT, CAM_WIDTH, 3
    print("摄像头进程启动...")
    while True:
        ret, frame = cap.read()
        if ret:
            with frame_lock:
                frame_buffer_np = np.frombuffer(frame_buffer, dtype=np.uint8).reshape(frame_dims[:])
                np.copyto(frame_buffer_np, frame)
        else:
            time.sleep(0.05)
    cap.release()

# ----------------- 识别与控制进程 -----------------
def recognition_process(frame_lock, frame_buffer, frame_dims, landmarks_lock, landmarks_buffer, shared_direction):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False, max_num_hands=1,
        min_detection_confidence=0.7, min_tracking_confidence=0.7)
    face_detector = FaceDetectRec()
    frame_count = 0
    print("识别进程启动...")
    while True:
        time.sleep(0.05)
        frame_count += 1
        with frame_lock:
            if frame_dims[0] == 0:
                continue
            frame_buffer_np = np.frombuffer(frame_buffer, dtype=np.uint8).reshape(frame_dims[:])
            frame = frame_buffer_np.copy()
        frame = cv2.flip(frame, 1)
        # 手势识别
        do_hand = enable_hand_control.value
        do_face = enable_face_tracking.value
        # 手势识别每5帧
        if do_hand and frame_count % 5 == 0:
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)
            direction = b"center"
            found_hand = False
            if results.multi_hand_landmarks:
                found_hand = True
                hand_landmarks = results.multi_hand_landmarks[0]
                lm_array = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]).flatten()
                with landmarks_lock:
                    np.copyto(np.frombuffer(landmarks_buffer, dtype=np.float64), lm_array)
                # 判断张开/握拳
                points = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark])
                palm_center = points[0]
                finger_tips = points[[4, 8, 12, 16, 20]]
                avg_distance = np.mean(np.linalg.norm(finger_tips - palm_center, axis=1))
                # 五指张开判定
                def is_finger_open(tip, pip):
                    return (np.linalg.norm(points[tip][:2] - points[pip][:2]) > 0.07) and (points[tip][1] < points[pip][1])
                if avg_distance > 0.25 and all(is_finger_open(tip, pip) for tip, pip in [(4,3),(8,6),(12,10),(16,14),(20,18)]):
                    gesture = "open"
                else:
                    gesture = "closed"
                # 张开手掌切换人脸追踪（带冷却时间）
                now = time.time()
                if gesture == "open" and now - last_face_toggle_time.value > 2.0:
                    enable_face_tracking.value = not enable_face_tracking.value
                    last_face_toggle_time.value = now
                # 只有握拳时才允许方向识别
                if gesture == "closed":
                    thumb_tip = points[mp_hands.HandLandmark.THUMB_TIP.value]
                    index_finger_pip = points[mp_hands.HandLandmark.INDEX_FINGER_PIP.value]
                    pinky_pip = points[mp_hands.HandLandmark.PINKY_PIP.value]
                    wrist = points[mp_hands.HandLandmark.WRIST.value]
                    if thumb_tip[0] < wrist[0] and thumb_tip[0] < pinky_pip[0]:
                        direction = b"left"
                    elif thumb_tip[0] > wrist[0] and thumb_tip[0] > index_finger_pip[0]:
                        direction = b"right"
                    elif thumb_tip[1] < index_finger_pip[1] and thumb_tip[1] < wrist[1]:
                        direction = b"up"
                    elif thumb_tip[1] > wrist[1]:
                        direction = b"down"
                    else:
                        direction = b"center"
                else:
                    direction = b"center"
            with landmarks_lock:
                if not found_hand:
                    np.frombuffer(landmarks_buffer, dtype=np.float64)[0] = -1.0
            with shared_direction.get_lock():
                shared_direction.value = direction
            # 电机控制
            if not enable_face_tracking.value:
                if direction != b"center":
                    last_motor_activity.value = time.time()
                    if motor_sleep_status.value:
                        motor_sleep_status.value = False
                    if direction == b"up" and motor2_angle.value < MOTOR2_MAX:
                        motor.rotate(motor.motor2, MOTOR_STEP)
                        motor2_angle.value += MOTOR_STEP
                    elif direction == b"down" and motor2_angle.value > MOTOR2_MIN:
                        motor.rotate(motor.motor2, -MOTOR_STEP)
                        motor2_angle.value -= MOTOR_STEP
                    elif direction == b"left" and motor1_angle.value > MOTOR1_MIN:
                        motor.rotate(motor.motor1, -MOTOR_STEP)
                        motor1_angle.value -= MOTOR_STEP
                    elif direction == b"right" and motor1_angle.value < MOTOR1_MAX:
                        motor.rotate(motor.motor1, MOTOR_STEP)
                        motor1_angle.value += MOTOR_STEP
        # 人脸跟踪每15帧
        if do_face and frame_count % 15 == 0:
            predictions = face_detector.inference(frame)
            if predictions and predictions[0] is not None and len(predictions[0]) > 0:
                bbox = predictions[0][0]
                face_cx = int((bbox[0] + bbox[2]) / 2)
                face_cy = int((bbox[1] + bbox[3]) / 2)
                cx, cy = CAM_WIDTH // 2, CAM_HEIGHT // 2
                # 中心死区（中心框），例如宽高各80像素
                dead_zone_w = 80
                dead_zone_h = 80
                dx = face_cx - cx
                dy = face_cy - cy
                # 判断是否在中心框内
                if abs(dx) > dead_zone_w // 2:
                    # 离中心越远，步数越大（最大5步）
                    step_x = int(np.clip(abs(dx) / (CAM_WIDTH // 8), 1, 5)) * MOTOR_STEP
                    if dx > 0 and motor1_angle.value < MOTOR1_MAX:
                        # 右移（修正：人脸在右，电机应右转，画面左移）
                        motor.rotate(motor.motor1, step_x)
                        motor1_angle.value += step_x
                    elif dx < 0 and motor1_angle.value > MOTOR1_MIN:
                        # 左移
                        motor.rotate(motor.motor1, -step_x)
                        motor1_angle.value -= step_x
                if abs(dy) > dead_zone_h // 2:
                    step_y = int(np.clip(abs(dy) / (CAM_HEIGHT // 8), 1, 5)) * MOTOR_STEP
                    if dy > 0 and motor2_angle.value > MOTOR2_MIN:
                        # 下移
                        motor.rotate(motor.motor2, -step_y)
                        motor2_angle.value -= step_y
                    elif dy < 0 and motor2_angle.value < MOTOR2_MAX:
                        # 上移
                        motor.rotate(motor.motor2, step_y)
                        motor2_angle.value += step_y
                last_motor_activity.value = time.time()
                if motor_sleep_status.value:
                    motor_sleep_status.value = False
        # 电机休眠
        if time.time() - last_motor_activity.value > 30 and not motor_sleep_status.value:
            motor.sleep_motor()
            motor_sleep_status.value = True

# ----------------- Web/推流进程 -----------------
app = Flask(__name__)

# HTML模板
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>智能摄像头控制系统</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Microsoft YaHei', Arial, sans-serif; background: #f4f6f8; margin: 0; padding: 20px; }
        .container { 
            max-width: 1200px; 
            margin: auto; 
            display: grid;
            grid-template-columns: 1fr 300px;
            gap: 20px;
        }
        .main-content {
            background: #fff;
            border-radius: 10px;
            box-shadow: 0 2px 8px #ccc;
            padding: 20px;
        }
        .side-panel {
            background: #fff;
            border-radius: 10px;
            box-shadow: 0 2px 8px #ccc;
            padding: 20px;
            height: fit-content;
        }
        h2 { color: #333; margin-bottom: 20px; }
        .cam-box { margin-bottom: 20px; }
        .cam-box img { width: 100%; border-radius: 6px; }

        .control-group {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }

        .switch-container {
            display: flex;
            align-items: center;
            margin: 10px 0;
        }

        .switch-label {
            margin-right: 10px;
            color: #555;
            flex: 1;
        }

        .switch {
            position: relative;
            display: inline-block;
            width: 60px;
            height: 34px;
        }

        .switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }

        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: .4s;
            border-radius: 34px;
        }

        .slider:before {
            position: absolute;
            content: "";
            height: 26px;
            width: 26px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
        }

        input:checked + .slider {
            background-color: #2196F3;
        }

        input:checked + .slider:before {
            transform: translateX(26px);
        }

        .direction-pad {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 5px;
            width: 180px;
            margin: 20px auto;
        }

        .direction-pad button {
            padding: 15px;
            background: #2196F3;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 18px;
        }

        .direction-pad button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }

        .direction-pad .center {
            visibility: hidden;
        }

        .status-bar {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
        }

        .status-item {
            display: flex;
            align-items: center;
            margin: 5px 0;
        }

        .status-label {
            color: #666;
            width: 100px;
        }

        .status-value {
            font-weight: bold;
            color: #2196F3;
        }
    </style>
    <script>
        function updateStatus() {
            fetch('/status')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('direction').innerText = data.direction;
                    document.getElementById('motor1').innerText = data.motor1 + '°';
                    document.getElementById('motor2').innerText = data.motor2 + '°';
                    document.getElementById('temp').innerText = data.temp + ' ℃';
                    document.getElementById('hum').innerText = data.hum + ' %';
                    document.getElementById('time').innerText = data.time;
                    document.getElementById('face_tracking').checked = data.face_tracking;
                    document.getElementById('hand_control').checked = data.hand_control;
                    document.getElementById('show_hand').checked = data.show_hand;
                    document.getElementById('show_face').checked = data.show_face;

                    // 更新按钮状态
                    document.getElementById('m1_left').disabled = (data.motor1 <= -175);
                    document.getElementById('m1_right').disabled = (data.motor1 >= 175);
                    document.getElementById('m2_down').disabled = (data.motor2 <= -65);
                    document.getElementById('m2_up').disabled = (data.motor2 >= 65);
                });
        }

        function toggleControl(type) {
            fetch('/toggle_control', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({type: type})
            })
            .then(r => r.json())
            .then(updateStatus);
        }

        function moveMotor(motor, direction) {
            fetch('/move', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({motor: motor, direction: direction})
            })
            .then(r => r.json())
            .then(updateStatus);
        }

        window.onload = function() {
            updateStatus();
            setInterval(updateStatus, 500);
        };
    </script>
</head>
<body>
    <div class="container">
        <div class="main-content">
            <h2>智能摄像头控制系统</h2>
            <div class="cam-box">
                <img id="cam" src="/video_feed" alt="摄像头画面">
            </div>
        </div>

        <div class="side-panel">
            <div class="control-group">
                <h3>功能控制</h3>
                <div class="switch-container">
                    <span class="switch-label">人脸跟踪</span>
                    <label class="switch">
                        <input type="checkbox" id="face_tracking" onchange="toggleControl('face_tracking')">
                        <span class="slider"></span>
                    </label>
                </div>
                <div class="switch-container">
                    <span class="switch-label">手势控制</span>
                    <label class="switch">
                        <input type="checkbox" id="hand_control" onchange="toggleControl('hand_control')">
                        <span class="slider"></span>
                    </label>
                </div>
            </div>

            <div class="control-group">
                <h3>显示控制</h3>
                <div class="switch-container">
                    <span class="switch-label">显示手势标记</span>
                    <label class="switch">
                        <input type="checkbox" id="show_hand" onchange="toggleControl('show_hand')">
                        <span class="slider"></span>
                    </label>
                </div>
                <div class="switch-container">
                    <span class="switch-label">显示人脸标记</span>
                    <label class="switch">
                        <input type="checkbox" id="show_face" onchange="toggleControl('show_face')">
                        <span class="slider"></span>
                    </label>
                </div>
            </div>

            <div class="control-group">
                <h3>手动控制</h3>
                <div class="direction-pad">
                    <div></div>
                    <button id="m2_up" onclick="moveMotor(2, 1)">↑</button>
                    <div></div>
                    <button id="m1_left" onclick="moveMotor(1, -1)">←</button>
                    <div class="center"></div>
                    <button id="m1_right" onclick="moveMotor(1, 1)">→</button>
                    <div></div>
                    <button id="m2_down" onclick="moveMotor(2, -1)">↓</button>
                    <div></div>
                </div>
            </div>

            <div class="status-bar">
                <div class="status-item">
                    <span class="status-label">当前时间:</span>
                    <span class="status-value" id="time">--:--:--</span>
                </div>
                <div class="status-item">
                    <span class="status-label">温度:</span>
                    <span class="status-value" id="temp">-- ℃</span>
                </div>
                <div class="status-item">
                    <span class="status-label">湿度:</span>
                    <span class="status-value" id="hum">-- %</span>
                </div>
                <div class="status-item">
                    <span class="status-label">手势方向:</span>
                    <span class="status-value" id="direction">--</span>
                </div>
                <div class="status-item">
                    <span class="status-label">水平角度:</span>
                    <span class="status-value" id="motor1">0°</span>
                </div>
                <div class="status-item">
                    <span class="status-label">垂直角度:</span>
                    <span class="status-value" id="motor2">0°</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

def gen_video_stream():
    mp_hands = mp.solutions.hands
    face_detector = FaceDetectRec()
    while True:
        time.sleep(1/30)
        with frame_lock:
            if frame_dims[0] == 0:
                continue
            frame_buffer_np = np.frombuffer(frame_buffer, dtype=np.uint8).reshape(frame_dims[:])
            frame = frame_buffer_np.copy()
        frame = cv2.flip(frame, 1)
        # 手势overlay
        if show_hand_overlay.value:
            with landmarks_lock:
                landmarks_np = np.frombuffer(landmarks_buffer, dtype=np.float64)
                if landmarks_np[0] != -1.0:
                    landmarks_np = landmarks_np.reshape((21, 3))
                    height, width, _ = frame.shape
                    for connection in mp_hands.HAND_CONNECTIONS:
                        start_idx, end_idx = connection
                        start_point = (int(landmarks_np[start_idx][0] * width), int(landmarks_np[start_idx][1] * height))
                        end_point = (int(landmarks_np[end_idx][0] * width), int(landmarks_np[end_idx][1] * height))
                        cv2.line(frame, start_point, end_point, (0,255,0), 2)
                    for i in range(landmarks_np.shape[0]):
                        point = (int(landmarks_np[i][0] * width), int(landmarks_np[i][1] * height))
                        cv2.circle(frame, point, 5, (255,0,0), -1)
        # 人脸overlay
        if show_face_overlay.value and enable_face_tracking.value:
            predictions = face_detector.inference(frame)
            if predictions and predictions[0] is not None and len(predictions[0]) > 0:
                frame, _ = faceDetecImgDis(frame, predictions)
        _, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/video_feed')
def video_feed():
    return Response(gen_video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/status')
def status():
    try:
        h, m, s = time_utils.get_time()
    except Exception:
        t = time.localtime()
        h, m, s = t.tm_hour, t.tm_min, t.tm_sec
    now = f"{h:02d}:{m:02d}:{s:02d}"
    temp_raw = temp_hum.get_temp() if hasattr(temp_hum, 'get_temp') else None
    hum_raw = temp_hum.get_hum() if hasattr(temp_hum, 'get_hum') else None
    temp = round(temp_raw / 10, 1) if temp_raw is not None else '--'
    hum = round(hum_raw / 10, 1) if hum_raw is not None else '--'
    with shared_direction.get_lock():
        direction = shared_direction.value.decode('utf-8')
    return jsonify({
        'time': now,
        'temp': temp,
        'hum': hum,
        'direction': direction,
        'motor1': motor1_angle.value,
        'motor2': motor2_angle.value,
        'face_tracking': enable_face_tracking.value,
        'hand_control': enable_hand_control.value,
        'show_hand': show_hand_overlay.value,
        'show_face': show_face_overlay.value
    })

@app.route('/toggle_control', methods=['POST'])
def toggle_control():
    data = request.get_json()
    control_type = data.get('type')
    if control_type == 'face_tracking':
        enable_face_tracking.value = not enable_face_tracking.value
    elif control_type == 'hand_control':
        enable_hand_control.value = not enable_hand_control.value
    elif control_type == 'show_hand':
        show_hand_overlay.value = not show_hand_overlay.value
    elif control_type == 'show_face':
        show_face_overlay.value = not show_face_overlay.value
    return jsonify({'success': True})

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    motor_id = data.get('motor')
    direction = data.get('direction')
    last_motor_activity.value = time.time()
    if motor_sleep_status.value:
        motor_sleep_status.value = False
    if motor_id == 1:
        new_angle = motor1_angle.value + direction * MOTOR_STEP
        if MOTOR1_MIN <= new_angle <= MOTOR1_MAX:
            motor.rotate(motor.motor1, direction * MOTOR_STEP)
            motor1_angle.value = new_angle
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': '电机一已达极限'})
    elif motor_id == 2:
        new_angle = motor2_angle.value + direction * MOTOR_STEP
        if MOTOR2_MIN <= new_angle <= MOTOR2_MAX:
            motor.rotate(motor.motor2, direction * MOTOR_STEP)
            motor2_angle.value = new_angle
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': '电机二已达极限'})
    return jsonify({'success': False, 'error': '参数错误'})

if __name__ == '__main__':
    p_camera = Process(target=camera_process, args=(frame_lock, frame_buffer, frame_dims))
    p_recognition = Process(target=recognition_process, args=(frame_lock, frame_buffer, frame_dims, landmarks_lock, landmarks_buffer, shared_direction))
    p_camera.daemon = True
    p_recognition.daemon = True
    p_camera.start()
    p_recognition.start()
    print("Web服务已启动，请访问 http://<设备IP>:8081")
    try:
        app.run(host='0.0.0.0', port=8081, debug=False)
    except KeyboardInterrupt:
        print("\n正在关闭所有进程...")
    finally:
        p_camera.terminate()
        p_recognition.terminate()
        p_camera.join()
        p_recognition.join()
        print("所有进程已关闭。")
