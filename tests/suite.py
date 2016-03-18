import re
from pseudo.pseudo_tree import Node, to_node, call, method_call, local, typename, assignment
from pseudo import generate

SNAKE_CASE_REGEX = re.compile(r'(_\[a-z])')

def standard_method_call(receiver, message, args, pseudo_type):
    return Node('standard_method_call', 
        receiver=receiver,
        message=message,
        args=args,
        pseudo_type=pseudo_type)

def standard_call(namespace, function, args, pseudo_type):
    return Node('standard_call',
        namespace=namespace,
        function=function,
        args=args,
        pseudo_type=pseudo_type)

class TestLanguage(type):

    def __new__(cls, name, bases, namespace, **kwargs):

        def generate_test(name, examples, expected_):
            def test(self):
                if isinstance(expected_, (str, tuple)):
                    expected = [expected_]
                else:
                    expected = expected_

                if not isinstance(examples, list):
                    examples_ = [examples]
                else:
                    examples_ = examples
                for example, exp in zip(examples_, expected):
                    if isinstance(example, tuple) and example[0] == 'custom_exceptions':
                        custom_exceptions, example_ = example[1], example[2]
                        # import pdb;pdb.set_trace() #input(custom_exceptions)
                    else:
                        custom_exceptions = []
                        example_ = example if not isinstance(example, list) else example[:]
                    if isinstance(exp, str):
                        self.assertEqual(self.gen(custom_exceptions, example_), exp)
                    elif exp[0] == 'raw':
                        self.assertEqual(self.gen(custom_exceptions, example_), exp)
                    else:
                        # input(exp)
                        imports, source = self.gen_with_imports(custom_exceptions, example_)
                        self.assertCountEqual(imports, exp[0])
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

        if 'gen' not in namespace:
            namespace['gen'] = TestHelpers.gen
        if 'gen_with_imports' not in namespace:
            namespace['gen_with_imports'] = TestHelpers.gen_with_imports
        namespace['maxDiff'] = None
        return super().__new__(cls, name, bases, namespace)

Module      = [Node('module', constants=[], code=[])]
Int         = [to_node(42)]
Float       = [to_node(42.420)]
String      = [to_node('la')]
Boolean     = [Node('boolean', value='true', pseudo_type='Boolean')]
Null        = [Node('null')]
Dictionary  = [Node('dictionary', pairs=[
                Node('pair', key=to_node('la'), value=to_node(0))],
                pseudo_type=['Dictionary', 'String', 'Int'])]
List        = [Node('list', elements=[to_node('la')], pseudo_type=['List', 'String'])]
Local       = [local('egg')]
Typename    = [typename('Egg')]
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
        value=to_node('String'))
]
Call        = [call('map', [local('x')])]
MethodCall  = [method_call(local('e', 'E'), 'filter', [to_node(42)])]
StandardCall = [
    Node('standard_call', namespace='io', function='display', args=[to_node(42)], pseudo_type='Void'),
    Node('standard_call', namespace='io', function='read', args=[], pseudo_type='String'),
    Node('standard_call', namespace='math', function='ln', args=[Node('local', name='ham', pseudo_type='Int')], pseudo_type='Float'),
    assignment(
        local('source', pseudo_type='String'),
        Node('standard_call', namespace='io', function='read_file', args=[to_node('f.py')], pseudo_type='String'))
]

IoDisplay   = standard_call('io', 'display', [to_node(2), to_node('z')], 'Void')
IoRead      = assignment(local('source', 'String'), standard_call('io', 'read', [], 'String'))
IoReadFile  = assignment(local('source', 'String'), standard_call('io', 'read_file', [to_node('z.py')], 'String'))
IoWriteFile = standard_call('io', 'write_file', [to_node('z.py'), local('source', 'String')], 'Void')

INT_EXAMPLE = local('z', 'Int')
MathLn      = standard_call('math', 'ln', [INT_EXAMPLE], 'Float')
MathLog     = standard_call('math', 'log', [INT_EXAMPLE, to_node(2.0)], 'Float')
MathTan     = standard_call('math', 'tan', [INT_EXAMPLE], 'Float')
MathSin     = standard_call('math', 'sin', [INT_EXAMPLE], 'Float')
MathCos     = standard_call('math', 'cos', [INT_EXAMPLE], 'Float')


LIST_EXAMPLE_TYPE = ['List', 'String']
LIST_EXAMPLE = local('cpus', LIST_EXAMPLE_TYPE)
LIST_EXAMPLE_ELEMENT_TYPE = 'String'
LITERAL_STRING_EXAMPLE = to_node('')
STRING_EXAMPLE = local('s', 'String')
OTHER_STRING_EXAMPLE = local('t', 'String')

REGEXP_EXAMPLE = local('r', 'Regexp')
REGEXP_MATCH_EXAMPLE = local('m', 'RegexpMatch')

RegexpCompile = standard_call('regexp', 'compile', [STRING_EXAMPLE], 'Regexp')
RegexpEscape = standard_call('regexp', 'escape', [STRING_EXAMPLE], 'String')

EMPTY = Node('anonymous_function',
    params=[local('value', 'String')],
    block=[Node('implicit_return', value=Node('comparison',
        op='==',
        left=standard_method_call(local('value', 'String'), 'length', [], 'Int'),
        right=to_node(0)), pseudo_type='Boolean')],
    pseudo_type=['Function', 'String', 'Boolean'],
    return_type='Boolean')



ADD_A = Node('anonymous_function', 
    params=[local('value', 'String')],
    block=[Node('implicit_return',
                value=standard_method_call(
                    local('value', 'String'),
                    'concat',
                    [to_node('a')],
                    'String'),
                pseudo_type='String')],
    pseudo_type=['Function', 'String', 'String'],
    return_type='String')

COMBINER = Node('anonymous_function',
    params=[local('value', 'String'), local('other', 'String')],
    block=[
        assignment(local('result', 'String'), 
            standard_method_call(
                local('value', 'String'),
                'concat',
                [local('other', 'String')],
                'String')),
        Node('implicit_return', value=local('result', 'String'), pseudo_type='String')],
    pseudo_type=['Function', 'String', 'String'],
    return_type='String')

# Node('dictionary',
#     pairs=[Node('pair', key=to_node('s'), value=to_node(0))],
#     pseudo_type=DICTIONARY_EXAMPLE_TYPE)

DICTIONARY_EXAMPLE_TYPE = ['Dictionary', 'String', 'Int']
DICTIONARY_EXAMPLE = local('pointers', DICTIONARY_EXAMPLE_TYPE)
DICTIONARY_EXAMPLE_KEY_TYPE = 'String'
DICTIONARY_EXAMPLE_VALUE_TYPE = 'Int'

SET_EXAMPLE_TYPE = ['Set', 'String']
SET_EXAMPLE = local('words', SET_EXAMPLE_TYPE)

TUPLE_EXAMPLE_TYPE = ['Tuple', 'String', 'Int']
TUPLE_EXAMPLE = local('flowers', TUPLE_EXAMPLE_TYPE)

ARRAY_EXAMPLE_TYPE = ['Array', 'Int', 10]
ARRAY_EXAMPLE = local('cars', ARRAY_EXAMPLE_TYPE)
StandardMethodCall = [
    Node('standard_method_call', receiver=local('l', pseudo_type=['List', 'Int']), message='length', args=[], pseudo_type='Int'),
    Node('standard_method_call', receiver=to_node('l'), message='substr', args=[to_node(0), to_node(2)], pseudo_type='String'),
]


#List
ListPush        = standard_method_call(LIST_EXAMPLE, 'push', [LITERAL_STRING_EXAMPLE], 'Void')
ListPop         = standard_method_call(LIST_EXAMPLE, 'pop',  [], LIST_EXAMPLE_ELEMENT_TYPE)
ListLength      = standard_method_call(LIST_EXAMPLE, 'length', [], 'Int')
ListMap         = standard_method_call(LIST_EXAMPLE, 'map', [ADD_A], LIST_EXAMPLE_TYPE)
ListRemove      = standard_method_call(LIST_EXAMPLE, 'remove', [STRING_EXAMPLE], 'Void')
ListRemoveAt    = standard_method_call(LIST_EXAMPLE, 'remove_at', [to_node(0)], 'Void')
ListLength      = standard_method_call(LIST_EXAMPLE, 'length', [], 'Int')
ListSlice       = standard_method_call(LIST_EXAMPLE, 'slice', [to_node(2), to_node(-1)], LIST_EXAMPLE_TYPE)
ListSliceFrom   = standard_method_call(LIST_EXAMPLE, 'slice_from', [to_node(2)], LIST_EXAMPLE_TYPE)
ListSliceTo     = standard_method_call(LIST_EXAMPLE, 'slice_to', [to_node(2)], LIST_EXAMPLE_TYPE)
ListFilter      = standard_method_call(LIST_EXAMPLE, 'filter', [EMPTY], LIST_EXAMPLE_TYPE)
ListReduce      = standard_method_call(LIST_EXAMPLE, 'reduce', [COMBINER, to_node('')], 'String')
ListAny         = standard_method_call(LIST_EXAMPLE, 'any?', [EMPTY], 'Boolean')
ListAll         = standard_method_call(LIST_EXAMPLE, 'all?', [EMPTY], 'Boolean')
ListFind        = standard_method_call(LIST_EXAMPLE, 'find', [STRING_EXAMPLE], 'Int')
ListSort        = standard_method_call(LIST_EXAMPLE, 'sort', [], 'Void')
ListPresent     = standard_method_call(LIST_EXAMPLE, 'present?', [], 'Boolean')
ListEmpty       = standard_method_call(LIST_EXAMPLE, 'empty?', [], 'Boolean')
ListContains    = standard_method_call(LIST_EXAMPLE, 'contains?', [STRING_EXAMPLE], 'Boolean')

#Dictionary
DictionaryLength   = standard_method_call(DICTIONARY_EXAMPLE, 'length', [], 'Int')
DictionaryContains = standard_method_call(DICTIONARY_EXAMPLE, 'contains?', [STRING_EXAMPLE], 'Boolean')
DictionaryKeys     = standard_method_call(DICTIONARY_EXAMPLE, 'keys', [], ['List', DICTIONARY_EXAMPLE_KEY_TYPE])
DictionaryValues   = standard_method_call(DICTIONARY_EXAMPLE, 'values', [], ['List', DICTIONARY_EXAMPLE_VALUE_TYPE])

#Set
SetLength          = standard_method_call(SET_EXAMPLE, 'length', [], 'Int')
SetContains        = standard_method_call(SET_EXAMPLE, 'contains?', [STRING_EXAMPLE], 'Boolean')
SetUnion           = standard_method_call(SET_EXAMPLE, 'union', [SET_EXAMPLE], SET_EXAMPLE_TYPE)
SetIntersection    = standard_method_call(SET_EXAMPLE, 'intersection', [SET_EXAMPLE], SET_EXAMPLE_TYPE)

TupleLength        = standard_method_call(TUPLE_EXAMPLE, 'length', [], 'Int')

ArrayLength        = standard_method_call(ARRAY_EXAMPLE, 'length', [], 'Int')

#String
StringSubstr       = standard_method_call(STRING_EXAMPLE, 'substr', [to_node(1), to_node(-1)], 'String')
StringSubstrFrom   = standard_method_call(STRING_EXAMPLE, 'substr_from', [to_node(2)], 'String')
StringSubstrTo     = standard_method_call(STRING_EXAMPLE, 'substr_to', [to_node(-2)], 'String')
StringLength       = standard_method_call(STRING_EXAMPLE, 'length', [], 'Int')
StringFind         = standard_method_call(STRING_EXAMPLE, 'find', [OTHER_STRING_EXAMPLE], 'Int')
StringFindFrom     = standard_method_call(STRING_EXAMPLE, 'find_from', [OTHER_STRING_EXAMPLE, INT_EXAMPLE], 'Int')
StringCount        = standard_method_call(STRING_EXAMPLE, 'count', [OTHER_STRING_EXAMPLE], 'Int')
StringConcat       = standard_method_call(STRING_EXAMPLE, 'concat', [OTHER_STRING_EXAMPLE], 'String')
StringPartition    = standard_method_call(STRING_EXAMPLE, 'partition', [OTHER_STRING_EXAMPLE], ['Tuple', 'String', 'String', 'String'])
StringSplit        = standard_method_call(STRING_EXAMPLE, 'split', [OTHER_STRING_EXAMPLE], ['List', 'String'])
StringTrim         = standard_method_call(STRING_EXAMPLE, 'trim', [], 'String')
StringReversed     = standard_method_call(STRING_EXAMPLE, 'reversed', [], 'String')
StringCenter       = standard_method_call(STRING_EXAMPLE, 'center', [local('z', 'Int'), OTHER_STRING_EXAMPLE], 'String')
StringPresent      = standard_method_call(STRING_EXAMPLE, 'present?', [], 'Boolean')
StringEmpty        = standard_method_call(STRING_EXAMPLE, 'empty?', [], 'Boolean')
StringContains     = standard_method_call(STRING_EXAMPLE, 'contains?', [OTHER_STRING_EXAMPLE], 'Boolean')
StringToInt        = standard_method_call(STRING_EXAMPLE, 'to_int', [], 'Int')
StringPadLeft      = standard_method_call(STRING_EXAMPLE, 'pad_left', [to_node(0), OTHER_STRING_EXAMPLE], 'String')
StringPadRight     = standard_method_call(STRING_EXAMPLE, 'pad_right', [to_node(0), OTHER_STRING_EXAMPLE], 'String')
#Regexp
RegexpMatch           = standard_method_call(REGEXP_EXAMPLE, 'match', [STRING_EXAMPLE], 'RegexpMatch')

#RegexpMatch
RegexpMatchGroup      = standard_method_call(REGEXP_MATCH_EXAMPLE, 'group', [to_node(2)], 'String')
RegexpMatchHasMatch   = standard_method_call(REGEXP_MATCH_EXAMPLE, 'has_match', [], 'Boolean')

BinaryOp = [Node('binary_op', op='+', left=local('ham', pseudo_type='Int'), right=local('egg', pseudo_type='Int'))]
UnaryOp = [Node('unary_op', op='-', value=local('a', 'Int'))]
Comparison = [Node('comparison', op='>', left=local('egg', 'Float'), right=local('ham', 'Float'))]
Interpolation = [Node('interpolation', args=[Node('interpolation_literal', 
            value='',
            pseudo_type='String'),
        Node('interpolation_placeholder',
            value=STRING_EXAMPLE,
            index=0,
            pseudo_type='String'),
        Node('interpolation_literal',
            value='la',
            pseudo_type='String'), 
        Node('interpolation_placeholder',
            value=to_node(4),
            index=1,
            pseudo_type='Int')], pseudo_type='String')]


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
                message='slice_to',
                args=[to_node(2)],
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
            left=call(local('f', ['Function', 'Int']), [], pseudo_type='Int')),
        block=[
            Node('assignment', target=local('b', pseudo_type='Int'), value=call(local('g'), [], pseudo_type='Int'))
        ])]


FunctionDefinition = [Node('function_definition', 
        name='weird',
        params=[Node('local', name='z', pseudo_type='Int')],
        pseudo_type=['Function', 'Int', 'Int'],
        return_type='Int',
        block=[
            assignment(
                local('fixed', pseudo_type='Int'), 
                call(local('fix', pseudo_type=['Function', 'Int', 'Int']), 
                     [local('z', 'Int')], pseudo_type='Int')),
            Node('implicit_return', value=Node('local', name='fixed'))
        ])]

MethodDefinition = [Node('method_definition', 
        name='parse',
        params=[Node('local', name='source', pseudo_type='String')],
        this=Node('typename', name='A'),
        pseudo_type=['Function', 'String', ['List', 'String']],
        return_type=['List', 'String'],
        is_public=True,
        block=[
            assignment(
                Node('instance_variable', name='ast', pseudo_type='Int'), 
                to_node(0)),
            Node('implicit_return', value=Node('list', elements=[Node('local', name='source')], pseudo_type=['List', 'String']))
        ])]

ClassWithMethodDefinition = [
    Node('class_definition',
        name='A',
        constructor=None,
        base=None,
        attrs=[Node('class_attr', name='ast', is_public=False, pseudo_type='Int')],
        methods=MethodDefinition)
]

AnonymousFunction = [
    Node('anonymous_function', 
        params=[Node('local', name='source', pseudo_type='String')],
        pseudo_type=['Function', 'String', 'String'],
        return_type=['List', 'String'],
        block=[
            Node('implicit_return', value=call(local('ves'), [
                Node('standard_method_call', 
                    receiver=Node('local', name='source', pseudo_type='String'),
                    message='length',
                    args=[])]))
        ]),

    Node('anonymous_function', 
        params=[Node('local', name='source', pseudo_type='String')],
        pseudo_type=['Function', 'String', 'String'],
        return_type=['List', 'String'],
        block=[
            Node('standard_call', namespace='io', function='display', args=[Node('local', name='source', pseudo_type='String')], pseudo_type='Void'),
            Node('implicit_return', value=call(local('ves'), [
                Node('standard_method_call', 
                    receiver=Node('local', name='source', pseudo_type='String'),
                    message='length',
                    args=[])]))])
]

ClassDefinition = [Node('class_definition', 
        name='A',
        base='X',
        constructor=Node('constructor',
            params=[Node('local', name='a', pseudo_type='Int')],
            this=typename('A'),
            pseudo_type=['Function', 'Int', 'A'],
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
                this=typename('A'),
                pseudo_type=['Function', 'Int'],
                return_type='Int',
                is_public=False,
                block=[
                    Node('implicit_return', value=to_node(42))
                ])
        ])]

This = [Node('this', pseudo_type='A')]

Constructor = [Node('constructor',
            params=[
                local('a', 'Int'),
                local('b', 'Int')
            ],
            this=typename('A'),
            pseudo_type=['Function', 'Int', 'Int', 'A'],
            return_type='A',
            block=[
                assignment(Node('instance_variable', name='a', pseudo_type='Int'), local('a', 'Int')),
                assignment(Node('instance_variable', name='b', pseudo_type='Int'), local('b', 'Int'))
            ])]

ClassConstructor = [Node('class_definition',
    name='A',
    constructor=Constructor[0],
    base=None,
    attrs=[
        Node('class_attr', is_public=False, name='a', pseudo_type='Int'), 
        Node('class_attr', is_public=False, name='b', pseudo_type='Int')],
    methods=[])]

Index = [Node('index', sequence=to_node('la'), pseudo_type='String', index=to_node(2))]

NegIndex = [Node('index', sequence=to_node('la'), pseudo_type='String', index=to_node(-2))]

Regex = [Node('regex', value='[a-b]', pseudo_type='Regexp')]

Tuple = [Node('tuple', elements=[to_node(2), to_node(42.2)], pseudo_type=['Tuple', 'Int', 'Float'])]

Set = [Node('set', elements=[to_node(2)], pseudo_type=['Set', 'Int'])]

Array = [Node('array', elements=[to_node(2), to_node(4)], pseudo_type=['Array', 'Int', 2])]

u0 = \
Node('try_statement', block=[
        call(local('a', ['Function', 'Int']), [], pseudo_type='Int'),
        call(local('h', ['Function', 'Int', 'Int']), [to_node(-4)], pseudo_type='Int')
    ], handlers=[
        Node('exception_handler',
            exception=None,
            is_builtin=True,
            instance='e',
            block=[
                Node('standard_call', namespace='io', function='display', args=[local('e', 'Exception')], pseudo_type='Void')
            ])
    ])


CppNewInstance = [
    assignment(
        local('z', 'Z'),
        Node('new_instance', class_name=typename('Z'), args=[], pseudo_type='Z'))
]

CppPointerMethodCall = [
    method_call(
        local('z', 'Z'),
        'rave',
        [to_node(0)],
        pseudo_type='Int')]

u = Node('try_statement', block=[
    call(local('a', ['Function', 'Int']), [], pseudo_type='Int'),
    call(local('h', ['Function', 'Int', 'Int']), [to_node(-4)], pseudo_type='Int')
], handlers=[
        Node('exception_handler',
            exception='NeptunError',
            is_builtin = False,
            instance='e',
            block=[
                Node('standard_call', namespace='io', function='display', args=[local('e', 'NeptunError')], pseudo_type='Void')
            ])
    ])

u2 = Node('custom_exception',
           name='NeptunError',
           base=None)

TryStatement = [
    u0,

    ('custom_exceptions', [u2], u)
]

ThrowStatement = [('custom_exceptions', [u2], 
        Node('throw_statement',
          exception='NeptunError',
          value=to_node('no tea')))]

# GoErrorHandling = [
    
class TestHelpers:
    def gen(self, custom_exceptions, ast):
        return generate(Node('module', 
            definitions=[],
            dependencies=[],
            constants=[],
            custom_exceptions=custom_exceptions,
            main=ast if isinstance(ast, list) else [ast]), self._language).rstrip()

    def gen_with_imports(self, custom_exceptions, ast):
        if isinstance(ast, Node):
            if ast.type == 'block':
                e = ast.block
            else:
                e = [ast]
        elif isinstance(ast, list):
            e = ast
        else:
            e = [ast]
        definitions, main = [], []
        for node in e:
            if node.type.endswith('_definition'):
                definitions.append(node)
            else:
                main.append(node)

        result = generate(Node('module', definitions=definitions, custom_exceptions=custom_exceptions, dependencies=[], constants=[], main=main), self._language)
        if hasattr(self, 'gen_special'):
            # input(result)
        
            return self.gen_special(result)

        ls = result.split('\n')
        l = 0
        imports = []
        while ls[l].startswith(self._import):
            imports.append(self._parse_import(ls[l]).strip())
            l += 1
        if not ls[l].strip():
            l += 1
        source = '\n'.join(ls[l:])
        if not hasattr(self, '_no_strip'):
            source = source.strip()
        if hasattr(self, '_ignore_import'):
            imports.remove(self._ignore_import)
        return imports, source

