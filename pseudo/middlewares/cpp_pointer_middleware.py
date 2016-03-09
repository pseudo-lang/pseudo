from pseudo.middlewares.middleware import Middleware
from pseudo.pseudo_tree import Node, method_call

BUILTIN_SIMPLE = {'Int', 'String', 'Void', 'Exception', 'Float', 'Boolean', 'CppIterator', 'ifstream', 'istreambuf_iterator<char>', 'Library'}

class CppPointerMiddleware(Middleware):
    '''
    converts variables allocated with `new` to pointers

    if a variable is allocated with `new`, it's type T is transformed to Pointer[T] and the method calls on it are transformed to pointer_method_calls
    '''

    @classmethod
    def process(cls, tree):
        return cls(tree).transform(tree)

    def __init__(self, tree):
        self.tree = tree

    def after(self, node, in_block=False, assignment=None):
        node.pseudo_type = self.process_type(node.pseudo_type)

        if node.type == 'method_call':
            if not node.receiver.pseudo_type:
                node.receiver = node.receiver.name
        if node.type == 'method_call' and isinstance(node.receiver, str):
            input(node.y)
        if node.type == 'method_call' and isinstance(node.receiver.pseudo_type, list) and node.receiver.pseudo_type[0] == 'Pointer':
            node.type = 'pointer_method_call'            
        return node

    def process_type(self, t):
        if isinstance(t, list) and t[0] != 'Pointer':
            return [t[0]] + [self.process_type(a) for a in t[1:]]
        elif t and t not in BUILTIN_SIMPLE and not t.endswith('Error'):
            return ['Pointer', t]
        else:
            return t
