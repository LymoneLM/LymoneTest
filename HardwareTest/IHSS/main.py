import cv2
import numpy as np
import time
import re
import datetime
from flask import Flask, render_template_string, Response, request, jsonify
from multiprocessing import Process, Lock, Value, RawArray
from ctypes import c_char_p, c_bool
import utils.motor as motor
import utils.temp_hum as temp_hum
import utils.time as time_utils
import utils.speaker as speaker
from face_detect_rec import FaceDetectRec, faceDetecImgDis
import sqlite3
import json
import os
from danger_rec import DangerDetectRec
import utils.baidu as baidu
import utils.deepseek as deepseek
import pvporcupine
from pvrecorder import PvRecorder
import config.key as key
import wave

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

frame_dims = RawArray('i', [0, 0, 0])  # [H, W, C]
frame_buffer = RawArray('B', CAM_HEIGHT * CAM_WIDTH * 3)
shared_direction = Value(c_char_p, b"center")
enable_face_detection = Value(c_bool, False)
enable_face_tracking = Value(c_bool, False)
enable_face_overlay = Value(c_bool, True)
motor1_angle = Value('i', 0)
motor2_angle = Value('i', 0)
last_motor_activity = Value('d', time.time())
motor_sleep_status = Value(c_bool, False)
last_face_toggle_time = Value('d', 0.0)  # 新增：记录上次切换人脸追踪的时间
volume_value = Value('d', 0.05)  # 全局音量（0.0~1.0）
enable_danger_detection = Value(c_bool, False)
last_danger_alarm_time = Value('d', 0.0)  # 火焰报警防抖
# ----------------- 全局人脸检测器实例 -----------------
face_detector = None
# ----------------- 全局危险物检测器实例 -----------------
danger_detector = None
danger_last_result = {'boxes': [], 'labels': [], 'confs': []}
# ----------------- SQLite数据库初始化 -----------------
DB_PATH = 'events.db'
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS event_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                detail TEXT,
                confidence REAL
            )
        ''')
        conn.commit()
        conn.close()

init_db()

# 事件记录插入函数

def log_event(event_type, detail=None, confidence=None):
    ts = datetime.datetime.now().isoformat()
    detail_str = json.dumps(detail, ensure_ascii=False) if detail is not None else None
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        'INSERT INTO event_log (timestamp, event_type, detail, confidence) VALUES (?, ?, ?, ?)',
        (ts, event_type, detail_str, confidence)
    )
    conn.commit()
    conn.close()
    print(f"[EVENT LOG] {ts} | {event_type} | detail={detail_str} | confidence={confidence}")

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
def recognition_process(frame_lock, frame_buffer, frame_dims, shared_direction):
    face_detector = FaceDetectRec()
    frame_count = 0
    print("识别进程启动...")
    # 人脸消抖队列和状态
    from collections import deque
    face_count_queue = deque(maxlen=5)
    confirmed_face_count = 0
    last_confirmed_face_count = 0
    while True:
        time.sleep(0.05)
        frame_count += 1
        with frame_lock:
            if frame_dims[0] == 0:
                continue
            frame_buffer_np = np.frombuffer(frame_buffer, dtype=np.uint8).reshape(frame_dims[:])
            frame = frame_buffer_np.copy()
        frame = cv2.flip(frame, 1)
        # 人脸检测和跟踪每5帧
        if (enable_face_detection.value or enable_face_tracking.value) and frame_count % 5 == 0:
            predictions = face_detector.inference(frame)
            bboxes = predictions[0] if predictions and predictions[0] is not None else []
            face_count = len(bboxes)
            face_count_queue.append(face_count)
            # 消抖：连续5帧人数一致且与上次确认人数不同
            if len(face_count_queue) == face_count_queue.maxlen and all(x == face_count_queue[0] for x in face_count_queue):
                confirmed_face_count = face_count_queue[0]
                if confirmed_face_count != last_confirmed_face_count:
                    # 事件判定
                    if last_confirmed_face_count == 0 and confirmed_face_count > 0:
                        # 场景来人
                        log_event('scene_enter', detail={'count': confirmed_face_count})
                    elif last_confirmed_face_count > 0 and confirmed_face_count == 0:
                        # 场景无人
                        log_event('scene_leave')
                    elif last_confirmed_face_count > 0 and confirmed_face_count > 0:
                        diff = confirmed_face_count - last_confirmed_face_count
                        if diff > 0:
                            log_event('person_enter', detail={'count': confirmed_face_count, 'change': diff})
                        elif diff < 0:
                            log_event('person_leave', detail={'count': confirmed_face_count, 'change': diff})
                    last_confirmed_face_count = confirmed_face_count
            # 人脸跟踪电机控制逻辑
            if enable_face_tracking.value and face_count > 0:
                bbox = bboxes[0]
                face_cx = int((bbox[0] + bbox[2]) / 2)
                face_cy = int((bbox[1] + bbox[3]) / 2)
                cx, cy = CAM_WIDTH // 2, CAM_HEIGHT // 2
                dead_zone_w = 80
                dead_zone_h = 80
                dx = face_cx - cx
                dy = face_cy - cy
                if abs(dx) > dead_zone_w // 2:
                    step_x = int(np.clip(abs(dx) / (CAM_WIDTH // 8), 1, 5)) * MOTOR_STEP
                    if dx > 0 and motor1_angle.value < MOTOR1_MAX:
                        motor.rotate(motor.motor1, step_x)
                        motor1_angle.value += step_x
                    elif dx < 0 and motor1_angle.value > MOTOR1_MIN:
                        motor.rotate(motor.motor1, -step_x)
                        motor1_angle.value -= step_x
                if abs(dy) > dead_zone_h // 2:
                    step_y = int(np.clip(abs(dy) / (CAM_HEIGHT // 8), 1, 5)) * MOTOR_STEP
                    if dy > 0 and motor2_angle.value > MOTOR2_MIN:
                        motor.rotate(motor.motor2, -step_y)
                        motor2_angle.value -= step_y
                    elif dy < 0 and motor2_angle.value < MOTOR2_MAX:
                        motor.rotate(motor.motor2, step_y)
                        motor2_angle.value += step_y
                last_motor_activity.value = time.time()
                if motor_sleep_status.value:
                    motor_sleep_status.value = False
        # 电机休眠
        if time.time() - last_motor_activity.value > 30 and not motor_sleep_status.value:
            motor.sleep_motor()
            motor_sleep_status.value = True

# ----------------- 危险物检测进程 -----------------
def danger_recognition_process(frame_lock, frame_buffer, frame_dims):
    danger_detector = DangerDetectRec()
    frame_count = 0
    print("危险物检测进程启动...")
    last_fire_alarm = 0
    global danger_last_result
    while True:
        time.sleep(0.05)
        frame_count += 1
        if not enable_danger_detection.value:
            continue
        if frame_count % 5 != 0:
            continue
        with frame_lock:
            if frame_dims[0] == 0:
                continue
            frame_buffer_np = np.frombuffer(frame_buffer, dtype=np.uint8).reshape(frame_dims[:])
            frame = frame_buffer_np.copy()
        frame = cv2.flip(frame, 1)
        boxes = danger_detector.inference(frame, conf_thres=0.3)
        out_boxes = [b['bbox'] for b in boxes]
        out_labels = [b['label'] for b in boxes]
        out_confs = [b['conf'] for b in boxes]
        danger_last_result = {'boxes': out_boxes, 'labels': out_labels, 'confs': out_confs}
        for box in boxes:
            label = box['label']
            conf = box['conf']
            if conf > 0.3:
                log_event('dangerous_object', detail={'label': label, 'confidence': conf})
            if label == 'fire' and conf > 0.8:
                now = time.time()
                if now - last_fire_alarm > 10:  # 10秒防抖
                    log_event('fire_alarm', detail={'confidence': conf})
                    try:
                        from utils import speaker
                        speaker.play_wav_file_queued('assets/alarm.wav', volume=volume_value.value)
                    except Exception as e:
                        print(f"火焰报警音频播放失败: {e}")
                    last_fire_alarm = now

# ----------------- 语音指令进程 -----------------
def voice_command_process():
    access_key = key.picovoice_access_key
    keywords = ["哨兵"]
    porcupine = pvporcupine.create(
        access_key=access_key,
        keyword_paths=['models/porcupine/哨兵_zh_raspberry-pi_v3_0_0.ppn'],
        model_path='models/porcupine/porcupine_params_zh.pv'
    )
    recoder = PvRecorder(device_index=11, frame_length=porcupine.frame_length)
    print("唤醒词检测进程启动... (唤醒词: 哨兵)")
    try:
        recoder.start()
        while True:
            keyword_index = porcupine.process(recoder.read())
            if keyword_index >= 0:
                print(f"[唤醒] 检测到唤醒词: {keywords[keyword_index]}")
                # 播放“我在”提示音
                speaker.play_wav_file_queued('assets/iamhere.wav', volume=volume_value.value)
                # 用PvRecorder录制10秒音频
                samplerate = 16000
                frame_length = porcupine.frame_length
                total_frames = samplerate * 5 // frame_length
                print("[录音] 开始录音10秒...")
                audio_frames = []
                for _ in range(total_frames):
                    frame = recoder.read()
                    audio_frames.append(frame)
                import numpy as np
                audio_np = np.concatenate(audio_frames).astype('float32') / 32768.0  # PvRecorder输出int16
                # 保存为wav
                wav_path = 'voice_cmd.wav'
                import wave
                with wave.open(wav_path, 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(samplerate)
                    audio_int16 = (audio_np * 32767).astype('int16')
                    wf.writeframes(audio_int16.tobytes())
                print(f"[录音] 已保存到 {wav_path}")
                # 播放“请稍候”提示音
                speaker.play_wav_file_queued('assets/please_wait.wav', volume=volume_value.value)
                # 语音转文字
                text = baidu.audio2text(wav_path, format='wav', rate=16000)
                if not text:
                    print("[语音识别] 识别失败")
                    continue
                print(f"[语音识别] 识别结果: {text}")
                # DeepSeek与命令处理
                now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                prompt = f"""
                你是一个智能安防摄像头的语音助手。请根据用户的语音指令，严格返回如下格式的JSON：
                {{
                  "cmd_type": 0/1/2, // 0:无效命令 1:控制命令 2:查找命令
                  "cmd_content": 控制命令内容（0:旋转 1:模式切换 2:控制人脸追踪 3:控制唤醒 4:控制安全检测 5:控制安全声音检测），
                  "cmd_detail": {{
                    "rotate": [水平步数, 垂直步数], // 仅旋转命令时填写，根据用户的语气控制步数，两个都控制在[-5,5]区间
                    "switch": true/false, // 控制开关命令时填写
                    "mode": 0/1/2/3 // 模式切换命令时填写 0普通 1静音 2哨兵 3隐私
                  }},
                  "search_time": ["开始时间", "结束时间"], // 如果是查找命令时填写，格式如"2024-05-01 00:00:00"根据用户命令确定需要的时间
                  "search_type": 0/1/2, // 0安全声音 1人类活动 2危险物品
                  "search_extra": [可选附加内容数组]
                }}
                注意：
                - 现在时间是{now_str}
                - 安全识别类的名字有：fire, gun, knife。
                - 人类活动类的名字有：scene_enter, scene_leave, person_enter, person_leave。
                - search_extra如果用户有指定查找内容，请严格填写上述类名。
                - 只返回JSON，不要有多余解释！！这是关键！！确保回复只有JSON并且格式正确！！
                - 你需要察觉出用户隐含的含义，进行一定的模糊理解，比如询问可能是查询
                - 如果无法理解指令，cmd_type设为0。
                - 控制命令和查找命令的内容必须严格按上述字段填写。
                - 查找命令必须填写时间范围。
                """
                ai_reply = deepseek.chat_with_ai(text, system_prompt=prompt)
                if not ai_reply:
                    print("[DeepSeek] 无AI回复")
                    continue
                print(f"[DeepSeek] 原始回复: {ai_reply}")
                try:
                    cmd = parse_ai_json_reply(ai_reply)
                except Exception as e:
                    print(f"[DeepSeek] JSON解析失败: {e}")
                    continue
                if cmd.get('cmd_type') == 1:
                    cc = cmd.get('cmd_content')
                    detail = cmd.get('cmd_detail', {})
                    if cc == 0 and 'rotate' in detail:
                        dx, dy = detail['rotate']
                        global motor1_angle, motor2_angle
                        # 按步移动，每步MOTOR_STEP，正负方向
                        steps_x = int(np.clip(dx, -5, 5))
                        steps_y = int(np.clip(dy, -5, 5))
                        moved = False
                        if steps_x != 0:
                            for _ in range(abs(steps_x)):
                                if steps_x > 0 and motor1_angle.value < MOTOR1_MAX:
                                    motor.rotate(motor.motor1, MOTOR_STEP)
                                    motor1_angle.value += MOTOR_STEP
                                elif steps_x < 0 and motor1_angle.value > MOTOR1_MIN:
                                    motor.rotate(motor.motor1, -MOTOR_STEP)
                                    motor1_angle.value -= MOTOR_STEP
                                moved = True
                        if steps_y != 0:
                            for _ in range(abs(steps_y)):
                                if steps_y > 0 and motor2_angle.value < MOTOR2_MAX:
                                    motor.rotate(motor.motor2, MOTOR_STEP)
                                    motor2_angle.value += MOTOR_STEP
                                elif steps_y < 0 and motor2_angle.value > MOTOR2_MIN:
                                    motor.rotate(motor.motor2, -MOTOR_STEP)
                                    motor2_angle.value -= MOTOR_STEP
                                moved = True
                        print(f"[控制] 旋转: dx={dx}, dy={dy}")
                        if moved:
                            speaker.play_wav_file_queued('assets/rotated.wav', volume=volume_value.value)
                    elif cc == 1 and 'mode' in detail:
                        mode = detail['mode']
                        if mode == 0:
                            enable_face_tracking.value = True
                            enable_danger_detection.value = True
                            speaker.play_wav_file_queued('assets/normal_mode.wav', volume=volume_value.value)
                        elif mode == 1:
                            enable_face_tracking.value = True
                            enable_danger_detection.value = True
                            speaker.play_wav_file_queued('assets/mute_mode.wav', volume=volume_value.value)
                        elif mode == 2:
                            enable_face_tracking.value = True
                            enable_danger_detection.value = True
                            speaker.play_wav_file_queued('assets/sentry_mode.wav', volume=volume_value.value)
                        elif mode == 3:
                            motor.rotate(motor.motor1, 175 - motor1_angle.value)
                            motor1_angle.value = 175
                            motor.rotate(motor.motor2, -65 - motor2_angle.value)
                            motor2_angle.value = -65
                            enable_face_tracking.value = False
                            enable_danger_detection.value = False
                            speaker.play_wav_file_queued('assets/privacy_mode.wav', volume=volume_value.value)
                        print(f"[控制] 模式切换: {mode}")
                    elif cc == 2 and 'switch' in detail:
                        enable_face_tracking.value = bool(detail['switch'])
                        if detail['switch']:
                            speaker.play_wav_file_queued('assets/face_tracking.wav', volume=volume_value.value)
                            speaker.play_wav_file_queued('assets/on.wav', volume=volume_value.value)
                        else:
                            speaker.play_wav_file_queued('assets/face_tracking.wav', volume=volume_value.value)
                            speaker.play_wav_file_queued('assets/off.wav', volume=volume_value.value)
                        print(f"[控制] 人脸追踪开关: {detail['switch']}")
                    elif cc == 3 and 'switch' in detail:
                        # 唤醒功能开关
                        if detail['switch']:
                            speaker.play_wav_file_queued('assets/voice_awake.wav', volume=volume_value.value)
                            speaker.play_wav_file_queued('assets/on.wav', volume=volume_value.value)
                        else:
                            speaker.play_wav_file_queued('assets/voice_awake.wav', volume=volume_value.value)
                            speaker.play_wav_file_queued('assets/off.wav', volume=volume_value.value)
                        print(f"[控制] 唤醒功能开关: {detail['switch']}")
                    elif cc == 4 and 'switch' in detail:
                        enable_danger_detection.value = bool(detail['switch'])
                        if detail['switch']:
                            speaker.play_wav_file_queued('assets/danger_detection.wav', volume=volume_value.value)
                            speaker.play_wav_file_queued('assets/on.wav', volume=volume_value.value)
                        else:
                            speaker.play_wav_file_queued('assets/danger_detection.wav', volume=volume_value.value)
                            speaker.play_wav_file_queued('assets/off.wav', volume=volume_value.value)
                        print(f"[控制] 安全检测开关: {detail['switch']}")
                elif cmd.get('cmd_type') == 2:
                    st, et = cmd.get('search_time', [None, None])
                    s_type = cmd.get('search_type')
                    s_extra = cmd.get('search_extra', [])
                    q = "SELECT timestamp, event_type, detail, confidence FROM event_log WHERE timestamp BETWEEN ? AND ?"
                    params = [st, et]
                    if s_type == 0:
                        q += " AND event_type LIKE '%sound%'"
                    elif s_type == 1:
                        q += " AND event_type LIKE '%scene%'"
                    elif s_type == 2:
                        q += " AND event_type LIKE '%danger%'"
                    conn = sqlite3.connect(DB_PATH)
                    c = conn.cursor()
                    c.execute(q, params)
                    rows = c.fetchall()
                    conn.close()
                    # 严格按时间戳筛选
                    try:
                        def parse_iso(ts):
                            try:
                                return datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%f')
                            except Exception:
                                return datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S')
                        st_dt = parse_iso(st)
                        et_dt = parse_iso(et)
                        filtered_rows = []
                        for row in rows:
                            ts = row[0]
                            try:
                                ts_dt = parse_iso(ts)
                                if st_dt <= ts_dt <= et_dt:
                                    filtered_rows.append(row)
                            except Exception:
                                continue
                        rows = filtered_rows
                    except Exception as e:
                        print(f"[时间筛选异常] {e}")
                    if s_extra:
                        filtered = []
                        for row in rows:
                            if any(x in row[2] for x in s_extra):
                                filtered.append(row)
                        rows = filtered
                    data_str = '\n'.join([str(r) for r in rows])
                    explain_prompt = (f"你是安防专家，请用最简短的话总结分析如下事件数据，如果有必要可以建议用户重点关注哪些时间段录像以确保安全：\n{data_str}"
                                      f"\n全部信息已经完全插入上文，如果没有信息表示没有任何安全事件。")
                    # 只要求返回自然语言分析，不要JSON
                    explain = deepseek.chat_with_ai(explain_prompt, system_prompt="你是安防专家，请用简洁自然语言总结分析，只要自然语言！")
                    print(f"[查找分析] {explain}")
                    # TTS转语音并播放
                    tts_wav = 'explain_reply.wav'
                    if baidu.text2audio(explain, output_file=tts_wav):
                        try:
                            speaker.play_wav_file_queued(tts_wav, volume=volume_value.value)
                        except Exception as e:
                            print(f"[TTS播放失败] {e}")
                else:
                    print("[AI] 无效命令，忽略。")
                    speaker.play_wav_file_queued('assets/noidea.wav', volume=volume_value.value)
                recoder.start()  # 录音和处理完毕后恢复唤醒词检测
    except KeyboardInterrupt:
        recoder.stop()
        recoder.delete()

# ----------------- 工具函数：解析AI JSON回复 -----------------
def parse_ai_json_reply(ai_reply):
    """
    从AI回复中提取并解析第一个合法JSON对象。
    支持去除markdown代码块、前后空白、多余内容。
    """
    json_str = ai_reply.strip()
    if json_str.startswith('```json'):
        json_str = json_str[7:]
    if json_str.startswith('```'):
        json_str = json_str[3:]
    if json_str.endswith('```'):
        json_str = json_str[:-3]
    try:
        return json.loads(json_str)
    except Exception:
        match = re.search(r'\{[\s\S]*\}', ai_reply)
        if match:
            return json.loads(match.group(0))
        else:
            raise ValueError('无法从AI回复中提取合法JSON')

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
            max-width: 1400px; 
            margin: auto; 
            display: grid;
            grid-template-columns: 250px 1fr 300px;
            gap: 20px;
            align-items: stretch;
            height: 80vh;
        }
        .panel {
            background: #fff;
            border-radius: 10px;
            box-shadow: 0 2px 8px #ccc;
            padding: 20px;
            height: 100%;
            display: flex;
            flex-direction: column;
            box-sizing: border-box;
        }
        .left-panel, .right-panel {
            height: 100%;
        }
        .main-content {
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }
        .cam-box {
            margin-bottom: 20px;
            flex: 1 1 auto;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }
        .cam-box img {
            width: 100%;
            height: auto;
            max-height: 100%;
            border-radius: 6px;
            object-fit: contain;
        }
        .cam-box canvas {
            position: absolute;
            left: 0;
            top: 0;
            pointer-events: none;
            border-radius: 6px;
            width: 100%;
            height: 100%;
        }

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
                    document.getElementById('face_detection').checked = data.face_detection;
                    document.getElementById('face_tracking').checked = data.face_tracking;
                    document.getElementById('face_overlay').checked = data.face_overlay;
                    document.getElementById('volume_slider').value = Math.round(data.volume * 100);
                    document.getElementById('volume_value').innerText = Math.round(data.volume * 100);
                    document.getElementById('danger_detection').checked = data.danger_detection;
                    // 更新按钮状态
                    document.getElementById('m1_left').disabled = (data.motor1 <= -175);
                    document.getElementById('m1_right').disabled = (data.motor1 >= 175);
                    document.getElementById('m2_down').disabled = (data.motor2 <= -65);
                    document.getElementById('m2_up').disabled = (data.motor2 >= 65);
                });
        }

        function drawFaceBoxes(boxes) {
            const img = document.getElementById('cam');
            const canvas = document.getElementById('face_canvas');
            if (!img || !canvas) return;
            if (!img.complete || img.naturalWidth === 0) {
                setTimeout(() => drawFaceBoxes(boxes), 100);
                return;
            }
            const containerRect = canvas.parentElement.getBoundingClientRect();
            canvas.width = containerRect.width;
            canvas.height = containerRect.height;
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const imgW = 640, imgH = 480;
            const imgAspectRatio = imgW / imgH;
            const containerAspectRatio = containerRect.width / containerRect.height;
            let displayWidth, displayHeight, offsetX, offsetY;
            if (imgAspectRatio > containerAspectRatio) {
                displayWidth = containerRect.width;
                displayHeight = containerRect.width / imgAspectRatio;
                offsetX = 0;
                offsetY = (containerRect.height - displayHeight) / 2;
            } else {
                displayHeight = containerRect.height;
                displayWidth = containerRect.height * imgAspectRatio;
                offsetX = (containerRect.width - displayWidth) / 2;
                offsetY = 0;
            }
            const scaleX = displayWidth / imgW;
            const scaleY = displayHeight / imgH;
            boxes.forEach(box => {
                const [x1, y1, x2, y2] = box;
                const drawX = offsetX + x1 * scaleX;
                const drawY = offsetY + y1 * scaleY;
                const drawWidth = (x2 - x1) * scaleX;
                const drawHeight = (y2 - y1) * scaleY;
                ctx.strokeStyle = '#00ff00';
                ctx.lineWidth = 2;
                ctx.strokeRect(drawX, drawY, drawWidth, drawHeight);
                ctx.fillStyle = '#00ff00';
                ctx.font = '14px Arial';
                ctx.fillText('Face', drawX, drawY - 5);
            });
        }

        function updateFaceOverlay() {
            if (!document.getElementById('face_overlay').checked) {
                const canvas = document.getElementById('face_canvas');
                if (canvas) {
                    const ctx = canvas.getContext('2d');
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                }
                // 更新人脸数量显示
                document.getElementById('face_count').innerText = '0';
                return;
            }
            
            fetch('/face_boxes')
                .then(r => r.json())
                .then(data => {
                    if (data.boxes && data.boxes.length > 0) {
                        drawFaceBoxes(data.boxes);
                        // 更新人脸数量显示
                        document.getElementById('face_count').innerText = data.boxes.length;
                        // 调试信息
                        console.log(`Detected ${data.boxes.length} faces:`, data.boxes);
                    } else {
                        // 清除canvas
                        const canvas = document.getElementById('face_canvas');
                        if (canvas) {
                            const ctx = canvas.getContext('2d');
                            ctx.clearRect(0, 0, canvas.width, canvas.height);
                        }
                        // 更新人脸数量显示
                        document.getElementById('face_count').innerText = '0';
                    }
                })
                .catch(err => {
                    console.error('Failed to fetch face boxes:', err);
                    document.getElementById('face_count').innerText = '0';
                });
        }

        function drawDangerBoxes(boxes, labels, confs) {
            const img = document.getElementById('cam');
            const canvas = document.getElementById('danger_canvas');
            if (!img || !canvas) return;
            if (!img.complete || img.naturalWidth === 0) {
                setTimeout(() => drawDangerBoxes(boxes, labels, confs), 100);
                return;
            }
            const containerRect = canvas.parentElement.getBoundingClientRect();
            canvas.width = containerRect.width;
            canvas.height = containerRect.height;
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const imgW = 640, imgH = 480;
            const imgAspectRatio = imgW / imgH;
            const containerAspectRatio = containerRect.width / containerRect.height;
            let displayWidth, displayHeight, offsetX, offsetY;
            if (imgAspectRatio > containerAspectRatio) {
                displayWidth = containerRect.width;
                displayHeight = containerRect.width / imgAspectRatio;
                offsetX = 0;
                offsetY = (containerRect.height - displayHeight) / 2;
            } else {
                displayHeight = containerRect.height;
                displayWidth = containerRect.height * imgAspectRatio;
                offsetX = (containerRect.width - displayWidth) / 2;
                offsetY = 0;
            }
            const scaleX = displayWidth / imgW;
            const scaleY = displayHeight / imgH;
            for (let i = 0; i < boxes.length; i++) {
                const [x1, y1, x2, y2] = boxes[i];
                const drawX = offsetX + x1 * scaleX;
                const drawY = offsetY + y1 * scaleY;
                const drawWidth = (x2 - x1) * scaleX;
                const drawHeight = (y2 - y1) * scaleY;
                ctx.strokeStyle = '#ff0000';
                ctx.lineWidth = 2;
                ctx.strokeRect(drawX, drawY, drawWidth, drawHeight);
                ctx.fillStyle = '#ff0000';
                ctx.font = '14px Arial';
                ctx.fillText(labels[i] + ':' + confs[i].toFixed(2), drawX, drawY - 5);
            }
        }

        function updateDangerOverlay() {
            if (!document.getElementById('danger_detection').checked) {
                const canvas = document.getElementById('danger_canvas');
                if (canvas) {
                    const ctx = canvas.getContext('2d');
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                }
                document.getElementById('danger_count').innerText = '0';
                return;
            }
            fetch('/danger_boxes')
                .then(r => r.json())
                .then(data => {
                    if (data.boxes && data.boxes.length > 0) {
                        drawDangerBoxes(data.boxes, data.labels, data.confs);
                        document.getElementById('danger_count').innerText = data.boxes.length;
                    } else {
                        const canvas = document.getElementById('danger_canvas');
                        if (canvas) {
                            const ctx = canvas.getContext('2d');
                            ctx.clearRect(0, 0, canvas.width, canvas.height);
                        }
                        document.getElementById('danger_count').innerText = '0';
                    }
                })
                .catch(err => {
                    document.getElementById('danger_count').innerText = '0';
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

        function setVolume(val) {
            fetch('/set_volume', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({volume: val/100})
            }).then(r => r.json()).then(updateStatus);
            document.getElementById('volume_value').innerText = val;
        }

        window.onload = function() {
            updateStatus();
            setInterval(updateStatus, 500);
            setInterval(updateFaceOverlay, 500);
            setInterval(updateDangerOverlay, 500);
            // 监听窗口大小变化，重新绘制人脸框
            window.addEventListener('resize', function() {
                if (document.getElementById('face_overlay').checked) {
                    updateFaceOverlay();
                }
                if (document.getElementById('danger_detection').checked) {
                    updateDangerOverlay();
                }
            });
        };
    </script>
</head>
<body>
    <div class="container">
        <div class="panel left-panel">
            <div class="control-group">
                <h3>功能控制</h3>
                <div class="switch-container">
                    <span class="switch-label">人脸检测</span>
                    <label class="switch">
                        <input type="checkbox" id="face_detection" onchange="toggleControl('face_detection')">
                        <span class="slider"></span>
                    </label>
                </div>
                <div class="switch-container">
                    <span class="switch-label">人脸跟踪</span>
                    <label class="switch">
                        <input type="checkbox" id="face_tracking" onchange="toggleControl('face_tracking')">
                        <span class="slider"></span>
                    </label>
                </div>
                <div class="switch-container">
                    <span class="switch-label">人脸绘制</span>
                    <label class="switch">
                        <input type="checkbox" id="face_overlay" onchange="toggleControl('face_overlay')">
                        <span class="slider"></span>
                    </label>
                </div>
                <div class="switch-container">
                    <span class="switch-label">危险物检测</span>
                    <label class="switch">
                        <input type="checkbox" id="danger_detection" onchange="toggleControl('danger_detection')">
                        <span class="slider"></span>
                    </label>
                </div>
            </div>
            <div class="control-group">
                <h3>音量调节</h3>
                <div class="switch-container">
                    <span class="switch-label">音量</span>
                    <input type="range" id="volume_slider" min="0" max="100" value="100" style="flex:2" oninput="setVolume(this.value)">
                    <span id="volume_value">100</span>
                </div>
            </div>
        </div>
        <div class="panel main-content">
            <h2>哨兵Sentry控制平台</h2>
            <div class="cam-box">
                <img id="cam" src="/video_feed" alt="摄像头画面">
                <canvas id="face_canvas" style="position:absolute;left:0;top:0;pointer-events:none;border-radius:6px;width:100%;height:100%;z-index:10;"></canvas>
                <canvas id="danger_canvas" style="position:absolute;left:0;top:0;pointer-events:none;border-radius:6px;width:100%;height:100%;z-index:20;"></canvas>
            </div>
        </div>
        <div class="panel right-panel">
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
                <div class="status-item">
                    <span class="status-label">检测到人脸:</span>
                    <span class="status-value" id="face_count">0</span>
                </div>
                <div class="status-item">
                    <span class="status-label">危险物体:</span>
                    <span class="status-value" id="danger_count">0</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

def gen_video_stream():
    while True:
        time.sleep(1/30)
        with frame_lock:
            if frame_dims[0] == 0:
                continue
            frame_buffer_np = np.frombuffer(frame_buffer, dtype=np.uint8).reshape(frame_dims[:])
            frame = frame_buffer_np.copy()
        frame = cv2.flip(frame, 1)
        # 只推送原始图像，不再绘制人脸框
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
        'face_detection': enable_face_detection.value,
        'face_tracking': enable_face_tracking.value,
        'face_overlay': enable_face_overlay.value,
        'volume': volume_value.value,
        'danger_detection': enable_danger_detection.value
    })

@app.route('/toggle_control', methods=['POST'])
def toggle_control():
    data = request.get_json()
    control_type = data.get('type')
    if control_type == 'face_detection':
        enable_face_detection.value = not enable_face_detection.value
    elif control_type == 'face_tracking':
        enable_face_tracking.value = not enable_face_tracking.value
    elif control_type == 'face_overlay':
        enable_face_overlay.value = not enable_face_overlay.value
    elif control_type == 'danger_detection':
        enable_danger_detection.value = not enable_danger_detection.value
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

@app.route('/set_volume', methods=['POST'])
def set_volume():
    data = request.get_json()
    v = float(data.get('volume', 1.0))
    v = min(max(v, 0.0), 1.0)
    volume_value.value = v
    return jsonify({'success': True, 'volume': v})

# 新增：人脸检测结果API
@app.route('/face_boxes')
def face_boxes():
    global face_detector
    try:
        with frame_lock:
            if frame_dims[0] == 0:
                return jsonify({'boxes': [], 'types': []})
            frame_buffer_np = np.frombuffer(frame_buffer, dtype=np.uint8).reshape(frame_dims[:])
            frame = frame_buffer_np.copy()
        
        frame = cv2.flip(frame, 1)
        
        if not (enable_face_detection.value or enable_face_tracking.value):
            return jsonify({'boxes': [], 'types': []})
        
        # 延迟初始化人脸检测器
        if face_detector is None:
            face_detector = FaceDetectRec()
        
        predictions = face_detector.inference(frame)
        bboxes = predictions[0] if predictions and predictions[0] is not None else []
        
        # boxes: [ [x1, y1, x2, y2], ... ]
        boxes = []
        for b in bboxes:
            try:
                x1, y1, x2, y2 = int(b[0]), int(b[1]), int(b[2]), int(b[3])
                # 确保坐标在有效范围内
                if 0 <= x1 < x2 <= CAM_WIDTH and 0 <= y1 < y2 <= CAM_HEIGHT:
                    boxes.append([x1, y1, x2, y2])
            except (ValueError, IndexError) as e:
                print(f"Invalid bbox format: {b}, error: {e}")
                continue
        
        # types: 目前全部为"face"，如有多类型可扩展
        types = ["face"] * len(boxes)
        
        return jsonify({'boxes': boxes, 'types': types})
    except Exception as e:
        print(f"Error in face_boxes API: {e}")
        return jsonify({'boxes': [], 'types': [], 'error': str(e)})

# 新增：危险物检测结果API
@app.route('/danger_boxes')
def danger_boxes():
    global danger_detector
    global danger_last_result
    try:
        with frame_lock:
            if frame_dims[0] == 0:
                return jsonify(danger_last_result)
            frame_buffer_np = np.frombuffer(frame_buffer, dtype=np.uint8).reshape(frame_dims[:])
            frame = frame_buffer_np.copy()
        frame = cv2.flip(frame, 1)
        if not enable_danger_detection.value:
            return jsonify(danger_last_result)
        if danger_detector is None:
            danger_detector = DangerDetectRec()
        # 这里不做实时检测，直接返回缓存结果
        return jsonify(danger_last_result)
    except Exception as e:
        print(f"Error in danger_boxes API: {e}")
        return jsonify({'boxes': [], 'labels': [], 'confs': [], 'error': str(e)})

if __name__ == '__main__':
    # 预初始化人脸检测器
    print("正在初始化人脸检测模型...")
    face_detector = FaceDetectRec()
    print("人脸检测模型初始化完成")
    print("正在初始化危险物检测模型...")
    danger_detector = DangerDetectRec()
    print("危险物检测模型初始化完成")
    
    p_camera = Process(target=camera_process, args=(frame_lock, frame_buffer, frame_dims))
    p_recognition = Process(target=recognition_process, args=(frame_lock, frame_buffer, frame_dims, shared_direction))
    p_danger = Process(target=danger_recognition_process, args=(frame_lock, frame_buffer, frame_dims))
    p_voice = Process(target=voice_command_process)
    p_camera.daemon = True
    p_recognition.daemon = True
    p_danger.daemon = True
    p_voice.daemon = True
    p_camera.start()
    p_recognition.start()
    p_danger.start()
    p_voice.start()
    print("Web服务已启动，请访问 http://<设备IP>:8081")
    try:
        app.run(host='0.0.0.0', port=8081, debug=False)
    except KeyboardInterrupt:
        print("\n正在关闭所有进程...")
    finally:
        p_camera.terminate()
        p_recognition.terminate()
        p_danger.terminate()
        p_voice.terminate()
        p_camera.join()
        p_recognition.join()
        p_danger.join()
        p_voice.join()
        print("所有进程已关闭。")
