import unittest
import textwrap
from pseudon import generate
from pseudon.pseudon_tree import Node
import suite

#v
class TestJavascript(unittest.TestCase, metaclass=suite.TestLanguage): # dark magic bitches
    def gen(self, ast):
        return self.gen_with_imports(ast)[1]

    def gen_with_imports(self, ast):
        result = generate(Node('module',
            definitions=[],
            dependencies=[],
            constants=[],
            main=ast if isinstance(ast, list) else [ast]), self._language).rstrip()
        if result.startswith("var _ = require('lodash')"):
            lines = result.split('\n')
            imports, source = ['lodash'], lines[2:]
        else:
            imports, source = [], result.split('\n')

        if len(source) == 1 and source[0][-1] == ';':
            return imports, source[0][:-1]
        else:
            return imports, '\n'.join(source).rstrip()


    _language = 'javascript'

    # make declarative style great again

    # expected javascript translation for each example in suite:

    int_ = '42'

    float_ = '42.42'

    string = "'la'"

    boolean = 'true'

    null = 'null'

    dictionary = '{la: 0}'

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
        'console.log(42)',
        'console.read()'
    ]

    standard_method_call = [
        'l.length',
        "'l'.slice(0, 2)"
    ]

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
          this.ast = null;
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
