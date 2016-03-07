import unittest
import textwrap
from pseudo import generate
from pseudo.pseudo_tree import Node
import suite

#v
class TestRuby(unittest.TestCase, metaclass=suite.TestLanguage): # dark magic bitches

    _language = 'ruby'
    _import = 'require'
    _parse_import = lambda self, line: line[9:-1]

    # make declarative style great again

    # expected ruby translation for each example in suite:

    int_ = '42'

    float_ = '42.42'

    string = "'la'"

    boolean = 'true'

    null = 'nil'

    dictionary = "{la: 0}"

    list_ = "['la']"

    local = 'egg'

    set_  = 'Set.new([2])'

    tuple_ = '[2, 42.2]'

    array = '[2, 4]'

    regex = '/[a-b]/'

    typename = 'Egg'

    instance_variable = '@egg'

    attr = 'e.egg'

    assignments = [
        'egg = ham',
        '@egg = ham',
        'T.egg = ham',
        "x[4] = 'String'"
    ]

    call = 'map(x)'

    method_call = 'e.filter(42)'

    standard_call = [
        'puts 42',
        'gets',
        'Math.log(ham)',
        "source = File.read('f.py')"
    ]

    standard_method_call = [
        'l.length',
        "'l'[0...2]",
    ]

    # List
    list_push       = "cpus.push('')"
    list_pop        = 'cpus.pop'
    list_length     = 'cpus.length'
    list_map        = "cpus.map { |value| value + 'a' }"
    list_remove     = "cpus.delete(s)"
    list_remove_at  = "cpus.delete_at(0)"
    list_length     = 'cpus.length'
    list_slice      = 'cpus[2...-1]'
    list_slice_from = 'cpus[2..-1]'
    list_slice_to   = 'cpus[0...2]'
    list_filter     = 'cpus.select { |value| value.length == 0 }'
    list_reduce     = textwrap.dedent('''\
                        cpus.reduce('') do |value, other|
                          result = value + other
                          result
                        end''')

    binary_op = 'ham + egg'

    unary_op = '-a'

    comparison = 'egg > ham'

    if_statement = textwrap.dedent('''\
        if egg == ham
          l[0...2]
        elsif egg == ham
          puts 4.2
        else
          z
        end''')

    for_statement = [
        textwrap.dedent('''\
          sequence.each do |a|
            log(a)
          end'''),

        textwrap.dedent('''\
          (0...42).step(2).each do |j|
            analyze(j)
          end'''),


        textwrap.dedent('''\
          z.each_with_index do |k, j|
            analyze(j, k)
          end'''),

        textwrap.dedent('''\
          z.each do |j, k|
            analyze(k, j)
          end'''),

        textwrap.dedent('''\
          z.zip(zz).each do |k, l|
            a(k, l)
          end''')
    ]

    while_statement = textwrap.dedent('''\
        while f >= 42
          b = g
        end''')

    function_definition = textwrap.dedent('''\
        def weird(z)
          fixed = fix(z)
          fixed
        end''')

    method_definition = textwrap.dedent('''\
        def parse(source)
          @ast = 0
          [source]
        end''')

    anonymous_function = [
        '-> source { ves(source.length) }',

        textwrap.dedent('''\
            -> source do
              puts source
              ves(source.length)
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
        def initialize(a, b)
          @a = a
          @b = b
        end''')

    index = "'la'[2]"

    try_statement = [
        textwrap.dedent('''\
            begin
              a
              h(-4)
            rescue StandardError => e
              puts e
            end'''),

        textwrap.dedent('''\
            class NeptunError < StandardError
            end


            begin
              a
              h(-4)
            rescue NeptunError => e
              puts e
            end''')
    ]

    throw_statement = textwrap.dedent('''\
        class NeptunError < StandardError
        end


        throw NeptunError.new(\'no tea\')''')



