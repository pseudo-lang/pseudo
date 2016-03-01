import textwrap
from pseudon import generate
from pseudon.pseudon_tree import Node

#v
def gen(ast):
    return generate(ast, 'python')[:-1] #without last \n

def test_module():
    source = gen(Node('module', code=[]))
    assert source == ''

def test_int():
    source = gen(Node('int', value=42))
    assert source == '42'

def test_float():
    source = gen(Node('float', value=42.420))
    assert source == '42.42'

def test_str():
    source = gen(Node('string', value='la'))
    assert source == "'la'"

def test_boolean():
    source = gen(Node('boolean', value=True))
    assert source == 'True'

def test_null():
    source = gen(Node('null'))
    assert source == 'None'

def test_dictionary():
    source = gen(Node('dictionary', pairs=[
        [Node('string', value='la'), Node('int', 0)]]))
    assert source == "{'la': 0}"

def test_list():
    source = gen(Node('list', elements=[Node('string', value='la')]))
    assert source == "['la']"

def test_local():
    source = gen(Node('local', name='egg'))
    assert source == 'egg'

def test_typename():
    source = gen(Node('typename', name='Egg'))
    assert source == 'Egg'

def test_instance_variable():
    source = gen(Node('instance_variable', name='egg'))
    assert source == 'self.egg'

def test_attr():
    source = gen(Node('attr', receiver=Node('local', name='e'), attr='egg'))
    assert source == 'e.egg'

def test_local_assignment():
    source = gen(Node('local_assignment', local='egg', value=Node('local', name='ham')))
    assert source == 'egg = ham'

def test_instance_assignment():
    source = gen(Node('instance_assignment', name='egg', value=Node('local', name='ham')))
    assert source == 'self.egg = ham'

def test_attr_assignment():
    source = gen(Node('attr_assignment', 
        attr=Node('attr', receiver=Node('typename', name='T'), attr='egg'), 
         value=Node('local', name='ham')))
    assert source == 'T.egg = ham'

def test_call():
    source = gen(Node('call', function=Node('local', name='map'), args=[Node('local', name='x')]))
    assert source == 'map(x)'

def test_method_call():
    source = gen(Node('method_call', receiver=Node('local', name='e'), message='filter', args=[Node('int', value=42)]))
    assert source == 'e.filter(42)'

def test_standard_call():
    source = gen(Node('standard_call', function='display', args=[Node('int', value=42)]))
    assert source == 'print(42)'

    source = gen(Node('standard_call', function='read', args=[]))
    assert source == 'input()'

def test_standard_method_call():
    source = gen(Node('standard_method_call', receiver=Node('local', name='l', type='List[Int]'), message='length', args=[]))
    assert source == 'len(l)'

    source = gen(Node('standard_method_call', receiver=Node('str', value='l'), message='substr', args=[Node('int', value=0), Node('int', value=2)]))
    assert source == 'l[0:2]'

def test_binary_op():
    source = gen(Node('binary_op', op='+', left=Node('local', name='ham'), right=Node('local', name='egg')))
    assert source == 'ham + egg'

def test_unary_op():
    source = gen(Node('unary_op', op='-', value=Node('local', name='a')))
    assert source == '-a'

def test_standard_math():
    source = gen(Node('module', code=[
        Node('standard_math', op='sin', args=[Node('local', name='ham')])]))
    assert source == 'import math\nmath.sin(ham)'

def test_comparison():
    source = gen(Node('comparison', op='>', left=Node('local', name='egg'), right=Node('local', name='ham')))
    assert source == 'egg > ham'


def test_if():
    source = gen(Node('if_statement', 
        test=Node('comparison',
            op='==',
            left=Node('local', name='egg'), 
            right=Node('local', name='ham')),
        block=[
            Node('standard_method_call',
                receiver=Node('local', name='l', type='List[String]'),
                message='sublist',
                args=[Node('int', value=0), Node('int', value=2)])],
        otherwise=Node('if', 
            test=Node('comparison',
                op='==',
                left=Node('local', name='egg'), 
                right=Node('local', name='ham')),
            block=[
                Node('standard_call', function='display', args=[Node('float', '4.2')])
            ],
            otherwise=[
                Node('local', 'z', type='List[String]')
            ])))

    assert source == textwrap.dedent('''\
            if egg == ham:
                l[0:2]
            elif egg == ham:
                print(4.2)
            else:
                z''')


def test_for_each():
    source = gen(Node('for_each_statement', 
        iterator='a',
        sequence=Node('local', name='sequence', type='List[String]'),
        block=[
            Node('method_call',
                receiver=Node('local', name='a'),
                message='sub',
                args=[])]))

    assert source == textwrap.dedent('''\
            for a in sequence:
                a.sub()''')

def test_for_range():
    source = gen(Node('for_range_statement', 
        index='j',
        first=Node('int', value=0),
        last=Node('int', value=42),
        step=Node('int', value=2),
        block=[
            Node('call',
                function=Node('local', name='analyze', type='Function[Int, Int]'),
                args=[Node('local', name='j', type='Int')])]))

    assert source == textwrap.dedent('''\
            for j in range(0, 42, 2):
                analyze(j)''')

def test_for_each_with_index():
    source = gen(Node('for_each_with_index_statement', 
        index='j',
        iterator='k',
        sequence=Node('local', name='z', type='List[String]'),
        block=[
            Node('call',
                function=Node('local', name='analyze', type='Function[Int, String, Int]'),
                args=[Node('local', name='j', type='Int'), Node('local', name='k', type='String')])]))

    assert source == textwrap.dedent('''\
            for j, k in enumerate(z):
                analyze(j, k)''')

    source = gen(Node('for_each_with_index_statement', 
        index='j',
        iterator='k',
        sequence=Node('local', name='z', type='Dictionary[String, Int]'),
        block=[
            Node('call',
                function=Node('local', name='analyze', type='Function[String, Int, Int]'),
                args=[Node('local', name='j', type='String'), Node('local', name='k', type='Int')])]))

    assert source == textwrap.dedent('''\
            for j, k in z.items():
                analyze(j, k)''')


def test_for_each_in_zip():
    source = gen(Node('for_each_in_zip_statement', 
        iterators=['k', 'l']
        sequences=[
            Node('local', name='z', type='List[String]'),
            Node('local', name='zz', type='List[Int]')
        ],
        block=[
            Node('call',
                function=Node('local', name='a', type='Function[String, Int, Int]'),
                args=[Node('local', name='k', type='String'), Node('local', name='l', type='Int')])]))

    assert source == textwrap.dedent('''\
            for k, l in zip(z, zz):
                a(k, l)''')

def test_while():
    source = gen(Node('while_statement', 
        test=Node('comparison',
            op='>=',
            right=Node('int', 42),
            left=Node('call', function=Node('local', name='f'), args=[])),
        block=[
            Node('local_assignment', local='b', value=Node('call', function=Node('local', name='g'), args=[]))
        ]))

    assert source == textwrap.dedent('''\
            while f() >= 42:
                b = g()''')


def test_function():
    source = gen(Node('function_definition', 
        name='weird',
        params=[Node('local', name='z', type='Int')],
        type='Function[Int, Int]',
        return_type='Int',
        block=[
            Node('local_assignment', local='fixed', value=Node('call', function=Node('local', name='fix'), args=[Node('local', name='z')])),
            Node('implicit_return', value=Node('local', name='fixed'))
        ]))

    assert source == textwrap.dedent('''\
            def weird(z):
                fixed = fix(z)
                return fixed''')

def test_method():
    source = gen(Node('method_definition', 
        name='parse',
        params=[Node('local', name='source', type='String')],
        this=Node('typename', name='A'),
        type='Function[String, List[String]]',
        return_type='List[String]',
        block=[
            Node('instance_assignment', local='ast', value=Node('null'))
            Node('implicit_return', value=Node('list', elements=[Node('local', name='source')]))
        ]))

    assert source == textwrap.dedent('''\
            def parse(self, source):
                self.ast = None
                return [source]''')

def test_anonymous_function():
    source = gen(Node('anonymous_function', 
        params=[Node('local', name='source', type='String')],
        type='Function[String, List[String]]',
        return_type='List[String]',
        block=[
            Node('implicit_return', value=Node('call', function=Node('local', name='ves'), args=[
                Node('standard_method_call', 
                    receiver=Node('local', name='source', type='String'),
                    message='length',
                    args=[])]))
        ]))

    assert source == textwrap.dedent('''\
            lambda source: ves(len(source))''')

    source = gen(Node('anonymous_function', 
        params=[Node('local', name='source', type='String')],
        type='Function[String, List[String]]',
        return_type='List[String]',
        block=[
            Node('standard_call', function='display', args=[Node('local', name='source', type='String')]),
            Node('implicit_return', value=Node('call', function=Node('local', name='ves'), args=[
                Node('standard_method_call', 
                    receiver=Node('local', name='source', type='String'),
                    message='length',
                    args=[])]))
        ]))
    
    assert source == textwrap.dedent('''\
            def print_and_ves(source):
                print(source)
                return ves(source)

            print_and_ves''')

def test_class():
    source = gen(Node('class_statement', 
        name='A',
        parent='B',
        constructor=Node('constructor',
            params=[Node('local', name='a', type='Int')],
            this=Node('typename', name='A'),
            type='Function[Int, A]',
            return_type='A',
            block=[
                Node('instance_assignment', name='a', value=Node('local', name='a', type='Int'))
            ]),
        attrs=[
            Node('instance_variable', name='a', type='Int')
        ],
        methods=[
            Node('method',
                name='parse',
                params=[],
                this=Node('typename', name='A'),
                type='Function[Int]',
                return_type='Int',
                block=[
                    Node('int', value=42)
                ])
        ]))

    assert source == textwrap.dedent('''\
            class A(B):
                def __init__(self, a):
                    self.a = a

                def parse(self):
                    return 42''')

def test_this():
    source = gen(Node('this', type='A'))
    assert source == 'self'

def test_constructor():
    source = gen(Node('constructor',
            params=[
                Node('local', name='a', type='Int'),
                Node('local', name='b', type='String')
            ],
            this=Node('typename', name='A'),
            type='Function[Int, String, A]',
            return_type='A',
            block=[
                Node('instance_assignment', name='a', value=Node('local', name='a', type='Int')),
                Node('instance_assignment', name='b', value=Node('local', name='b', type='String'))
            ]))

    assert source == textwrap.dedent('''\
                def __init__(self, a, b):
                    self.a = a
                    self.b = b''')
