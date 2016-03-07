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

    set_  = '{2}'

    tuple_ = '(2, 42.2)'

    array = '(2, 4)'

    regex = "re.compile(r'[a-b]')"

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
        "'l'[:2]",
    ]

    #List
    list_push           = "cpus.append('')"
    list_pop            = "cpus.pop()"
    list_length         = "len(cpus)"
    list_map            = "[value + 'a' for value in cpus]"
    list_remove         = 'cpus.remove(s)'
    list_remove_at      = 'del cpus[0]'
    list_length         = 'len(cpus)'
    list_slice          = 'cpus[2:-1]'
    list_slice_from     = 'cpus[2:]'
    list_slice_to       = 'cpus[:2]'
    list_filter         = '[value for value in cpus if len(value) == 0]'
    list_reduce         = (['functools'], textwrap.dedent('''\
                            
                            def a_0(value, other):
                                result = value + other
                                return result



                            functools.reduce(a_0, '')

                            '''))
    list_any            = 'any(len(value) == 0 for value in cpus)'
    list_all            = 'all(len(value) == 0 for value in cpus)'

    #Dict
    dictionary_length   = 'len(pointers)'
    dictionary_contains = "s in pointers"
    dictionary_keys     = 'list(pointers.keys())'  # list for compatibillity with pseudo api
    dictionary_values   = 'list(pointers.values())'

    #Set
    set_length          = 'len(words)'
    set_contains        = 's in words'
    set_union           = 'words | words'
    set_intersection    = 'words - words'

    #Tuple
    tuple_length        = 'len(flowers)'

    #Array
    array_length        = 'len(cars)'


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
            self.ast = 0
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


