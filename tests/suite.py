import re
import unittest
from pseudon.pseudon_tree import Node

class TestLanguage(type):

    SNAKE_CASE_REGEX = re.compile(r'(_\[a-z])')

    def __new__(cls, name, bases, namespace, **kwargs):

        def generate_test(name, examples, expected):
            def test(self):
                if isinstance(expected, (str, tuple)):
                    expected = [expected]

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

        for name, exp in namespace:
            if name[-1] == '_':
                name = name[:-1] # int etc
            examples = getattr(suite, SNAKE_CASE_REGEX.sub(lambda e: e[1].upper(), name.title()))
            if examples:
                test_name = 'test_%s' % name
                namespace[test_name] = generate_test(name, exp)

        return super().__new__(cls, name, bases, namespace)

Module      = [Node('module', code=[])]
Int         = [Node('int', value=42)]
Float       = [Node('float', value=42.420)]
String      = [Node('string', value='la')]
Boolean     = [Node('boolean', value=True)]
Null        = [Node('null')]
Dictionary  = [Node('dictionary', pairs=[
                [Node('string', value='la'), Node('int', 0)]])]
List        = [Node('list', elements=[Node('string', value='la')])]
Local       = [Node('local', name='egg')]
Typename    = [Node('typename', name='Egg')]
InstanceVariable = [Node('instance_variable', name='egg')]
Attr        = [Node('attr', receiver=Node('local', name='e'), attr='egg')]
LocalAssignment = [Node('local_assignment', local='egg', value=Node('local', name='ham'))]
InstanceAssignment = [Node('instance_assignment', name='egg', value=Node('local', name='ham'))]
AttrAssignment = [Node('attr_assignment', 
        attr=Node('attr', receiver=Node('typename', name='T'), attr='egg'), 
         value=Node('local', name='ham'))]
Call        = [Node('call', function=Node('local', name='map'), args=[Node('local', name='x')])]
MethodCall  = [Node('method_call', receiver=Node('local', name='e'), message='filter', args=[Node('int', value=42)])]
StandardCall = [
    Node('standard_call', namespace='io', function='display', args=[Node('int', value=42)]),
    Node('standard_call', namespace='io', function='read', args=[]),
    Node('standard_call', namespace='math', function='ln', args=[Node('local', name='ham', pseudon_type='Int')]),
    Node('standard_call', namespace='io', function='read_file', args=[Node('string', value='f.py')])
]

StandardMethodCall = [
    Node('standard_method_call', receiver=Node('local', name='l', type='List[Int]'), message='length', args=[]),
    Node('standard_method_call', receiver=Node('str', value='l'), message='substr', args=[Node('int', value=0), Node('int', value=2)])
]

BinaryOp = [Node('binary_op', op='+', left=Node('local', name='ham'), right=Node('local', name='egg'))]
UnaryOp = [Node('unary_op', op='-', value=Node('local', name='a'))]
Comparison = [Node('comparison', op='>', left=Node('local', name='egg'), right=Node('local', name='ham'))]

IfStatement = [
    Node('if_statement', 
        test=Node('comparison',
            op='==',
            left=Node('local', name='egg'), 
            right=Node('local', name='ham')),
        block=[
            Node('standard_method_call',
                receiver=Node('local', name='l', pseudon_type='List[String]'),
                message='slice',
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
                Node('local', 'z', pseudon_type='List[String]')
            ]))
]


ForEach = [Node('for_each_statement', 
        iterator='a',
        sequence=Node('local', name='sequence', type='List[String]'),
        block=[
            Node('method_call',
                receiver=Node('local', name='a'),
                message='sub',
                args=[])])]
ForRange = [Node('for_range_statement', 
        index='j',
        first=Node('int', value=0),
        last=Node('int', value=42),
        step=Node('int', value=2),
        block=[
            Node('call',
                function=Node('local', name='analyze', type='Function[Int, Int]'),
                args=[Node('local', name='j', type='Int')])])]
ForEachWithIndex = [
    Node('for_each_with_index_statement', 
        index='j',
        iterator='k',
        sequence=Node('local', name='z', type='List[String]'),
        block=[
            Node('call',
                function=Node('local', name='analyze', type='Function[Int, String, Int]'),
                args=[Node('local', name='j', type='Int'), Node('local', name='k', type='String')])]),
 
    Node('for_each_with_index_statement', 
        index='j',
        iterator='k',
        sequence=Node('local', name='z', type='Dictionary[String, Int]'),
        block=[
            Node('call',
                function=Node('local', name='analyze', type='Function[String, Int, Int]'),
                args=[Node('local', name='j', type='String'), Node('local', name='k', type='Int')])])
]

ForEachInZip = [Node('for_each_in_zip_statement', 
        iterators=['k', 'l'],
        sequences=[
            Node('local', name='z', type='List[String]'),
            Node('local', name='zz', type='List[Int]')
        ],
        block=[
            Node('call',
                function=Node('local', name='a', type='Function[String, Int, Int]'),
                args=[Node('local', name='k', type='String'), Node('local', name='l', type='Int')])])]
WhileStatement = [Node('while_statement', 
        test=Node('comparison',
            op='>=',
            right=Node('int', 42),
            left=Node('call', function=Node('local', name='f'), args=[])),
        block=[
            Node('local_assignment', local='b', value=Node('call', function=Node('local', name='g'), args=[]))
        ])]


FunctionDefinition = [Node('function_definition', 
        name='weird',
        params=[Node('local', name='z', type='Int')],
        type='Function[Int, Int]',
        return_type='Int',
        block=[
            Node('local_assignment', local='fixed', value=Node('call', function=Node('local', name='fix'), args=[Node('local', name='z')])),
            Node('implicit_return', value=Node('local', name='fixed'))
        ])]

MethodDefinition = [Node('method_definition', 
        name='parse',
        params=[Node('local', name='source', type='String')],
        this=Node('typename', name='A'),
        type='Function[String, List[String]]',
        return_type='List[String]',
        block=[
            Node('instance_assignment', local='ast', value=Node('null')),
            Node('implicit_return', value=Node('list', elements=[Node('local', name='source')]))
        ])]

AnonymousFunction = [
    Node('anonymous_function', 
        params=[Node('local', name='source', type='String')],
        type='Function[String, List[String]]',
        return_type='List[String]',
        block=[
            Node('implicit_return', value=Node('call', function=Node('local', name='ves'), args=[
                Node('standard_method_call', 
                    receiver=Node('local', name='source', type='String'),
                    message='length',
                    args=[])]))
        ]),

    Node('anonymous_function', 
        params=[Node('local', name='source', type='String')],
        type='Function[String, List[String]]',
        return_type='List[String]',
        block=[
            Node('standard_call', function='display', args=[Node('local', name='source', type='String')]),
            Node('implicit_return', value=Node('call', function=Node('local', name='ves'), args=[
                Node('standard_method_call', 
                    receiver=Node('local', name='source', type='String'),
                    message='length',
                    args=[])]))])
]

ClassDefinition = [Node('class_definition', 
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
        ])]

This = [Node('this', type='A')]

Constructor = [Node('constructor',
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
            ])]

u = Node('try_statement', block=[
        Node('call', function=Node('local', name='a'), args=[]),
        Node('call', function=Node('local', name='h'), args=[Node('int', -4)])
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
           methods=[]),

TryStatement = [
    u,

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
            value=Node('string', value='no tea'))
    ])
]


