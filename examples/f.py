class Shape:
    def __init__(self, a):
        self.a = a

    def area(self):
        return self.a * self.a


s = Shape(0)
s.area()
