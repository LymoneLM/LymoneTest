from flask import Flask, render_template_string, jsonify, Response
import cv2
import mediapipe as mp
import motor
import time
from multiprocessing import Process, Queue, Value
from ctypes import c_char_p, c_bool
import numpy as np

# ----------------- Mediapipe and Motor Control Logic -----------------

def get_thumb_direction(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

    if thumb_tip.x < wrist.x and thumb_tip.x < pinky_pip.x:
        return b"left"
    if thumb_tip.x > wrist.x and thumb_tip.x > index_finger_pip.x:
        return b"right"
    if thumb_tip.y < index_finger_pip.y and thumb_tip.y < wrist.y:
        return b"up"
    if thumb_tip.y > wrist.y:
        return b"down"
    return b"center"

# ----------------- Background Worker Process -----------------

def hand_detection_worker(q_video, shared_direction, show_overlay):
    """
    后台进程: 捕获摄像头, 运行手势识别, 控制电机, 并将数据放入队列
    """
    try:
        # 初始化 Mediapipe
        global mp_hands
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7)
        mp_drawing = mp.solutions.drawing_utils
        
        # 打开摄像头
        cap = cv2.VideoCapture(0)
        # 设置摄像头分辨率
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # 电机控制参数
        MOTOR_STEP = 10
        last_move_time = 0
        move_interval = 1.0  # 秒

        # 手势识别控制参数
        PROCESS_INTERVAL = 10  # 每隔多少帧进行一次手势识别
        frame_count = 0
        last_direction = b"center"  # 保存最后一次识别的方向
        last_landmarks = None  # 保存最后一次识别的关键点

        print("摄像头和手势识别初始化完成")
        print(f"当前设置：每{PROCESS_INTERVAL}帧进行一次手势识别")

        while True:
            success, image = cap.read()
            if not success:
                print("无法读取摄像头数据")
                time.sleep(1)
                continue

            try:
                # 图像处理
                image = cv2.flip(image, 1)  # 水平翻转
                
                # 每 PROCESS_INTERVAL 帧进行一次手势识别
                if frame_count % PROCESS_INTERVAL == 0:
                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    results = hands.process(image_rgb)

                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            last_landmarks = hand_landmarks  # 保存关键点
                            last_direction = get_thumb_direction(hand_landmarks)
                            
                            # 电机控制
                            current_time = time.time()
                            if last_direction != b"center" and (current_time - last_move_time > move_interval):
                                last_move_time = current_time
                                try:
                                    if last_direction == b"up":
                                        motor.rotate(motor.motor2, MOTOR_STEP)
                                    elif last_direction == b"down":
                                        motor.rotate(motor.motor2, -MOTOR_STEP)
                                    elif last_direction == b"left":
                                        motor.rotate(motor.motor1, -MOTOR_STEP)
                                    elif last_direction == b"right":
                                        motor.rotate(motor.motor1, MOTOR_STEP)
                                except Exception as e:
                                    print(f"电机控制错误: {str(e)}")
                    else:
                        last_landmarks = None
                        last_direction = b"center"

                # 根据开关状态决定是否显示叠加层
                if show_overlay.value:
                    # 使用最后一次识别的结果绘制关键点
                    if last_landmarks is not None:
                        mp_drawing.draw_landmarks(
                            image, 
                            last_landmarks, 
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(0,255,0), thickness=2),
                            mp_drawing.DrawingSpec(color=(0,0,255), thickness=2)
                        )

                    # 在图像上显示方向和帧计数信息
                    cv2.putText(
                        image, 
                        f"{last_direction.decode('utf-8')} ({frame_count % PROCESS_INTERVAL}/{PROCESS_INTERVAL})", 
                        (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        1, 
                        (0, 255, 0), 
                        2
                    )

                # 更新共享变量
                with shared_direction.get_lock():
                    shared_direction.value = last_direction

                # 将帧编码为JPEG并放入队列
                try:
                    _, jpeg = cv2.imencode('.jpg', image)
                    if not q_video.full():
                        q_video.put(jpeg.tobytes())
                    else:
                        q_video.get()  # 丢弃旧帧
                        q_video.put(jpeg.tobytes())
                except Exception as e:
                    print(f"图像编码错误: {str(e)}")

                # 更新帧计数器
                frame_count = (frame_count + 1) % 1000  # 防止数字太大

            except Exception as e:
                print(f"处理循环错误: {str(e)}")
                continue

    except Exception as e:
        print(f"Worker进程初始化错误: {str(e)}")
    finally:
        print("正在清理资源...")
        try:
            for pin in motor.pins:
                motor.wiringpi.digitalWrite(pin, 0)
        except:
            pass
        try:
            cap.release()
        except:
            pass
        print("资源清理完成")

# ----------------- Flask Web Application -----------------

app = Flask(__name__)

# HTML模板更新
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
        <h2>手势控制摄像头UI</h2>
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

def gen_video_stream(q):
    """生成视频流"""
    while True:
        if not q.empty():
            frame = q.get()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            time.sleep(0.01)

@app.route('/status')
def status():
    """获取当前状态"""
    try:
        with shared_direction.get_lock():
            current_direction = shared_direction.value.decode('utf-8')
        return jsonify({'direction': current_direction})
    except Exception as e:
        return jsonify({'direction': 'error', 'message': str(e)})

@app.route('/toggle_overlay', methods=['POST'])
def toggle_overlay():
    """切换显示开关"""
    show_overlay.value = not show_overlay.value
    return jsonify({'show_overlay': show_overlay.value})

@app.route('/')
def index():
    """主页"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/video_feed')
def video_feed():
    """视频流"""
    return Response(
        gen_video_stream(q_video),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

if __name__ == '__main__':
    try:
        # 创建用于进程间通信的队列和共享内存
        q_video = Queue(maxsize=2)
        shared_direction = Value(c_char_p, b"center")
        show_overlay = Value(c_bool, True)  # 显示开关，默认开启

        # 创建并启动后台工作进程
        p_worker = Process(target=hand_detection_worker, args=(q_video, shared_direction, show_overlay))
        p_worker.daemon = True
        p_worker.start()
        
        print("Web服务已启动，请访问:")
        print("http://127.0.0.1:5000 或")
        print("http://<设备IP>:5000")
        
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序发生错误: {str(e)}")
    finally:
        print("正在关闭服务...") 