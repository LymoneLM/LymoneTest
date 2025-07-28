import wiringpi
import time
import random

# 初始化wiringPi库
wiringpi.wiringPiSetup()


class StepperMotorController:
    def __init__(self):
        self.last_btm_degree = 170    # 最近一次底部舵机的角度值记录
        self.last_top_degree = 60    # 最近一次顶部舵机的角度值记录

        # 定义电机控制引脚
        self.IN1, self.IN2, self.IN3, self.IN4 = 3, 4, 6, 9
        self.IN5, self.IN6, self.IN7, self.IN8 = 10, 13, 15, 16

        # 将所有引脚设置为输出模式
        self.pins = [self.IN1, self.IN2, self.IN3, self.IN4, self.IN5, self.IN6, self.IN7, self.IN8]
        for pin in self.pins:
            wiringpi.pinMode(pin, 1)

        # 定义步进电机的步序（2相全步）
        self.sequence = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1]
        ]

    def rotate_angle(self, motor_pins, angle):
        # 根据角度确定旋转方向并选择相应的序列
        seq = self.sequence if angle >= 0 else self.sequence[::-1]

        # 计算所需的步数
        step_num = int(abs(angle) / 360 * 4096)

        # 遍历每一步
        for i in range(step_num):
            step = seq[i % 8]
            for pin, value in zip(motor_pins, step):
                wiringpi.digitalWrite(pin, value)
            time.sleep(0.001)

    # 电机角度初始化
    def set_cloud_platform_degree(self, btm=170, top=60):

        angle1 = 350  # 第一个电机旋转的角度
        angle2 = 130  # 第二个电机旋转的角度
        self.rotate_motors(angle1, angle2)
        time.sleep(1)  # 等待1秒
        self.rotate_motors(-angle1, -angle2)

        self.rotate_angle([self.IN1, self.IN2, self.IN3, self.IN4], btm)
        self.rotate_angle([self.IN5, self.IN6, self.IN7, self.IN8], top)
        time.sleep(0.01)

    def rotate_motors(self, angle1, angle2):
        # 旋转两个电机
        self.rotate_angle([self.IN1, self.IN2, self.IN3, self.IN4], angle1)
        self.rotate_angle([self.IN5, self.IN6, self.IN7, self.IN8], angle2)


    def stop_motors(self):
        # 关闭所有电机控制引脚
        for pin in self.pins:
            wiringpi.digitalWrite(pin, 0)


# 如果脚本被执行，创建对象并运行示例
if __name__ == "__main__":
    motor_controller = StepperMotorController()
    # motor_controller.set_cloud_platform_degree()
    try:
        for _ in range(3):
            angle1 = 350  # 第一个电机旋转的角度
            angle2 = 130  # 第二个电机旋转的角度
            motor_controller.rotate_motors(angle1, angle2)
            time.sleep(1)  # 等待1秒
            motor_controller.rotate_motors(-angle1, -angle2)
    finally:
        motor_controller.stop_motors()
