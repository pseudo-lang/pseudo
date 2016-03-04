import unittest
import textwrap
import suite

#v
class TestPython(unittest.TestCase, metaclass=suite.TestLanguage): # dark magic bitches
    
    _language = 'python'
    _import = 'import'
    _parse_import = lambda self, line: line[7:]

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

    assignments = [
        'egg = ham',
        'self.egg = ham',
        'T.egg = ham',
        "x[4] = 'String'"
    ]

    call = 'map(x)'

    method_call = 'e.filter(42)'

    standard_call = [
        'print(42)',
        'input()',
        (['math'], 'math.log(ham)\n'),
        textwrap.dedent('''\
            with open('f.py', 'r') as _f:
                source = _f.read()''')
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

    for_statement = [
        textwrap.dedent('''\
            for a in sequence:
                log(a)'''),

        textwrap.dedent('''\
             for j in range(0, 42, 2):
                 analyze(j)'''),
    

        textwrap.dedent('''\
            for j, k in enumerate(z):
                analyze(j, k)'''),

        textwrap.dedent('''\
            for j, k in z.items():
                analyze(k, j)'''),
    
        textwrap.dedent('''\
            for k, l in zip(z, zz):
                a(k, l)''')
    ]

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
        class A(X):
            def __init__(self, a):
                self.a = a

            def parse(self):
                return 42''')]

    this = 'self'

    constructor = textwrap.dedent('''\
        def __init__(self, a, b):
            self.a = a
            self.b = b''')

    index = "'la'[2]"

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

        raise NeptunError('no tea')''')


