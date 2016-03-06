class Env:

    def __init__(self, values=None, parent=None):
        self.values = values or {}
        self.parent = parent
        self.top = self if parent is None else parent.top

    def __getitem__(self, key):
        current = self
        while current is not None:
            if key in current.values:
                return current.values[key]
            current = current.parent

    def __setitem__(self, key, value):
        self.values[key] = value

    def motherify(self):
        return self.parent

    def child_env(self, values=None):
        return Env(values, self)
