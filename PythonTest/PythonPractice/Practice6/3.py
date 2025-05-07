class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def distance(self, other):
        return round(((self.x - other.x)**2 + (self.y - other.y)**2)**0.5, 2)

class Line:
    def __init__(self, p1, p2):
        dx = p1.x - p2.x
        dy = p1.y - p2.y
        self.k = None if dx == 0 else dy / dx
    def relationship(self, other):
        if self.k is None and other.k is None:
            return "平行"
        if self.k is None or other.k is None:
            return "相交"
        return "平行" if abs(self.k - other.k) < 1e-9 else "相交"

p = [Point(*map(float, input().split(','))) for _ in range(4)]
print(f"两点的欧式距离是{p[0].distance(p[1]):.2f}")
line1, line2 = Line(p[0], p[1]), Line(p[2], p[3])
print(line1.relationship(line2))