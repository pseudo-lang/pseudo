import unittest
import textwrap
from pseudon import generate
from pseudon.pseudon_tree import Node
import pseudon.tests.suite as suite

#v
class TestRuby(unittest.TestCase, metaclass=suite.TestLanguage): # dark magic bitches
    def gen(ast):
        return generate(ast, 'ruby')[:-1] #without last \n

    def gen_with_imports(ast):
        result = generate(Node('module', main=[ast]))[:-1]
        ls = result.split('\n')
        l = 0
        imports = []
        while ls[l].startswith('require'):
            imports.append(ls[l][9:-1])
            l += 1
        if not ls[l].strip():
            l += 1
        source = '\n'.join(ls[l:])
        return imports, source

    # make declarative style great again

    # expected ruby translation for each example in suite:

    module = ''

    int_ = '42'

    float_ = '42.42'

    string = "'la'"

    boolean = 'true'

    null = 'nil'

    dictionary = "{la: 0}"

    list_ = "['la']"

    local = 'egg'

    typename = 'Egg'

    instance_variable = '@egg'

    attr = 'e.egg'

    local_assignment = 'egg = ham'

    instance_assignment = '@egg = ham'

    attr_assignment = 'T.egg = ham'

    call = 'map(x)'

    method_call = 'e.filter(42)'

    standard_call = [
        'puts 42',
        'gets',
        'Math.log(ham)',
        "File.read('f.py')"
    ]

    standard_method_call = [
        'l.length',
        "'l'[0...2]"
    ]

    binary_op = 'ham + egg'

    unary_op = '-a'

    comparison = 'egg > ham'

    if_statement = textwrap.dedent('''\
        if egg == ham
          l[0...2]
        elsif egg == ham
          4.2
        else
          z
        end''')

    for_each_statement = textwrap.dedent('''\
        sequence.each do |a|
          a.sub
        end''')

    for_range = textwrap.dedent('''\
        (0...42).step(2).each do |j|
          analyze(j)
        end''')

    for_each_with_index = [
        textwrap.dedent('''\
          z.each_with_index do |k, j|
            analyze(j, k)
          end'''),

        textwrap.dedent('''\
          z.each do |j, k|
            analyze(j, k)
          end''')
    ]

    for_each_in_zip = textwrap.dedent('''\
        z.zip(zz).each do |k, l|
          a(k, l)
        end''')

    while_statement = textwrap.dedent('''\
        while f() >= 42
          b = g
        end''')

    function_definition = textwrap.dedent('''\
        def weird(z)
          fixed = fix(z)
          fixed
        end''')

    method_definition = textwrap.dedent('''\
        def parse(source):
          @ast = None
          [source]
        end''')

    anonymous_function = [
        '-> source { ves(source.length) }',

        textwrap.dedent('''\
            -> source do
              puts source
              ves(source)
            end''')
    ]

    class_statement = [textwrap.dedent('''\
        class A < B
          def initialize(a)
            @a = a
          end

          def parse
            42
          end
        end''')]

    this = 'self'

    constructor = textwrap.dedent('''\
        def initialize(a, b):
          @a = a
          @b = b
        end''')

    try_statement = [
        textwrap.dedent('''\
            begin
              a
              h(2)
            rescue StandardError => e
              puts e
            end'''),

        textwrap.dedent('''\
            class NeptunError < StandardError
            end

            begin
              a
              h(2)
            resuce NeptunError => e
              echo e
            end''')
    ]

    throw_statement = textwrap.dedent('''\
        class NeptunError < StandardError
        end

        raise NeptunError, \'no tea\'''')



