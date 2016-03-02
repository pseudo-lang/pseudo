import unittest
import textwrap
from pseudon import generate
from pseudon.pseudon_tree import Node
import suite

#v
class TestPython(unittest.TestCase, metaclass=suite.TestLanguage): # dark magic bitches
    def gen(self, ast):
        return generate(ast, 'python').rstrip()


    def gen_with_imports(self, ast):
        if isinstance(ast, Node):
            if ast.type == 'block':
                e = ast.block
            else:
                e = [ast]
        else:
            e = ast
        definitions, main = [], []
        for node in e:
            if node.type.endswith('_definition'):
                definitions.append(node)
            else:
                main.append(node)

        result = generate(Node('module', definitions=definitions, main=main), 'python')
        ls = result.split('\n')
        l = 0
        imports = []
        while ls[l].startswith('import'):
            imports.append(ls[l][7:])
            l += 1
        if not ls[l].strip():
            l += 1
        source = '\n'.join(ls[l:])
        return imports, source

    # make declarative style great again

    # expected python translation for each example in suite:

    int_ = '42'

    float_ = '42.42'

    string = "'la'"

    boolean = 'True'

    null = 'None'

    dictionary = "{'la': 0}"

    list_ = "['la']"

    typename = 'Egg'

    instance_variable = 'self.egg'

    attr = 'e.egg'

    local_assignment = 'egg = ham'

    instance_assignment = 'self.egg = ham'

    attr_assignment = 'T.egg = ham'

    call = 'map(x)'

    method_call = 'e.filter(42)'

    standard_call = [
        'print(42)',
        'input()',
        (['math'], 'math.log(ham)\n'),
        textwrap.dedent('''\
            with open('f.py', 'r') as f:
                f.read()''')
    ]

    standard_method_call = [
        'len(l)',
        "'l'[:2]"
    ]

    binary_op = 'ham + egg'

    unary_op = '-a'

    comparison = 'egg > ham'

    if_statement = textwrap.dedent('''\
        if egg == ham:
            l[:2]
        elif egg == ham:
            print(4.2)
        else:
            z''')

    for_each_statement = textwrap.dedent('''\
        for a in sequence:
            a.sub()''')

    for_range_statement = textwrap.dedent('''\
        for j in range(0, 42, 2):
            analyze(j)''')

    for_each_with_index_statement = [
        textwrap.dedent('''\
            for j, k in enumerate(z):
                analyze(j, k)'''),

        textwrap.dedent('''\
            for j, k in z.items():
                analyze(j, k)''')
    ]

    for_each_in_zip_statement = textwrap.dedent('''\
        for k, l in zip(z, zz):
            a(k, l)''')

    while_statement = textwrap.dedent('''\
        while f() >= 42:
            b = g()''')

    function_definition = textwrap.dedent('''\
        def weird(z):
            fixed = fix(z)
            return fixed''')

    method_definition = textwrap.dedent('''\
        def parse(self, source):
            self.ast = None
            return [source]''')

    anonymous_function = [
        'lambda source: ves(len(source))',

        ([], textwrap.dedent('''\
            def a_0(source):
                print(source)
                return ves(len(source))

            

            a_0

            '''))
    ]

    class_definition = [textwrap.dedent('''\
        class A(B):
            def __init__(self, a):
                self.a = a

            def parse(self):
                return 42''')]

    this = 'self'

    constructor = textwrap.dedent('''\
        def __init__(self, a, b):
            self.a = a
            self.b = b''')

    try_statement = [
        textwrap.dedent('''\
            try:
                a()
                h(-4)
            except Exception as e:
                print(e)'''),

        textwrap.dedent('''\
            class NeptunError(Exception):
                pass

            try:
                a()
                h(-4)
            except NeptunError as e:
                print(e)''')
    ]

    throw_statement = textwrap.dedent('''\
        class NeptunError(Exception):
            pass

        throw NeptunError('no tea')''')


