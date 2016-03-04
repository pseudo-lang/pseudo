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
         value=local('ham', pseudo_type='String'))
]
Call        = [call('map', [local('x')])]
MethodCall  = [method_call(local('e'), 'filter', [to_node(42)])]
StandardCall = [
    Node('standard_call', namespace='io', function='display', args=[to_node(42)]),
    Node('standard_call', namespace='io', function='read', args=[]),
    Node('standard_call', namespace='math', function='ln', args=[Node('local', name='ham', pseudo_type='Int')]),
    Node('standard_call', namespace='io', function='read_file', args=[to_node("'f.py'")])
]

StandardMethodCall = [
    Node('standard_method_call', receiver=Node('local', name='l', pseudo_type='List[Int]'), message='length', args=[]),
    Node('standard_method_call', receiver=Node('string', value='l', pseudo_type='String'), message='substr', args=[Node('int', value=0), Node('int', value=2)])
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
                receiver=Node('local', name='l', pseudo_type='List[String]'),
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
                Node('local', name='z', pseudo_type='List[String]')
            ])))
]


ForEachStatement = [Node('for_each_statement', 
        iterator='a',
        sequence=Node('local', name='sequence', pseudo_type='List[String]'),
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
                function=Node('local', name='analyze', pseudo_type='Function[Int, Int]'),
                args=[Node('local', name='j', pseudo_type='Int')])])]
ForEachWithIndexStatement = [
    Node('for_each_with_index_statement', 
        index='j',
        iterator='k',
        sequence=Node('local', name='z', pseudo_type='List[String]'),
        block=[
            Node('call',
                function=Node('local', name='analyze', pseudo_type='Function[Int, String, Int]'),
                args=[Node('local', name='j', pseudo_type='Int'), Node('local', name='k', pseudo_type='String')])]),
 
    Node('for_each_with_index_statement', 
        index='j',
        iterator='k',
        sequence=Node('local', name='z', pseudo_type='Dictionary[String, Int]'),
        block=[
            Node('call',
                function=Node('local', name='analyze', pseudo_type='Function[String, Int, Int]'),
                args=[Node('local', name='j', pseudo_type='String'), Node('local', name='k', pseudo_type='Int')])])
]

ForEachInZipStatement = [Node('for_each_in_zip_statement', 
        iterators=['k', 'l'],
        sequences=[
            Node('local', name='z', pseudo_type='List[String]'),
            Node('local', name='zz', pseudo_type='List[Int]')
        ],
        block=[
            Node('call',
                function=Node('local', name='a', pseudo_type='Function[String, Int, Int]'),
                args=[Node('local', name='k', pseudo_type='String'), Node('local', name='l', pseudo_type='Int')])])]
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
                Node('instance_assignment', name='a', value=Node('local', name='a', pseudo_type='Int'))
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
                Node('instance_assignment', name='a', value=Node('local', name='a', pseudo_type='Int')),
                Node('instance_assignment', name='b', value=Node('local', name='b', pseudo_type='String'))
            ])]

Index = [Node('index', sequence=to_node("'la'"), pseudo_type='String'), index=to_node(2))]
IndexAssignment = [Node('index_assignment', 
    sequence=local('x', pseudo_type=['List', 'String']),
    index=to_node(4),
    value=to_node('"String"'))]

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


