class Vehicle:
    def __init__(self, speed, size, acceleration):
        print(f"初速度:{speed} 加速度:{acceleration} 体积:{size}")
        self.setSpeed(speed)
        print(f"设置的初速度为:{self.speed}")
        self.size = size
        self.acceleration = acceleration

    def move(self, time):
        print(f"移动了：{self.speed * time}")

    def setSpeed(self, speed):
        self.speed = speed

    def speedUp(self, time):
        self.setSpeed(self.speed + self.acceleration * time)
        print(f"加速完后速度是:{self.speed}")

    def speedDown(self, time):
        clac_speed = self.speed - (self.acceleration + self.size) * time
        clac_speed = clac_speed if clac_speed > 0 else 0
        print(f"减速完后速度是:{clac_speed}")


speed = int(input())
size = int(input())
time = int(input())
acceleration = int(input())
v = Vehicle(speed, size, acceleration)
v.speedUp(time)
v.speedDown(time)
