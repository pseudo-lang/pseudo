def f(s):
    return s(2)

class A:
    def expand(self, a):
        return B(a)


class B:
    def __init__(self, a):
        self.a = a


