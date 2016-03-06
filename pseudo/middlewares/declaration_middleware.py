from pseudo.middlewares.middleware import Middleware

class DeclarationMiddleware(Middleware):
    '''
    finds and marks first initializations of locals

    adds a boolean first_mention field to assignments for first mentions of locals as targets of
    assignments
    adds a local_declarations array with local not-arg names to function/methods
    rebuilds tree TreeTransformer in place!!
    '''

    @classmethod
    def process(cls, tree):
        return cls(tree).transform(tree)

    def __init__(self, tree):
        self.envs = [set()]
    
    def transform_module(self, node, in_block=False, assignment=None):
        self.current_function_ = node
        node.local_declarations = []
        node.definitions = self.transform(node.definitions)
        node.main = self.transform(node.main)
        return node

    def transform_f(self, node, in_block=False, assignment=None):
        self.envs.append(set(node.params))
        self.current_function_, old_function = node, self.current_function_
        node.local_declarations = []
        node.block = self.transform(node.block)
        self.current_function_ = old_function
        self.envs.pop()
        return node

    transform_function = transform_methods = transfrom_anonymous_function = transform_f

    def transform_assignment(self, node, in_block=False, assignment=None):
        if node.target.type == 'local' and node.target.name not in self.envs[-1]:
            node.first_mention = True
            self.current_function_.local_declarations.append(node.target.name)
        else:
            node.first_mention = False
        node.value = self.transform(node.value) # lambda can be somewhere here
        return node

    def transform__go_multi_assignment(self, node, in_block=False, assignment=False):
        node.first_mention = False
        for t in node.targets:
            if t.type == 'local' and t.name not in self.envs[-1]:
                node.first_mention = True
                self.current_function_.local_declarations.append(t.name)
        node.values = self.transform(node.values)
        return node

