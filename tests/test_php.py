import unittest
import textwrap
from pseudon import generate
from pseudon.pseudon_tree import Node
import pseudon.tests.suite as suite

#v
class TestPHP(unittest.TestCase, metaclass=suite.TestLanguage): # dark magic bitches
    def gen(ast):
        return generate(ast, 'php')[:-1] #without last \n

    def gen_with_imports(ast):
        result = generate(Node('module', main=[ast]))[:-1]
        ls = result.split('\n')[1:] # without <?php
        l = 0
        imports = []
        while ls[l].startswith('require_once'):
            imports.append(ls[l][14:-3]) # without req(' ')
            l += 1
        if not ls[l].strip():
            l += 1
        source = '\n'.join(ls[l:])
        return imports, source

    # make declarative style great again

    # expected php translation for each example in suite:

    module = ''

    int_ = '42'

    float_ = '42.42'

    string = '"la"'

    boolean = 'true'

    null = 'NULL'

    dictionary = "['la' => 0]"

    list_ = "['la']"

    local = '$egg'

    typename = 'Egg'

    instance_variable = '$this->egg'

    attr = '$e->egg'

    local_assignment = '$egg = $ham'

    instance_assignment = '$this->egg = $ham'

    attr_assignment = 'T->egg = $ham'

    call = 'map($x)'

    method_call = '$e->filter(42)'

    standard_call = [
        'echo 42',
        'fgets(STDIN)',
        'log(ham)',
        "file_get_contents('f.py')"
    ]

    standard_method_call = [
        'array_length(l)',
        "substr('l', 0, 2)"
    ]

    binary_op = 'ham + egg'

    unary_op = '-a'

    comparison = 'egg > ham'

    if_statement = textwrap.dedent('''\
        if ($egg == $ham) {
          l[0...2];
        }
        elseif ($egg == $ham) {
          4.2;
        }
        else {
          $z
        }''')

    for_each_statement = textwrap.dedent('''\
        foreach($sequence as $a) {
          $a->sub();
        }''')

    for_range = textwrap.dedent('''\
        for($j = 0;$j < 42;$j += 2) {
          analyze($j);
        }''')

    for_each_with_index = [
        textwrap.dedent('''\
          foreach($z as $j => $k) {
            analyze($j, $k);
          }'''),

        textwrap.dedent('''\
          foreach($z as $j => $k) {
            analyze($j, $k);
          }''')
    ]

    for_each_in_zip = textwrap.dedent('''\
        foreach(array_combine($z, $zz) as $k => $l) {
          a($k, $l);
        }''')

    while_statement = textwrap.dedent('''\
        while (f() >= 42) {
          $b = g();
        }''')

    function_definition = textwrap.dedent('''\
        function weird($z) {
          $fixed = fix($z);
          return $fixed;
        }''')

    method_definition = textwrap.dedent('''\
        function parse($source) {
          $this->ast = NULL;
          return [$source];
        }''')

    anonymous_function = [
        'function($source) { return ves(array_length($source)); }',

        textwrap.dedent('''\
            function($source) {
              echo $source;
              return ves($source);
            }''')
    ]

    class_statement = [textwrap.dedent('''\
        class A extends B {
          public $a;
          
          function __construct($a) {
            $this->a = $a;
          }

          public function parse() {
            return 42;
          }
        }''')]

    this = '$this'

    constructor = textwrap.dedent('''\
        function __construct($a, $b) {
          $this->a = $a;
          $this->$b = $b;
        }''')
