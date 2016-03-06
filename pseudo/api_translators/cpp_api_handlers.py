from pseudo.pseudo_tree import Node, call, method_call, local, assignment, to_node
from pseudo.api_handlers import BizarreLeakingNode, NormalLeakingNode

class Read(BizarreLeakingNode):
    '''
    transforms `io:read`

    `a = io:read()`
    `cin << a`
    '''

    def temp_name(self, target):
        return '_read_result'

    def as_expression(self):
        return [
            Node('_cpp_declaration',
                name='_dummy',
                args=[],
                decl_type='String',
                pseudo_type='Void'),
            Node('_cpp_cin', 
                args=[local('_dummy', 'String')])
        ], None

    def as_assignment(self, target):
        return [Node('_cpp_cin', args=[target])]

class Slice(BizarreLeakingNode):
    '''
    transforms `List:slice..`
    '''

    def temp_name(self, target):
        return '_sliced'

    def as_expression(self):
        # pseudo_type=self.args[0].pseudo_type
        begin = method_call(self.args[0], 'begin', [], 'CppIterator')
        end = method_call(self.args[0], 'end', [], 'CppIterator')
        if self.name == 'slice_to':
            from_, to = to_node(0), self.args[1]
        else:
            from_, to = self.args[1], self.args[2]
        if from_.type == 'int' and from_.value == 0:
            start = begin
        else:
            start = Node('binary_op', op='+', left=begin, right=from_, pseudo_type='CppIterator')
        if self.name == 'slice_from':
            finish = end
        elif to.type == 'int' and to.value < 0:
            finish = Node('binary_op', op='-', left=end, right=to_node(-to.value))
        else:
            finish = Node('binary_op', op='+', left=begin, right=to, pseudo_type='CppIterator')
        return [
            Node('_cpp_declaration', 
                name='_sliced', 
                args=[start, finish],
                decl_type=self.args[0].pseudo_type,
                pseudo_type='Void')], None

    def as_assignment(self, target):
        expression = self.as_expression()[0][0]
        expression.name = target.name
        return [expression]

class ReadFile(BizarreLeakingNode):
    '''
    transforms `io:read_file`
    '''

    def temp_name(self, target):
        return '_file_contents'

    def as_expression(self):
        return [Node('_cpp_declaration', 
                name='ifs',
                args=[to_node('f.py')],
                decl_type='ifstream',
                pseudo_type='Void'),
            Node('_cpp_declaration',
                name=self.temp_name(None),
                args=[Node('_cpp_group',
                        value=Node('_cpp_anon_declaration',
                            args=[local('ifs', 'ifstream')],
                            decl_type='istreambuf_iterator<char>',
                            pseudo_type='Void')),
                      Node('_cpp_group',
                        value=Node('_cpp_anon_declaration',
                            args=[],
                            decl_type='istreambuf_iterator<char>',
                            pseudo_type='Void'))],
                decl_type='String',
                pseudo_type='Void')], None

    def as_assignment(self, target):
        e = self.as_expression()[0]
        e[1].name = target.name
        return e