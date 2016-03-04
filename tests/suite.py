import re
from pseudon.pseudon_tree import Node, to_node, call, method_call, local, assignment

SNAKE_CASE_REGEX = re.compile(r'(_\[a-z])')

class TestLanguage(type):

    def __new__(cls, name, bases, namespace, **kwargs):

        def generate_test(name, examples, expected_):
            def test(self):
                if isinstance(expected_, (str, tuple)):
                    expected = [expected_]
                else:
                    expected = expected_

                for example, exp in zip(examples, expected):
                    if isinstance(exp, str):
                        self.assertEqual(self.gen(example), exp)
                    elif exp[0] == 'raw':
                        self.assertEqual(self.gen(example), exp)
                    else:
                        imports, source = self.gen_with_imports(example)
                        self.assertEqual(imports, exp[0])
                        self.assertEqual(source, exp[1])
            return test

        types = list(namespace.keys())
        for name in types:
            exp = namespace[name]
            if name.startswith('gen') or name[0] == '_':
                continue
            if name[-1] == '_':
                name = name[:-1] # int etc
            examples = globals().get(name.title().replace('_', ''))
            if examples:
                test_name = 'test_%s' % name
                namespace[test_name] = generate_test(name, examples, exp)

        return super().__new__(cls, name, bases, namespace)

Module      = [Node('module', constants=[], code=[])]
Int         = [to_node(42)]
Float       = [to_node(42.420)]
String      = [to_node("'la'")]
Boolean     = [to_node(True)]
Null        = [Node('null')]
Dictionary  = [Node('dictionary', pairs=[
                Node('pair', key=to_node("'la'"), value=to_node(0))])]
List        = [Node('list', elements=[to_node("'la'")])]
Local       = [local('egg')]
Typename    = [to_node('Egg')]
InstanceVariable = [Node('instance_variable', name='egg')]
Attr        = [Node('attr', object=local('e'), attr='egg')]
Assignment = [
    Node('assignment', target=local('egg', pseudo_type='Int'), value=local('ham', pseudo_type='Int')),
    Node('assignment', target=Node('instance_variable', name='egg', pseudo_type='Int'), value=local('ham', pseudo_type='Int')),
    Node('assignment', target=Node('attr', object=Node('typename', name='T'), attr='egg', pseudo_type='String'), 
         value=local('ham', pseudo_type='String')),
    Node('assignment', 
        target=Node('index',
            sequence=local('x', pseudo_type=['List', 'String']),
            index=to_node(4),
            pseudo_type='String'),
        value=to_node('"String"'))
]
Call        = [call('map', [local('x')])]
MethodCall  = [method_call(local('e'), 'filter', [to_node(42)])]
StandardCall = [
    Node('standard_call', namespace='io', function='display', args=[to_node(42)], pseudo_type='Void'),
    Node('standard_call', namespace='io', function='read', args=[], pseudo_type='String'),
    Node('standard_call', namespace='math', function='ln', args=[Node('local', name='ham', pseudo_type='Int')], pseudo_type='Float'),
    assignment(
        local('source', pseudo_type='String'),
        Node('standard_call', namespace='io', function='read_file', args=[to_node('"f.py"')], pseudo_type='String'))
]

StandardMethodCall = [
    Node('standard_method_call', receiver=local('l', pseudo_type=['List', 'Int']), message='length', args=[], pseudo_type='Int'),
    Node('standard_method_call', receiver=to_node('"l"'), message='substr', args=[to_node(0), to_node(2)], pseudo_type='String')
]

BinaryOp = [Node('binary_op', op='+', left=local('ham', pseudo_type='Int'), right=local('egg', pseudo_type='Int'))]
UnaryOp = [Node('unary_op', op='-', value=local('a', 'Int'))]
Comparison = [Node('comparison', op='>', left=local('egg', 'Float'), right=local('ham', 'Float'))]

IfStatement = [
    Node('if_statement', 
        test=Node('comparison',
            op='==',
            left=local('egg', 'Float'),
            right=local('ham', 'Float'),
            pseudo_type='Boolean'),
        block=[
            Node('standard_method_call',
                receiver=local('l', ['List', 'String']),
                message='slice',
                args=[to_node(0), to_node(2)],
                pseudo_type=['List', 'String'])],
        otherwise=Node('elseif_statement', 
            test=Node('comparison',
                op='==',
                left=local('egg', 'Float'),
                right=local('ham', 'Float'),
                pseudo_type='Boolean'),
            block=[
                Node('standard_call', 
                      namespace='io', 
                      function='display', 
                      args=[to_node(4.2)],
                      pseudo_type='Void')
            ],
            otherwise=Node('else_statement', block=[
                local('z', ['List', 'String'])
            ])))
]


ForStatement = [
    Node('for_statement', 
        iterators=Node('for_iterator',
                iterator=local('a', 'String')),
        sequences=Node('for_sequence',
                sequence=local('sequence', ['List', 'String'])),
        block=[
            call(local('log', ['Function', 'String', 'Void']),
                 [local('a', 'String')],
                 pseudo_type='Void')
        ]),

    Node('for_range_statement', 
        index=local('j', 'Int'),
        first=Node('int', value=0),
        last=Node('int', value=42),
        step=Node('int', value=2),
        block=[
            call(local('analyze', ['Function', 'Int', 'Int']),
                 [local('j', 'Int')],
                 pseudo_type='Int')
        ]),

    Node('for_statement', 
        iterators=Node('for_iterator_with_index',
                index=local('j', 'Int'),
                iterator=local('k', 'String')),
        sequences=Node('for_sequence_with_index',
                sequence=local('z', ['List', 'String'])),
        block=[
            call(local('analyze', ['Function', 'Int', 'String', 'Int']),
                 [local('j', 'Int'), local('k','String')],
                 pseudo_type='Int')]),

    Node('for_statement', 
        iterators=Node('for_iterator_with_items',
                key=local('j', 'Int'),
                value=local('k', 'String')),
        sequences=Node('for_sequence_with_items',
                sequence=local('z', ['Dictionary', 'Int', 'String'])),
        block=[
            call(local('analyze', ['Function', 'String', 'Int', 'Int']),
                 [local('k','String'), local('j', 'Int')],
                 pseudo_type='Int')]),

    Node('for_statement',
        iterators=Node('for_iterator_zip',
                iterators=[local('k', 'Int'), local('l', 'String')]),
        sequences=Node('for_sequence_zip',
                sequences=[local('z', ['List', 'Int']), local('zz', ['List', 'String'])]),
        block=[
            call(local('a', ['Function', 'Int', 'String', 'Int']),
                 [local('k', 'Int'), local('l','String')])])
]

WhileStatement = [Node('while_statement', 
        test=Node('comparison',
            op='>=',
            right=to_node(42),
            left=call(local('f'), [])),
        block=[
            Node('assignment', target=local('b', pseudo_type='Int'), value=call(local('g'), [], pseudo_type='Int'))
        ])]


FunctionDefinition = [Node('function_definition', 
        name='weird',
        params=[Node('local', name='z', pseudo_type='Int')],
        pseudo_type='Function[Int, Int]',
        return_type='Int',
        block=[
            Node('assignment', target=local('fixed', pseudo_type='Int'), value=call(local('fix'), [local('z')], pseudo_type='Int')),
            Node('implicit_return', value=Node('local', name='fixed'))
        ])]

MethodDefinition = [Node('method_definition', 
        name='parse',
        params=[Node('local', name='source', pseudo_type='String')],
        this=Node('typename', name='A'),
        pseudo_type='Function[String, List[String]]',
        return_type='List[String]',
        is_public=True,
        block=[
            Node('assignment', target=local('ast', pseudo_type='Void'), value=Node('null', pseudo_type='Void')),
            Node('implicit_return', value=Node('list', elements=[Node('local', name='source')]))
        ])]

AnonymousFunction = [
    Node('anonymous_function', 
        params=[Node('local', name='source', pseudo_type='String')],
        pseudo_type='Function[String, List[String]]',
        return_type='List[String]',
        block=[
            Node('implicit_return', value=call(local('ves'), [
                Node('standard_method_call', 
                    receiver=Node('local', name='source', pseudo_type='String'),
                    message='length',
                    args=[])]))
        ]),

    Node('anonymous_function', 
        params=[Node('local', name='source', pseudo_type='String')],
        pseudo_type='Function[String, List[String]]',
        return_type='List[String]',
        block=[
            Node('standard_call', namespace='io', function='display', args=[Node('local', name='source', pseudo_type='String')]),
            Node('implicit_return', value=call(local('ves'), [
                Node('standard_method_call', 
                    receiver=Node('local', name='source', pseudo_type='String'),
                    message='length',
                    args=[])]))])
]

ClassDefinition = [Node('class_definition', 
        name='A',
        base='B',
        constructor=Node('constructor',
            params=[Node('local', name='a', pseudo_type='Int')],
            this=to_node('A'),
            pseudo_type='Function[Int, A]',
            return_type='A',
            block=[
               Node('assignment', target=Node('instance_variable', name='a', pseudo_type='String'), value=local('a', pseudo_type='Int'))     
            ]),
        attrs=[
            Node('class_attr', name='a', is_public=True, pseudo_type='Int')
        ],
        methods=[
            Node('method_definition',
                name='parse',
                params=[],
                this=to_node('A'),
                pseudo_type='Function[Int]',
                return_type='Int',
                block=[
                    Node('implicit_return', value=to_node(42))
                ])
        ])]

This = [Node('this', pseudo_type='A')]

Constructor = [Node('constructor',
            params=[
                Node('local', name='a', pseudo_type='Int'),
                Node('local', name='b', pseudo_type='String')
            ],
            this=to_node('A'),
            pseudo_type='Function[Int, String, A]',
            return_type='A',
            block=[
                Node('assignment', target=Node('instance_variable', name='a'), value=Node('local', name='a', pseudo_type='Int')),
                Node('assignment', target=Node('instance_variable', name='b'), value=Node('local', name='b', pseudo_type='String'))
            ])]

Index = [Node('index', sequence=to_node("'la'"), pseudo_type='String', index=to_node(2))]

u0 = \
Node('try_statement', block=[
        call(local('a'), []),
        call(local('h'), [to_node(-4)])
    ], handlers=[
        Node('exception_handler',
            exception='Exception',
            is_builtin=True,
            instance='e',
            block=[
                Node('standard_call', namespace='io', function='display', args=[Node('local', name='e')])
            ])
    ])


u = Node('try_statement', block=[
        call(local('a'), []),
        call(local('h'), [to_node(-4)])
    ], handlers=[
        Node('exception_handler',
            exception='NeptunError',
            is_builtin = False,
            instance='e',
            block=[
                Node('standard_call', namespace='io', function='display', args=[Node('local', name='e')])
            ])
    ])

u2 = Node('custom_exception',
           name='NeptunError',
           base=None)

TryStatement = [
    u0,

    Node('block', block=[
        u2,
        u
    ])
]

ThrowStatement = [
    Node('block', block=[
        u2,

        Node('throw_statement',
          exception='NeptunError',
          value=to_node("'no tea'"))
    ])
]


