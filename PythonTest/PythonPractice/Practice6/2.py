class Vehicle:
    def __init__(self, speed, size, time, acceleration):
        print(f"初速度:{speed} 加速度:{acceleration} 体积:{size}")
        self.speed = speed
        self.size = size
        self.time = time
        self.acceleration = acceleration

    def move(self):
        print(f"移动了：{self.speed * self.time}")

    def setSpeed(self):
        print(f"设置的初速度为:{self.speed}")

    def speedUp(self):
        print(f"加速完后速度是:{self.speed + self.acceleration * self.time}")

    def speedDown(self):
        print(f"减速完后速度是:{max(0, self.speed - self.acceleration * self.time)}")


speed = int(input())
size = int(input())
time = int(input())
acceleration = int(input())
v = Vehicle(speed, size, time, acceleration)
v.setSpeed()
v.speedUp()
v.speedDown()