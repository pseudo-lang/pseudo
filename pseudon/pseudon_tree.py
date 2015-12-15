class Node:

    def __init__(self, type, fields):
        self.type = type
        self.__dict__.update(fields)
