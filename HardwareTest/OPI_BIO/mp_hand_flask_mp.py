import cv2
import mediapipe as mp
import motor
import time
import numpy as np
from flask import Flask, render_template_string, jsonify, Response
from multiprocessing import Process, Lock, Value, RawArray
from ctypes import c_char_p, c_bool, c_double

# ----------------- 共享函数 -----------------

def get_thumb_direction(hand_landmarks_np):
    """根据numpy格式的关键点数据判断方向"""
    # 重新映射关键点
    thumb_tip = hand_landmarks_np[mp.solutions.hands.HandLandmark.THUMB_TIP]
    index_finger_pip = hand_landmarks_np[mp.solutions.hands.HandLandmark.INDEX_FINGER_PIP]
    pinky_pip = hand_landmarks_np[mp.solutions.hands.HandLandmark.PINKY_PIP]
    wrist = hand_landmarks_np[mp.solutions.hands.HandLandmark.WRIST]

    if thumb_tip[0] < wrist[0] and thumb_tip[0] < pinky_pip[0]:
        return b"left"
    if thumb_tip[0] > wrist[0] and thumb_tip[0] > index_finger_pip[0]:
        return b"right"
    if thumb_tip[1] < index_finger_pip[1] and thumb_tip[1] < wrist[1]:
        return b"up"
    if thumb_tip[1] > wrist[1]:
        return b"down"
    return b"center"

# ----------------- 进程1: 摄像头捕获 -----------------

def camera_process(frame_lock, frame_buffer, frame_dims):
    """以最快速度从摄像头捕获图像并存入共享内存"""
    try:
        cap = cv2.VideoCapture(0)
        width, height = 640, 480
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        with frame_lock:
            frame_dims[0], frame_dims[1], frame_dims[2] = height, width, 3

        print("摄像头进程启动...")
        while True:
            success, frame = cap.read()
            if success:
                with frame_lock:
                    # 将图像数据复制到共享内存
                    frame_buffer_np = np.frombuffer(frame_buffer, dtype=np.uint8).reshape(frame_dims[:])
                    np.copyto(frame_buffer_np, frame)
            else:
                time.sleep(0.1) # 读取失败时等待
    except Exception as e:
        print(f"摄像头进程错误: {e}")
    finally:
        if 'cap' in locals() and cap.isOpened():
            cap.release()
        print("摄像头进程已关闭")

# ----------------- 进程2: 手势识别与控制 -----------------

def recognition_process(frame_lock, frame_buffer, frame_dims, landmarks_lock, landmarks_buffer, shared_direction):
    """独立于显示，进行手势识别和电机控制"""
    try:
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=False, max_num_hands=1,
            min_detection_confidence=0.7, min_tracking_confidence=0.7)

        MOTOR_STEP = 10
        last_move_time = 0
        move_interval = 1.0
        
        print("识别进程启动...")
        while True:
            time.sleep(0.1)  # 控制识别频率，约10 FPS

            with frame_lock:
                if frame_dims[0] == 0: continue # 等待摄像头初始化
                frame_buffer_np = np.frombuffer(frame_buffer, dtype=np.uint8).reshape(frame_dims[:])
                frame_copy = frame_buffer_np.copy()
            
            # 关键修复: 在识别前也进行水平翻转，与显示保持一致
            frame_copy = cv2.flip(frame_copy, 1)

            image_rgb = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB)
            image_rgb.flags.writeable = False
            results = hands.process(image_rgb)

            direction = b"center"
            found_hand = False
            if results.multi_hand_landmarks:
                found_hand = True
                hand_landmarks = results.multi_hand_landmarks[0]
                
                # 将关键点数据存入共享内存
                lm_array = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]).flatten()
                with landmarks_lock:
                    landmarks_buffer_np = np.frombuffer(landmarks_buffer, dtype=np.float64)
                    np.copyto(landmarks_buffer_np, lm_array)

                direction = get_thumb_direction(np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]))
            
            with landmarks_lock:
                # 如果没有找到手，将第一个坐标设为-1作为标记
                if not found_hand:
                    np.frombuffer(landmarks_buffer, dtype=np.float64)[0] = -1.0
            
            with shared_direction.get_lock():
                shared_direction.value = direction

            # 电机控制
            current_time = time.time()
            if direction != b"center" and (current_time - last_move_time > move_interval):
                last_move_time = current_time
                if direction == b"up": motor.rotate(motor.motor2, MOTOR_STEP)
                elif direction == b"down": motor.rotate(motor.motor2, -MOTOR_STEP)
                elif direction == b"left": motor.rotate(motor.motor1, -MOTOR_STEP)
                elif direction == b"right": motor.rotate(motor.motor1, MOTOR_STEP)

    except Exception as e:
        print(f"识别进程错误: {e}")
    finally:
        print("识别进程已关闭")

# ----------------- 进程3: Flask Web服务器 -----------------

app = Flask(__name__)

# (HTML_TEMPLATE 和其他 Flask 路由保持和之前一致)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>手势控制摄像头UI</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Microsoft YaHei', Arial, sans-serif; background: #f4f6f8; margin: 0; padding: 20px; text-align: center; }
        .container { max-width: 700px; margin: auto; background: #fff; border-radius: 10px; box-shadow: 0 2px 8px #ccc; padding: 30px; }
        h2 { color: #333; }
        .cam-box { margin: 20px 0; }
        .cam-box img { border: 1px solid #888; border-radius: 6px; width: 100%; max-width: 640px; }
        .status-bar { 
            margin-top: 20px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center;
            padding: 0 20px;
        }
        .status { 
            font-size: 1.2em; 
            display: flex;
            align-items: center;
        }
        .label { color: #555; margin-right: 10px; }
        #direction { color: #0078d7; font-weight: bold; }
        .error { color: red; margin: 10px 0; }
        
        /* 开关样式 */
        .switch-container {
            display: flex;
            align-items: center;
        }
        .switch-label {
            margin-right: 10px;
            color: #555;
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
            background-color: #0078d7;
        }
        input:checked + .slider:before {
            transform: translateX(26px);
        }
    </style>
    <script>
        let overlayEnabled = true;
        
        function updateStatus() {
            fetch('/status')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('direction').innerText = data.direction;
                })
                .catch(err => {
                    console.error('状态更新错误:', err);
                });
        }
        
        function toggleOverlay() {
            fetch('/toggle_overlay', {
                method: 'POST'
            })
            .then(r => r.json())
            .then(data => {
                overlayEnabled = data.show_overlay;
                document.getElementById('overlaySwitch').checked = overlayEnabled;
            });
        }
        
        window.onload = function() {
            updateStatus();
            setInterval(updateStatus, 500);
            
            document.getElementById('cam').onerror = function() {
                this.style.display = 'none';
                let error = document.createElement('div');
                error.className = 'error';
                error.innerText = '视频流加载失败，请刷新页面重试';
                this.parentElement.appendChild(error);
            };
        };
    </script>
</head>
<body>
    <div class="container">
        <h2>手势控制摄像头UI (多进程优化版)</h2>
        <div class="cam-box">
            <img id="cam" src="/video_feed" alt="摄像头画面">
        </div>
        <div class="status-bar">
            <div class="switch-container">
                <span class="switch-label">显示标记</span>
                <label class="switch">
                    <input type="checkbox" id="overlaySwitch" checked onclick="toggleOverlay()">
                    <span class="slider"></span>
                </label>
            </div>
            <div class="status">
                <span class="label">当前检测方向:</span>
                <span id="direction">--</span>
            </div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/toggle_overlay', methods=['POST'])
def toggle_overlay():
    with show_overlay.get_lock():
        show_overlay.value = not show_overlay.value
        return jsonify({'show_overlay': show_overlay.value})

def gen_video_stream():
    """从共享内存读取数据，合成视频流"""
    mp_hands = mp.solutions.hands
    
    while True:
        time.sleep(1/30) # 控制推流帧率
        with frame_lock:
            if frame_dims[0] == 0: continue
            frame_buffer_np = np.frombuffer(frame_buffer, dtype=np.uint8).reshape(frame_dims[:])
            frame = frame_buffer_np.copy()
        
        frame = cv2.flip(frame, 1)

        do_show = False
        with show_overlay.get_lock():
            do_show = show_overlay.value
            
        if do_show:
            with landmarks_lock:
                landmarks_np = np.frombuffer(landmarks_buffer, dtype=np.float64)
                if landmarks_np[0] != -1.0:
                    landmarks_np = landmarks_np.reshape((21, 3))
                    height, width, _ = frame.shape
                    
                    # 手动绘制连接线
                    for connection in mp_hands.HAND_CONNECTIONS:
                        start_idx = connection[0]
                        end_idx = connection[1]
                        
                        start_point = (int(landmarks_np[start_idx][0] * width), int(landmarks_np[start_idx][1] * height))
                        end_point = (int(landmarks_np[end_idx][0] * width), int(landmarks_np[end_idx][1] * height))
                        
                        cv2.line(frame, start_point, end_point, (0, 255, 0), 2)
                        
                    # 手动绘制关键点
                    for i in range(landmarks_np.shape[0]):
                        point = (int(landmarks_np[i][0] * width), int(landmarks_np[i][1] * height))
                        cv2.circle(frame, point, 5, (255, 0, 0), -1)
        
        _, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

# 其他路由...
@app.route('/')
def index(): return render_template_string(HTML_TEMPLATE)

@app.route('/status')
def status():
    with shared_direction.get_lock():
        return jsonify({'direction': shared_direction.value.decode('utf-8')})

@app.route('/video_feed')
def video_feed():
    return Response(gen_video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # 定义共享内存和锁
    frame_lock = Lock()
    landmarks_lock = Lock()
    
    # 摄像头帧共享
    H, W, C = 480, 640, 3
    frame_dims = RawArray('i', [0, 0, 0]) # [H, W, C]
    frame_buffer = RawArray('B', H * W * C)
    
    # 关键点共享 (21个点,每个点3个坐标)
    landmarks_buffer = RawArray('d', 21 * 3)
    
    # 状态共享
    shared_direction = Value(c_char_p, b"center")
    show_overlay = Value(c_bool, True)

    # 启动子进程
    p_camera = Process(target=camera_process, args=(frame_lock, frame_buffer, frame_dims))
    p_recognition = Process(target=recognition_process, args=(frame_lock, frame_buffer, frame_dims, landmarks_lock, landmarks_buffer, shared_direction))
    
    p_camera.daemon = True
    p_recognition.daemon = True
    
    p_camera.start()
    p_recognition.start()
    
    print("Web服务已启动，请访问 http://<设备IP>:5000")
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n正在关闭所有进程...")
    finally:
        p_camera.terminate()
        p_recognition.terminate()
        p_camera.join()
        p_recognition.join()
        print("所有进程已关闭。") 