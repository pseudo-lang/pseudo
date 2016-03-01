import unittest
import textwrap
from pseudon import generate
from pseudon.pseudon_tree import Node
import pseudon.tests.suite as suite

#v
class TestCSharp(unittest.TestCase, metaclass=suite.TestLanguage): # dark magic bitches
    def gen(ast):
        raw = generate(ast, 'csharp')
        return raw[:-1] # no \n end

    def gen_with_imports(ast):
        raw = generate(Node('module', main=[ast]))[:-1]
        lines = raw.split('\n')
        main = '\n'.join([line[12:] for line in lines[lines.find('        static void') + 2:-3]])
        
        l = 0
        imports = []
        while lines[l].startswith('using'):
            imports.append(lines[l][6:-1])
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

    string = '"la"'

    boolean = 'true'

    null = 'null'

    dictionary = 'new Dictionary<String, Int>{ {"la", 0} }'

    list_ = 'new List<string>{ "la" }'

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
        'Console.WriteLine(42)',
        'Console.ReadLine()',
        'Math.Log(ham)',
        "File.read('f.py')"
    ]

    standard_method_call = [
        'l.Count',
        '"l".Substring(0, 2)'
    ]

    binary_op = 'ham + egg'

    unary_op = '-a'

    comparison = 'egg > ham'

    if_statement = textwrap.dedent('''\
        if (egg == ham)
        {
            l.Take(2);
        }
        else if (egg == ham)
        {
            Console.WriteLine(4.2);
        } 
        else 
        {
            z;
        }''')


    for_each_statement = textwrap.dedent('''\
        foreach(var a in sequence) 
        {
          a.Sub();
        }''')

    for_range = textwrap.dedent('''\
        for(var j = 0;j < 42; j += 2)
        {
          Analyze(j);
        }''')

    for_each_with_index = [
        textwrap.dedent('''\
          for(int j = 0;j < z.Count;j ++) 
          {
            var k = z[j];
            Analyze(j, k);
          }'''),

        textwrap.dedent('''\
          foreach(var item in z)
          {
            Analyze(item.key, item.value)
          }''')
    ]

    for_each_in_zip = textwrap.dedent('''\
        for(var _index = 0;_index < Math.min(z.Count, zz.Count);_index ++)
        {
          var k = z[_index];
          var l = zz[_index];
          a(k, l);
        }
        ''')

    while_statement = textwrap.dedent('''\
        while (f() >= 42)
        {
          b = g();
        }''')

    function_definition = textwrap.dedent('''\
        int Weird(int z)
        {
          int fixed = fix(z);
          return fixed;
        }''')

    method_definition = textwrap.dedent('''\
        List<string> Parse(string source)
        {
          ast = Null;
          return List<string>{ source };
        }''')

    anonymous_function = [
        'source => ves(source.length)',

        textwrap.dedent('''\
            source =>
            {
                Console.WriteLine(source);
                return ves(source);
            }''')
    ]

    class_statement = [textwrap.dedent('''\
        public class A : B
        { 
            public int a;

            A(int a)
            {
                this.a = a;
            }

            int Parse()
            {
                return 42;
            }
        }''')]

    this = 'this'

    constructor = textwrap.dedent('''\
        A(int a, string b)
        {
          this.a = a;
          this.b = b;
        }''')
