import unittest
import textwrap
from pseudo import generate
from pseudo.pseudo_tree import Node
import suite

#v
class TestJavascript(unittest.TestCase, metaclass=suite.TestLanguage): # dark magic bitches
    def gen(self, custom_exceptions, ast):
        return self.gen_with_imports(custom_exceptions, ast)[1]

    def gen_with_imports(self, custom_exceptions, ast):
        result = generate(Node('module',
            definitions=[],
            dependencies=[],
            custom_exceptions=custom_exceptions,
            constants=[],
            main=ast if isinstance(ast, list) else [ast]), self._language).rstrip()
        l = 0
        lines = result.split('\n')
        imports = []
        while l < len(lines) and lines[l].startswith("var ") and 'require' in lines[l]:
            require_index = lines[l].index('require')
            imports.append(lines[l][require_index + 9:-3])
            l += 1
        source = lines[l:]

        if len(source) == 1 and source[0][-1] == ';':
            return imports, source[0][:-1]
        else:
            return imports, '\n'.join(source).strip()


    _language = 'javascript'

    # make declarative style great again

    # expected javascript translation for each example in suite:

    int_ = '42'

    float_ = '42.42'

    string = "'la'"

    boolean = 'true'

    null = 'null'

    dictionary = '{la: 0}'

    neg_index = "'la'['la'.length - 2]"

    list_ = "['la']"

    local = 'egg'

    typename = 'Egg'

    instance_variable = 'this.egg'

    attr = 'e.egg'

    assignments = [
        'egg = ham',
        'this.egg = ham',
        'T.egg = ham',
        "x[4] = 'String'"
    ]

    call = 'map(x)'

    method_call = 'e.filter(42)'

    standard_call = [
        'console.log(42)'
    ]

    standard_method_call = [
        'l.length',
        "'l'.slice(0, 2)"
    ]

    # io
    io_display          = "console.log(2, 'z')"
    io_read_file        = (['fs'], "var source = fs.readFileSync('z.py', 'utf8')")
    io_write_file       = (['fs'], "fs.writeFileSync('z.py', source, 'utf8')")

    # math
    math_ln             = 'Math.log(z)'
    math_log            = 'Math.log(z, 2.0)'
    math_tan            = 'Math.tan(z)'
    math_sin            = 'Math.sin(z)'
    math_cos            = 'Math.cos(z)'

    # regexp
    regexp_compile      = 'new RegExp(s)'
    regexp_escape       = (['lodash'], '_.escapeRegExp(s)')

    # # List
    list_push       = "cpus.push('')"
    list_pop        = 'cpus.pop()'
    list_length     = 'cpus.length'
    list_map        = textwrap.dedent('''\
                        _.map(cpus, function (value) {
                          return value + 'a';
                        });''')

    list_remove     = '_.pull(cpus, s)'
    list_remove_at  = 'cpus.splice(0, 1)'
    list_slice      = 'cpus.slice(2, -1)'
    list_slice_from = 'cpus.slice(2)'
    list_slice_to   = 'cpus.slice(0, 2)'
    list_filter     = textwrap.dedent('''\
                        _.filter(cpus, function (value) {
                          return value.length == 0;
                        });''')
    list_reduce     = textwrap.dedent('''\
                        _.reduce(cpus, function (value, other) {
                          var result = value + other;
                          return result;
                        }, '');''')
    list_any        = textwrap.dedent('''\
                        _.any(cpus, function (value) {
                          return value.length == 0;
                        });''')
    list_all        = textwrap.dedent('''\
                        _.all(cpus, function (value) {
                          return value.length == 0;
                        });''')
    list_find       = 'cpus.indexOf(s)'
    list_present    = 'cpus.length > 0'
    list_empty      = 'cpus.length == 0'
    list_contains   = '_.contains(cpus, s)'
    list_sort       = 'cpus.sort()'

    # # Hash
    dictionary_length   = 'Object.keys(pointers).length'
    dictionary_contains = 'pointers.hasOwnProperty(s)'
    dictionary_keys     = 'Object.keys(pointers)'
    dictionary_values   = 'Object.values(pointers)'

    # Set
    set_length          = 'Object.keys(words).length'
    set_contains        = '_.contains(words, s)'
    set_union           = '_.union(words, words)'
    set_intersection    = '_.intersection(words, words)'

    # Tuple
    tuple_length        = 'flowers.length'

    # Array
    array_length        = 'cars.length'

    # String
    string_substr       = 's.slice(1, -1)'
    string_substr_from  = 's.slice(2)'
    string_substr_to    = 's.slice(0, -2)'
    string_length       = 's.length'
    string_find         = 's.search(t)'
    string_find_from    = 'z + s.slice(z).search(t)'
    string_count        = '_.where(t).length'
    string_concat       = 's + t'
    string_partition    = '_.partition(t)[1]'
    string_split        = 's.split(t)'
    string_trim         = 's.trim()'
    string_reversed     = "s.split('').reverse().join('')"
    string_center       = '_.pad(s, z, t)'
    string_present      = 's'
    string_empty        = '!s'
    string_contains     = '_.contains(s, t)'
    string_to_int       = 'parseInt(s)'
    string_pad_left     = '_.padLeft(s, 0, t)'
    string_pad_right    = '_.padRight(s, 0, t)'

    
    # Regexp
    regexp_match        = 'r.exec(s)'
                            # hes = [r.exec(s)];
                            # while (_matches[_matches.length - 1] != null) {
                            #     _matches.push(r.exec(s));
                            # }
                            # _matches.pop()''')

    # RegexpMatch   # result of s.scan is an array, fix regex in next versions
    regexp_match_group  = 'm[3]'
    regexp_match_has_match = 'm'    

    binary_op = 'ham + egg'

    unary_op = '-a'

    standard_math = 'Math.sin(ham)'

    comparison = 'egg > ham'

    if_statement = textwrap.dedent('''\
        if (egg == ham) {
          l.slice(0, 2);
        } else if (egg == ham) {
          console.log(4.2);
        } else {
          z;
        }''')

    for_statement = [
        textwrap.dedent('''\
            _.forEach(sequence, function (a) {
              log(a);
            });'''),

        textwrap.dedent('''\
            for(var j = 0;j != 42;j += 2) {
              analyze(j);
            }'''),

        textwrap.dedent('''\
            _.forEach(z, function (k, j) {
              analyze(j, k);
            });'''),

        textwrap.dedent('''\
            _.forEach(z, function (k, j) {
              analyze(k, j);
            });'''),

        textwrap.dedent('''\
            _.forEach(_.zip(z, zz), function (k, l) {
              a(k, l);
            });''')
    ]

    while_statement = textwrap.dedent('''\
        while (f() >= 42) {
          var b = g();
        }''')

    function_definition = textwrap.dedent('''\
        function weird(z) {
          var fixed = fix(z);
          return fixed;
        }''')

    method_definition = textwrap.dedent('''\
        A.prototype.parse = function (source) {
          this.ast = 0;
          return [source];
        }''')

    anonymous_function = [
        textwrap.dedent('''\
            function (source) {
              return ves(source.length);
            }'''),

        textwrap.dedent('''\
            function (source) {
              console.log(source);
              return ves(source.length);
            }''')
    ]

    class_statement = [textwrap.dedent('''\
        function A(a) {
          this.a = a;
        }

        A.prototype = _.create(X.prototype, {constructor: A});

        A.prototype.parse = function () {
          return 42;
        }''')]

    this = 'this'

    constructor = textwrap.dedent('''\
        function A(a, b) {
          this.a = a;
          this.b = b;
        }''')

    try_statement = [
        textwrap.dedent('''\
            try {
              a();
              h(-4);
            } catch(e) {
              if (e isinstanceof Error) {
                console.log(e);
              } else {
                throw e;
              }
            }'''), # yes obvsly its an Error, but we'll have other builtin errors in next versions

        textwrap.dedent('''\
            function NeptunError(message) {
              this.message = message;
            }

            NeptunError.prototype = _.create(Error.prototype, {constructor: NeptunError});

            try {
              a();
              h(-4);
            } catch(e) {
              if (e isinstanceof NeptunError) {
                console.log(e);
              } else {
                throw e;
              }
            }''')
    ]

    throw_statement = textwrap.dedent('''\
        function NeptunError(message) {
          this.message = message;
        }

        NeptunError.prototype = _.create(Error.prototype, {constructor: NeptunError});

        throw new NeptunError('no tea');''')
