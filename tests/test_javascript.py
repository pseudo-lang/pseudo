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
        'l.slice(0, 2)'
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
        _.each(sequence, function(a) {
            a.sub();
        }''')



