import cv2
import mediapipe as mp
import motor
import time

# 初始化 Mediapipe 手部模块
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# 打开摄像头
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 电机控制参数
MOTOR_STEP = 10  # 每次移动步长

def get_thumb_direction(hand_landmarks):
    """
    根据大拇指和其他手指的位置判断方向
    返回: "up", "down", "left", "right", or None
    """
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

    # 左右判断：基于大拇指x坐标相对于手腕和尾指的位置
    if thumb_tip.x < wrist.x and thumb_tip.x < pinky_pip.x:
        return "left"
    if thumb_tip.x > wrist.x and thumb_tip.x > index_finger_pip.x:
        return "right"

    # 上下判断：基于大拇指y坐标相对于手腕和食指的位置
    if thumb_tip.y < index_finger_pip.y and thumb_tip.y < wrist.y:
        return "up"
    if thumb_tip.y > wrist.y:
        return "down"
        
    return None

def main():
    last_move_time = 0
    move_interval = 0.5  # 每次移动的最小时间间隔（秒）

    try:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("无法读取摄像头数据")
                time.sleep(1) # 等待一下再试
                continue

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)

            direction = None
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    direction = get_thumb_direction(hand_landmarks)
            
            current_time = time.time()
            if direction and (current_time - last_move_time > move_interval):
                last_move_time = current_time
                if direction == "up":
                    print("检测到方向: up, 电机2向上移动")
                    motor.rotate(motor.motor2, MOTOR_STEP)
                elif direction == "down":
                    print("检测到方向: down, 电机2向下移动")
                    motor.rotate(motor.motor2, -MOTOR_STEP)
                elif direction == "left":
                    print("检测到方向: left, 电机1向左移动")
                    motor.rotate(motor.motor1, -MOTOR_STEP)
                elif direction == "right":
                    print("检测到方向: right, 电机1向右移动")
                    motor.rotate(motor.motor1, MOTOR_STEP)

            # 短暂休眠，避免CPU占用过高
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\n程序被用户中断")
    finally:
        print("正在关闭电机并释放摄像头...")
        for pin in motor.pins:
            motor.wiringpi.digitalWrite(pin, 0)
        cap.release()
        print("清理完成。")


if __name__ == '__main__':
    main() 