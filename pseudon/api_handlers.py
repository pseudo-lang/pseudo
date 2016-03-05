class LeakingNode:
    def __init__(self, env, name, args):
        self.env  = env # namespace or class name
        self.name = name # function or method name
        self.args = args

    def as_expression(self):
        '''
        returns a list of nodes leaked in block and the expression node
        '''
        raise NotImplementedError('huh')

class NormalLeakingNode(LeakingNode):
    pass

class BizarreLeakingNode(LeakingNode):
    def as_assignment(self, target):
        '''
        returns a list of nodes leaked 
        in block
        '''
        raise NotImplementedError('why')
