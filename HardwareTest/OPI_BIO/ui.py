from flask import Flask, render_template_string, request, jsonify, Response
import time as systime
import cv2
from multiprocessing import Process, Queue

# 自定义模块
import motor
import temp_hum
import time
app = Flask(__name__)

# 电机最大角度
MOTOR1_MAX = 350
MOTOR2_MAX = 130
STEP = 5  # 每次移动步长

# 全局变量存储电机角度，初始为0
motor1_angle = 0
motor2_angle = 0

# 摄像头队列
q_view = Queue(maxsize=1)

# 摄像头采集进程
def camera_worker(q):
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        # 可根据需要调整分辨率
        frame = cv2.resize(frame, (320, 240))
        _, jpeg = cv2.imencode('.jpg', frame)
        if not q.full():
            q.put(jpeg.tobytes())
        systime.sleep(0.03)  # 控制帧率

# 视频流生成器
def gen_video_stream(q):
    while True:
        if not q.empty():
            frame = q.get()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            systime.sleep(0.01)

# HTML模板，按钮控制+摄像头画面
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>智能摄像头底层控制系统</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Microsoft YaHei', Arial, sans-serif; background: #f4f6f8; margin: 0; padding: 0; }
        .container { max-width: 500px; margin: 40px auto; background: #fff; border-radius: 10px; box-shadow: 0 2px 8px #ccc; padding: 30px; }
        h2 { text-align: center; color: #333; }
        .info { margin: 20px 0; font-size: 1.2em; }
        .label { color: #888; }
        .motor-control { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; }
        .motor-btns { display: flex; gap: 10px; }
        button { padding: 8px 16px; background: #0078d7; color: #fff; border: none; border-radius: 5px; font-size: 1em; cursor: pointer; }
        button:disabled { background: #ccc; cursor: not-allowed; }
        button:hover:not(:disabled) { background: #005fa3; }
        .angle { min-width: 60px; text-align: center; font-weight: bold; }
        .error { color: red; text-align: center; }
        .success { color: green; text-align: center; }
        .cam-box { text-align: center; margin: 20px 0; }
        .cam-box img { border: 1px solid #888; border-radius: 6px; }
    </style>
    <script>
        function updateData() {
            fetch('/status').then(r => r.json()).then(data => {
                document.getElementById('time').innerText = data.time;
                document.getElementById('temp').innerText = data.temp + ' ℃';
                document.getElementById('motor1').innerText = data.motor1 + '°';
                document.getElementById('motor2').innerText = data.motor2 + '°';
                // 按钮禁用逻辑
                document.getElementById('m1_dec').disabled = (data.motor1 <= -175);
                document.getElementById('m1_inc').disabled = (data.motor1 >= 175);
                document.getElementById('m2_dec').disabled = (data.motor2 <= -65);
                document.getElementById('m2_inc').disabled = (data.motor2 >= 65);
            });
        }
        setInterval(updateData, 1000);
        window.onload = updateData;
        function moveMotor(motor, direction) {
            fetch('/move', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ motor: motor, direction: direction })
            }).then(r => r.json()).then(data => {
                if(data.success){
                    updateData();
                } else {
                    alert(data.error);
                }
            });
        }
    </script>
</head>
<body>
    <div class="container">
        <h2>智能摄像头底层控制系统</h2>
        <div class="info"><span class="label">当前时间：</span><span id="time">--:--:--</span></div>
        <div class="info"><span class="label">机身内部温度：</span><span id="temp">-- ℃</span></div>
        <div class="cam-box">
            <span class="label">摄像头画面：</span><br>
            <img id="cam" src="/video_feed" width="320" height="240">
        </div>
        <div class="motor-control">
            <span class="label">电机一：</span>
            <div class="motor-btns">
                <button id="m1_dec" onclick="moveMotor(1, -1)">-</button>
                <span class="angle" id="motor1">--°</span>
                <button id="m1_inc" onclick="moveMotor(1, 1)">+</button>
            </div>
            <span class="label">范围：-175°~175°</span>
        </div>
        <div class="motor-control">
            <span class="label">电机二：</span>
            <div class="motor-btns">
                <button id="m2_dec" onclick="moveMotor(2, -1)">-</button>
                <span class="angle" id="motor2">--°</span>
                <button id="m2_inc" onclick="moveMotor(2, 1)">+</button>
            </div>
            <span class="label">范围：-65°~65°</span>
        </div>
        {% if error %}<div class="error">{{ error }}</div>{% endif %}
        {% if success %}<div class="success">{{ success }}</div>{% endif %}
    </div>
</body>
</html>
'''

@app.route('/status')
def status():
    try:
        h, m, s = time.get_time()
    except Exception:
        t = systime.localtime()
        h, m, s = t.tm_hour, t.tm_min, t.tm_sec
    now = f"{h:02d}:{m:02d}:{s:02d}"
    temp_raw = temp_hum.get_temp() if hasattr(temp_hum, 'get_temp') else None
    temp = round(temp_raw / 10, 1) if temp_raw is not None else '--'
    return jsonify({
        'time': now,
        'temp': temp,
        'motor1': motor1_angle,
        'motor2': motor2_angle
    })

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/move', methods=['POST'])
def move():
    global motor1_angle, motor2_angle
    data = request.get_json()
    motor_id = data.get('motor')
    direction = data.get('direction')  # -1 或 1
    if motor_id == 1:
        new_angle = motor1_angle + direction * STEP
        if 0 <= new_angle <= MOTOR1_MAX:
            motor.rotate(motor.motor1, direction * STEP)
            motor1_angle = new_angle
            return jsonify(success=True)
        else:
            return jsonify(success=False, error='电机一已达极限')
    elif motor_id == 2:
        new_angle = motor2_angle + direction * STEP
        if 0 <= new_angle <= MOTOR2_MAX:
            motor.rotate(motor.motor2, direction * STEP)
            motor2_angle = new_angle
            return jsonify(success=True)
        else:
            return jsonify(success=False, error='电机二已达极限')
    else:
        return jsonify(success=False, error='参数错误')

@app.route('/video_feed')
def video_feed():
    return Response(gen_video_stream(q_view), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    p_cam = Process(target=camera_worker, args=(q_view,))
    p_cam.daemon = True
    p_cam.start()
    app.run(host='0.0.0.0', port=5000, debug=False)