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

    # io
    io_display          = "puts 2, 'z'"
    io_read             = 'source = gets'
    io_read_file        = "source = File.read('z.py')"
    io_write_file       = "File.write('z.py', source)"

    # math
    math_ln             = 'Math.log(z)'
    math_log            = 'Math.log(z, 2.0)'
    math_tan            = 'Math.tan(z)'
    math_sin            = 'Math.sin(z)'
    math_cos            = 'Math.cos(z)'

    # regexp
    regexp_compile      = '/#{s}/'
    regexp_escape       = 'Regexp.escape(s)'


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
    list_any        = 'cpus.any? { |value| value.length == 0 }'
    list_all        = 'cpus.all? { |value| value.length == 0 }'
    list_find       = 'cpus.index(s)'
    list_present    = '!cpus.empty?'
    list_empty      = 'cpus.empty?'
    list_contains   = 'cpus.include?(s)'
    list_sort       = 'cpus.sort!'

    # Hash
    dictionary_length   = 'pointers.length'
    dictionary_contains = 'pointers.include?(s)'
    dictionary_keys     = 'pointers.keys'
    dictionary_values   = 'pointers.values'

    # Set
    set_length          = 'words.length'
    set_contains        = 'words.include?(s)'
    set_union           = 'words | words'
    set_intersection    = 'words.intersection(words)'

    # Tuple
    tuple_length        = 'flowers.length'

    # Array
    array_length        = 'cars.length'

    # String
    string_substr       = 's[1...-1]'
    string_substr_from  = 's[2..-1]'
    string_substr_to    = 's[0...-2]'
    string_length       = 's.length'
    string_find         = 's.index(t)'
    string_find_from    = 's.index(t, z)'
    string_count        = 's.count(t)'
    string_concat       = 's + t'
    string_partition    = 's.partition(t)'
    string_split        = 's.split(t)'
    string_trim         = 's.trim'
    string_reversed     = 's.reverse'
    string_center       = 's.center(z, t)'
    string_present      = '!s.empty?'
    string_empty        = 's.empty?'
    string_contains     = 's.include?(t)'
    string_to_int       = 's.to_i'
    string_pad_left     = 's.ljust(0, t)'
    string_pad_right    = 's.rjust(0, t)'

    # Regexp
    regexp_match        = 's.scan(r)'

    # RegexpMatch   # result of s.scan is an array, fix regex in next versions
    regexp_match_group  = 'm[2][0]'
    regexp_match_has_match = '!m.empty?'

    binary_op = 'ham + egg'

    unary_op = '-a'

    comparison = 'egg > ham'

    interpolation = '"#{s}la#{4}"'

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



