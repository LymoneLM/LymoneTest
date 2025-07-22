import wiringpi
import time

wiringpi.wiringPiSetup()
IN1, IN2, IN3, IN4 = 3, 4, 6, 9
IN5, IN6, IN7, IN8 = 10, 13, 15, 16
pins = [IN1, IN2, IN3, IN4, IN5, IN6, IN7, IN8]
motor1 = pins[:4]
motor2 = pins[4:]
for pin in pins:
    wiringpi.pinMode(pin, 1)

# 定义步进电机的步序（2相全步）
sequence = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

def rotate(motor_pins, angle):
    seq = sequence if angle >= 0 else sequence[::-1]
    step_num = int(abs(angle) / 360 * 4096)
    for i in range(step_num):
        step = seq[i % 8]
        for _pin, value in zip(motor_pins, step):
            wiringpi.digitalWrite(_pin, value)
        time.sleep(0.001)

# 新增：电机休眠与唤醒函数

def sleep_motor():
    """
    关闭所有电机引脚，进入低功耗状态
    """
    for pin in pins:
        wiringpi.digitalWrite(pin, 0)

# 主函数， 控制步进电机
def main():
    # 主循环， 使电机旋转
    angle1 = 350 # 第一个电机旋转的角度
    angle2 = 130 # 第二个电机旋转的角度
    for _ in range(5):
        rotate(motor1, angle1) # 旋转第一个电机
        rotate(motor2, angle2) # 旋转第二个电机
        time.sleep(1) # 等待 1 秒
        rotate(motor1, -angle1) # 反向旋转第一个电机
        rotate(motor2, -angle2) # 反向旋转第二个电机
    # 关闭所有电机控制引脚
    for _pin in pins:
        wiringpi.digitalWrite(_pin, 0)

if __name__ == "__main__":
    rotate(motor1, 350)