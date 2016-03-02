import re
import unittest
from pseudon.pseudon_tree import Node, to_node, call, method_call, local

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

Module      = [Node('module', code=[])]
Int         = [to_node(42)]
Float       = [to_node(42.420)]
String      = [to_node("'la'")]
Boolean     = [to_node(True)]
Null        = [Node('null')]
Dictionary  = [Node('dictionary', pairs=[
                Node('pair', first=to_node("'la'"), second=to_node(0))])]
List        = [Node('list', elements=[to_node("'la'")])]
Local       = [local('egg')]
Typename    = [to_node('Egg')]
InstanceVariable = [Node('instance_variable', name='egg')]
Attr        = [Node('attr', object=local('e'), attr='egg')]
LocalAssignment = [Node('local_assignment', local='egg', value=local('ham'))]
InstanceAssignment = [Node('instance_assignment', name='egg', value=local('ham'))]
AttrAssignment = [Node('attr_assignment', 
        attr=Node('attr', object=to_node('T'), attr='egg'), 
         value=local('ham'))]
Call        = [call('map', [local('x')])]
MethodCall  = [method_call(local('e'), 'filter', [to_node(42)])]
StandardCall = [
    Node('standard_call', namespace='io', function='display', args=[to_node(42)]),
    Node('standard_call', namespace='io', function='read', args=[]),
    Node('standard_call', namespace='math', function='ln', args=[Node('local', name='ham', pseudon_type='Int')]),
    Node('standard_call', namespace='io', function='read_file', args=[to_node("'f.py'")])
]

StandardMethodCall = [
    Node('standard_method_call', receiver=Node('local', name='l', pseudon_type='List[Int]'), message='length', args=[]),
    Node('standard_method_call', receiver=Node('string', value='l', pseudon_type='String'), message='substr', args=[Node('int', value=0), Node('int', value=2)])
]

BinaryOp = [Node('binary_op', op='+', left=Node('local', name='ham'), right=Node('local', name='egg'))]
UnaryOp = [Node('unary_op', op='-', value=Node('local', name='a'))]
Comparison = [Node('comparison', op='>', left=Node('local', name='egg'), right=Node('local', name='ham'))]

IfStatement = [
    Node('if_statement', 
        test=Node('comparison',
            op='==',
            left=local('egg'),
            right=local('ham')),
        block=[
            Node('standard_method_call',
                receiver=Node('local', name='l', pseudon_type='List[String]'),
                message='slice',
                args=[to_node(0), to_node(2)])],
        otherwise=Node('elseif_statement', 
            test=Node('comparison',
                op='==',
                left=local('egg'),
                right=local('ham')),
            block=[
                Node('standard_call', namespace='io', function='display', args=[to_node(4.2)])
            ],
            otherwise=Node('else_statement', block=[
                Node('local', name='z', pseudon_type='List[String]')
            ])))
]


ForEachStatement = [Node('for_each_statement', 
        iterator='a',
        sequence=Node('local', name='sequence', pseudon_type='List[String]'),
        block=[
            Node('method_call',
                receiver=Node('local', name='a'),
                message='sub',
                args=[])])]
ForRangeStatement = [Node('for_range_statement', 
        index='j',
        first=Node('int', value=0),
        last=Node('int', value=42),
        step=Node('int', value=2),
        block=[
            Node('call',
                function=Node('local', name='analyze', pseudon_type='Function[Int, Int]'),
                args=[Node('local', name='j', pseudon_type='Int')])])]
ForEachWithIndexStatement = [
    Node('for_each_with_index_statement', 
        index='j',
        iterator='k',
        sequence=Node('local', name='z', pseudon_type='List[String]'),
        block=[
            Node('call',
                function=Node('local', name='analyze', pseudon_type='Function[Int, String, Int]'),
                args=[Node('local', name='j', pseudon_type='Int'), Node('local', name='k', pseudon_type='String')])]),
 
    Node('for_each_with_index_statement', 
        index='j',
        iterator='k',
        sequence=Node('local', name='z', pseudon_type='Dictionary[String, Int]'),
        block=[
            Node('call',
                function=Node('local', name='analyze', pseudon_type='Function[String, Int, Int]'),
                args=[Node('local', name='j', pseudon_type='String'), Node('local', name='k', pseudon_type='Int')])])
]

ForEachInZipStatement = [Node('for_each_in_zip_statement', 
        iterators=['k', 'l'],
        sequences=[
            Node('local', name='z', pseudon_type='List[String]'),
            Node('local', name='zz', pseudon_type='List[Int]')
        ],
        block=[
            Node('call',
                function=Node('local', name='a', pseudon_type='Function[String, Int, Int]'),
                args=[Node('local', name='k', pseudon_type='String'), Node('local', name='l', pseudon_type='Int')])])]
WhileStatement = [Node('while_statement', 
        test=Node('comparison',
            op='>=',
            right=to_node(42),
            left=call(local('f'), [])),
        block=[
            Node('local_assignment', local='b', value=Node('call', function=Node('local', name='g'), args=[]))
        ])]


FunctionDefinition = [Node('function_definition', 
        name='weird',
        params=[Node('local', name='z', pseudon_type='Int')],
        pseudon_type='Function[Int, Int]',
        return_type='Int',
        block=[
            Node('local_assignment', local='fixed', value=Node('call', function=Node('local', name='fix'), args=[Node('local', name='z')])),
            Node('implicit_return', value=Node('local', name='fixed'))
        ])]

MethodDefinition = [Node('method_definition', 
        name='parse',
        params=[Node('local', name='source', pseudon_type='String')],
        this=Node('typename', name='A'),
        pseudon_type='Function[String, List[String]]',
        return_type='List[String]',
        block=[
            Node('instance_assignment', name='ast', value=Node('null')),
            Node('implicit_return', value=Node('list', elements=[Node('local', name='source')]))
        ])]

AnonymousFunction = [
    Node('anonymous_function', 
        params=[Node('local', name='source', pseudon_type='String')],
        pseudon_type='Function[String, List[String]]',
        return_type='List[String]',
        block=[
            Node('implicit_return', value=call(local('ves'), [
                Node('standard_method_call', 
                    receiver=Node('local', name='source', pseudon_type='String'),
                    message='length',
                    args=[])]))
        ]),

    Node('anonymous_function', 
        params=[Node('local', name='source', pseudon_type='String')],
        pseudon_type='Function[String, List[String]]',
        return_type='List[String]',
        block=[
            Node('standard_call', namespace='io', function='display', args=[Node('local', name='source', pseudon_type='String')]),
            Node('implicit_return', value=call(local('ves'), [
                Node('standard_method_call', 
                    receiver=Node('local', name='source', pseudon_type='String'),
                    message='length',
                    args=[])]))])
]

ClassDefinition = [Node('class_definition', 
        name='A',
        parent='B',
        constructor=Node('constructor',
            params=[Node('local', name='a', pseudon_type='Int')],
            this=to_node('A'),
            pseudon_type='Function[Int, A]',
            return_type='A',
            block=[
                Node('instance_assignment', name='a', value=Node('local', name='a', pseudon_type='Int'))
            ]),
        attrs=[
            Node('instance_variable', name='a', pseudon_type='Int')
        ],
        methods=[
            Node('method_definition',
                name='parse',
                params=[],
                this=to_node('A'),
                pseudon_type='Function[Int]',
                return_type='Int',
                block=[
                    Node('implicit_return', value=to_node(42))
                ])
        ])]

This = [Node('this', pseudon_type='A')]

Constructor = [Node('constructor',
            params=[
                Node('local', name='a', pseudon_type='Int'),
                Node('local', name='b', pseudon_type='String')
            ],
            this=to_node('A'),
            pseudon_type='Function[Int, String, A]',
            return_type='A',
            block=[
                Node('instance_assignment', name='a', value=Node('local', name='a', pseudon_type='Int')),
                Node('instance_assignment', name='b', value=Node('local', name='b', pseudon_type='String'))
            ])]

u0 = \
Node('try_statement', block=[
        call(local('a'), []),
        call(local('h'), [to_node(-4)])
    ], handlers=[
        Node('exception_handler',
            exception='Exception',
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
            instance='e',
            block=[
                Node('standard_call', namespace='io', function='display', args=[Node('local', name='e')])
            ])
    ])

u2 = Node('class_definition',
           name='NeptunError',
           parent='Exception',
           constructor=None,
           attrs=[],
           methods=[])

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


