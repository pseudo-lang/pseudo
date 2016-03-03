class Shape:
    def __init__(self, a):
        self.a = a

    def area(self):
        return 0

    def peri(self):
        return 0


class Rectangle(Shape):
    def __init__(self, a,     b):
        self.a = a
        self.b = b

    def area(self):
        return self.a * self.b

    def peri(self):
        return 2 * self.a + 2 * self.b


class Square(Rectangle):
    def __init__(self, a):
        self.a = a
        self.b = a


s = Shape(0)
q = Rectangle(2, 4)
s2 = Square(4)
z = [s2, q, s2]
