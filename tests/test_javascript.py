import unittest
import textwrap
from pseudon import generate
from pseudon.pseudon_tree import Node
import pseudon.tests.suite as suite

#v
class TestJavascript(unittest.TestCase, metaclass=suite.TestLanguage): # dark magic bitches
    def gen(ast):
        return generate(ast, 'javascript')[:-1] #without last \n

    # make declarative style great again

    # expected javascript translation for each example in suite:

    module = ''

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

    local_assignment = 'egg = ham'

    instance_assignment = 'this.egg = ham'

    attr_assignment = 'T.egg = ham'

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

    for_each_statement = textwrap.dedent('''\
        _.forEach(sequence, function(a) {
            a.sub();
        })''')

    for_range = textwrap.dedent('''\
        for(var j = 0;j < 42;j += 2) {
          analyze(j);
        }''')

    for_each_with_index = [
        textwrap.dedent('''\
          _.forEach(z, function(k, j) {
            analyze(j, k);
          })'''),

        textwrap.dedent('''\
          _.forEach(z, function(j, k) {
            analyze(j, k);
          })''')
    ]

    for_each_in_zip = textwrap.dedent('''\
        _.zip(z, zz).forEach(function(k, l) {
          a(k, l);
        }''')

    while_statement = textwrap.dedent('''\
        while (f() >= 42) {
          b = g();
        }''')

    function_definition = textwrap.dedent('''\
        function weird(z) {
          var fixed = fix(z);
          return fixed;
        }''')

    method_definition = textwrap.dedent('''\
        function parse(source) {
          this.ast = null;
          return [source];
        }''')

    anonymous_function = [
        'function(source) { return ves(source.length); }',

        textwrap.dedent('''\
            function(source) {
              console.log(source);
              return ves(source);
            }''')
    ]

    class_statement = [textwrap.dedent('''\
        function A(a) {
          this.a = a;
        }

        A.prototype = _.create(B.prototype, {
          'constructor': A
        });

        A.prototype.parse = function() {
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
                h(2);
            } catch(e) {
                console.log(e);
            }''')

        textwrap.dedent('''\
            function NeptunError(message) {
                this.message = message;
            }
            NeptunError.prototype = new Error;

            try {
                a();
                h(2);
            } catch(e) {
                if (e instanceof NeptunError) {
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
        NeptunError.prototype = new Error;

        throw new NeptunError('no tea')''')
