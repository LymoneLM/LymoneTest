import cv2
import numpy as np
import onnxruntime
from flask import Flask, render_template_string, Response, jsonify
from multiprocessing import Process, Queue, Value
import time
import utils.motor as motor  # 引入电机控制模块

# --- 全局配置 ---
# Flask应用
app = Flask(__name__)
# 摄像头帧队列
q_view = Queue(maxsize=1)

# --- 电机参数 ---
MOTOR1_MIN = -175
MOTOR1_MAX = 175
MOTOR2_MIN = -65
MOTOR2_MAX = 65
STEP = 3  # 手势控制时每步角度

# 使用多进程安全的值来存储电机角度
motor1_angle = Value('i', 0)
motor2_angle = Value('i', 0)

# ONNX模型加载
try:
    session = onnxruntime.InferenceSession(
        "./models/hand_shufflenetv2.onnx",
        providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
    )
    ort_inputs_name = session.get_inputs()[0].name
except Exception as e:
    print(f"模型加载失败: {e}")
    session = None

# --- 手势绘制与识别 ---
def draw_bd_handpose(img_, hand_, x_offset=0, y_offset=0):
    """在图像上绘制手部骨架"""
    thick = 3
    colors = [(0, 215, 255), (255, 115, 55), (5, 255, 55), (25, 15, 255), (225, 15, 55)]
    points_to_draw = [
        (0, 1, 0), (1, 2, 0), (2, 3, 0), (3, 4, 0),
        (0, 5, 1), (5, 6, 1), (6, 7, 1), (7, 8, 1),
        (0, 9, 2), (9, 10, 2), (10, 11, 2), (11, 12, 2),
        (0, 13, 3), (13, 14, 3), (14, 15, 3), (15, 16, 3),
        (0, 17, 4), (17, 18, 4), (18, 19, 4), (19, 20, 4)
    ]
    for start_idx, end_idx, color_idx in points_to_draw:
        start_pt = (int(hand_[str(start_idx)]['x'] + x_offset), int(hand_[str(start_idx)]['y'] + y_offset))
        end_pt = (int(hand_[str(end_idx)]['x'] + x_offset), int(hand_[str(end_idx)]['y'] + y_offset))
        cv2.line(img_, start_pt, end_pt, colors[color_idx], thick, cv2.LINE_AA)

def recognize_gesture(pts_hand):
    """
    根据张开的手掌方向识别手势。
    1. 先判断手是否为张开状态，若集中或扭曲则返回静止。
    2. 若手是张开的，则根据手腕到中指根部的向量判断方向。
    pts_hand: 包含21个关键点坐标的字典
    """
    if not pts_hand:
        return "No_Hand"

    # --- 步骤 1: 判断手是否集中或扭曲 (复用之前的逻辑) ---
    try:
        x_coords = [p['x'] for p in pts_hand.values()]
        y_coords = [p['y'] for p in pts_hand.values()]
        
        bbox_width = max(x_coords) - min(x_coords)
        bbox_height = max(y_coords) - min(y_coords)
        
        p5 = np.array([pts_hand['5']['x'], pts_hand['5']['y']])
        p17 = np.array([pts_hand['17']['x'], pts_hand['17']['y']])
        palm_width = np.linalg.norm(p5 - p17)

        if palm_width < 1e-6:
             return "Hand_Concentrated"

        spread_ratio = max(bbox_width, bbox_height) / palm_width
        
        # 如果手部不够“舒展”，则认为是集中状态，不进行移动
        # 这个阈值可以根据实际效果微调
        SPREAD_THRESHOLD = 3.0
        if spread_ratio < SPREAD_THRESHOLD:
            return "Hand_Concentrated"

    except (KeyError, IndexError):
        return "Hand_Concentrated" # 关键点缺失，视为集中状态

    # --- 步骤 2: 计算手掌方向向量并分类 ---
    try:
        # 使用手腕(0)到中指根部(9)的向量代表手掌方向
        p0 = np.array([pts_hand['0']['x'], pts_hand['0']['y']])
        p9 = np.array([pts_hand['9']['x'], pts_hand['9']['y']])
        
        dx = p9[0] - p0[0]
        dy = p9[1] - p0[1]

        # 阈值，避免微小抖动
        threshold = 15

        # 比较水平和垂直分量的绝对值，以确定主方向
        if abs(dx) > abs(dy): # 水平方向为主
            if dx > threshold:
                return "Palm_Right"
            elif dx < -threshold:
                return "Palm_Left"
        elif abs(dy) > abs(dx): # 垂直方向为主
            if dy < -threshold: # y减小是向上
                return "Palm_Up"
            elif dy > threshold:
                return "Palm_Down"
                
    except (KeyError, IndexError):
        return "Hand_Concentrated"

    return "Palm_Static"


def control_motor_by_gesture(gesture, m1_angle, m2_angle):
    """
    根据手势控制电机转动
    """
    # 水平控制 (Motor 1)
    if gesture == "Palm_Right":  # 手掌朝右 -> 摄像头向左 (物理)
        if m1_angle.value > MOTOR1_MIN:
            motor.rotate(motor.motor1, -STEP)
            m1_angle.value -= STEP
    elif gesture == "Palm_Left": # 手掌朝左 -> 摄像头向右 (物理)
        if m1_angle.value < MOTOR1_MAX:
            motor.rotate(motor.motor1, STEP)
            m1_angle.value += STEP
            
    # 垂直控制 (Motor 2) - 方向保持不变
    elif gesture == "Palm_Up": # 手掌朝上 -> 摄像头向上
        if m2_angle.value < MOTOR2_MAX:
            motor.rotate(motor.motor2, STEP)
            m2_angle.value += STEP
    elif gesture == "Palm_Down": # 手掌朝下 -> 摄像头向下
        if m2_angle.value > MOTOR2_MIN:
            motor.rotate(motor.motor2, -STEP)
            m2_angle.value -= STEP

# --- 核心工作进程 ---
def camera_worker(q, m1_angle, m2_angle):
    """
    在独立进程中运行，负责摄像头捕捉、手势识别和图像处理
    """
    if not session:
        print("ONNX模型未加载，工作进程退出。")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("无法打开摄像头")
        return

    # 设置较低的摄像头分辨率和帧率
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
        
    # --- 优化: 帧处理与检测分离 ---
    frame_count = 0
    PROCESS_EVERY_N_FRAMES = 20  # 每 20 帧做一次检测

    # 缓存最近一次的检测结果
    last_pts_hand = None
    last_gesture = "No_Hand"

    while True:
        ret, frame = cap.read()
        if not ret:
            time.sleep(0.1)
            continue

        frame_count += 1
        
        # --- 1. 检测模块 (每 N 帧运行一次) ---
        if frame_count % PROCESS_EVERY_N_FRAMES == 0:
            # 复制当前帧用于处理，避免影响实时显示的帧
            processing_frame = frame.copy()
            img_height, img_width, _ = processing_frame.shape
            
            img_ = cv2.resize(processing_frame, (256, 256), interpolation=cv2.INTER_LINEAR)
            img_ = (img_.astype(np.float32) - 128.) / 256.
            img_ = np.transpose(img_, [2, 0, 1])
            img_ = np.expand_dims(img_, axis=0)

            try:
                # ONNX推理
                output = session.run(None, {ort_inputs_name: img_})
                output = np.squeeze(output)
                
                # 解析关键点并缓存
                pts_hand = {}
                for i in range(int(output.shape[0] / 2)):
                    x = output[i * 2] * img_width
                    y = output[i * 2 + 1] * img_height
                    pts_hand[str(i)] = {"x": x, "y": y}
                last_pts_hand = pts_hand
                
                # 识别手势并缓存
                gesture = recognize_gesture(last_pts_hand)
                
                # 仅在手势变化时打印日志并控制电机
                if gesture != last_gesture:
                    print(f"检测到前景手势: {gesture}, M1: {m1_angle.value}, M2: {m2_angle.value}")
                control_motor_by_gesture(gesture, m1_angle, m2_angle)
                last_gesture = gesture

            except Exception as e:
                # 如果检测失败，清除缓存，停止绘制
                last_pts_hand = None
                if last_gesture != "No_Hand":
                     print("前景中未检测到手势")
                last_gesture = "No_Hand"
        
        # --- 2. 绘制模块 (每一帧都运行) ---
        # 如果有缓存的检测结果，就在当前实时帧上绘制
        if last_pts_hand:
            # 绘制骨架
            draw_bd_handpose(frame, last_pts_hand) 
            # 绘制关键点
            for i in range(21):
                try:
                    pt = (int(last_pts_hand[str(i)]['x']), int(last_pts_hand[str(i)]['y']))
                    cv2.circle(frame, pt, 4, (255, 50, 60), -1)
                    cv2.circle(frame, pt, 2, (255, 150, 180), -1)
                except KeyError:
                    continue # 如果某个点不存在，跳过
            # 绘制手势文本
            cv2.putText(frame, last_gesture, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
        
        # --- 3. 发送模块 (每一帧都运行) ---
        _, jpeg = cv2.imencode('.jpg', frame)
        if not q.full():
            q.put(jpeg.tobytes())
        else:
            q.get() 
            q.put(jpeg.tobytes())

# --- Flask Web服务 ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>实时手势识别</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Microsoft YaHei', Arial, sans-serif; background: #f0f2f5; margin: 0; padding: 20px; text-align: center; }
        .container { max-width: 800px; margin: 20px auto; background: #fff; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 30px; }
        h2 { color: #333; }
        .cam-box { margin-top: 20px; display: inline-block; border: 2px solid #ddd; border-radius: 8px; overflow: hidden; }
        img { display: block; }
        .angle-box { margin-top: 15px; font-size: 1.1em; color: #555; }
        .angle-box span { margin: 0 15px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>实时手势识别系统</h2>
        <div class="cam-box">
            <img id="cam" src="/video_feed" width="640" height="480">
        </div>
        <div class="angle-box">
            <span>电机一 (水平): <b id="motor1">--</b>°</span>
            <span>电机二 (垂直): <b id="motor2">--</b>°</span>
        </div>
    </div>
    <script>
        function updateStatus() {
            fetch('/status').then(r => r.json()).then(data => {
                document.getElementById('motor1').innerText = data.motor1;
                document.getElementById('motor2').innerText = data.motor2;
            });
        }
        setInterval(updateStatus, 500);
        window.onload = updateStatus;
    </script>
</body>
</html>
'''

def gen_video_stream(q):
    """视频流生成器"""
    while True:
        if not q.empty():
            frame = q.get()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            time.sleep(0.01)

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/video_feed')
def video_feed():
    return Response(gen_video_stream(q_view), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/status')
def status():
    """提供电机角度的状态接口"""
    return jsonify({
        'motor1': motor1_angle.value,
        'motor2': motor2_angle.value
    })

if __name__ == '__main__':
    # 启动摄像头工作进程
    p_cam = Process(target=camera_worker, args=(q_view, motor1_angle, motor2_angle))
    p_cam.daemon = True
    p_cam.start()
    
    # 启动Web服务
    print("服务已启动，请访问 http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)

