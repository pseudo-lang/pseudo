import unittest
import textwrap
from pseudon import generate
from pseudon.pseudon_tree import Node
import pseudon.tests.suite as suite

def dedent_with_tabs(source):
    a = textwrap.dedent(source)
    return a.replace('    ', '\t')

#v
class TestGo(unittest.TestCase, metaclass=suite.TestLanguage): # dark magic bitches
    def gen(ast):
        raw = generate(ast, 'go')
        return raw[:-1] # no \n end

    def gen_with_imports(ast):
        raw = generate(Node('module', main=[ast]))[:-1]
        lines = raw.split('\n')
        main = '\n'.join([line[1:] for line in lines[lines.find('func mai') + 1:-1]])
        
        l = 0
        if lines[0].startswith('import'):
            imports = [l.strip()[1:-1] for l in lines[1:lines.index(')')]]
        else:
            imports = []
        source = '\n'.join(main)
        return imports, source

    # make declarative style great again

    # expected c++ translation for each example in suite:

    int_ = '42'

    float_ = '42.42'

    string = '"la"'

    null = 'nil'

    dictionary = dedent_with_tabs('''\
        Map[string]int{
         "la": 0
        }''')

    list_ = '[]string{"la"}'

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
        (['fmt'], 'fmt.Println(42)'),
        (['bufio', 'os'], dedent_with_tabs('''\
            reader := bufio.NewReader(os.Stdin)
            reader.ReadString('\n')'''),
        (['math', 'Math.Log(ham)'),
        (['io/ioutil'], 'ioutil.ReadFile("f.py")')
    ]

    standard_method_call = [
        'len(l)',
        '"l"[0:2]'
    ]

    binary_op = 'ham + egg'

    unary_op = '-a'

    comparison = 'egg > ham'

    if_statement = (
        ['fmt'],
        dedent_with_tabs('''\
            if egg == ham {
                l[0:2]
            } else if egg == ham {
                fmt.Println(4.2)
            } 
            else {
                z
            }'''))
    )


    for_each_statement = dedent_with_tabs('''\
        for _, a := range sequence {
          a.sub()
        }''')
    )

    for_range = textwrap.dedent('''\
        for(int j = 0;j < 42; j += 2) {
          analyze(j);
        }''')

    for_each_with_index = [
        textwrap.dedent('''\
          for(int j = 0;j < z.size();j ++) 
          {
            var k = z[j];
            analyze(j, k);
          }'''),

        (['unordered_map'],
         textwrap.dedent('''\
          foreach(auto _item in z)
          {
            analyze(_item->first, _item->second);
          }'''))
    ]

    for_each_in_zip = textwrap.dedent('''\
        for(var _index = 0;_index < min(z.size(), zz.size()
);_index ++)
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
        int weird(int z)
        {
          int fixed = fix(z);
          return fixed;
        }''')

    method_definition = (
        ['vector', 'string'],
        textwrap.dedent('''\
        vector<string> parse(string source)
        {
          this->ast = Null;
          return vector<string>{ source };
        }'''))

    anonymous_function = [
        (['vector'],
         '[](auto source) { return ves(source.size()); }'),

        textwrap.dedent('''\
            [](auto source) {
                cout << source << "\n";
                return ves(source);
            }''')
    ]

    class_statement = [textwrap.dedent('''\
        class A : B { 
            public int a;

            public:

            A(int a) {
                this->a = a;
            }

            int parse() {
                return 42;
            }''')]

