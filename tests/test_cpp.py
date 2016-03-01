import unittest
import textwrap
from pseudon import generate
from pseudon.pseudon_tree import Node
import pseudon.tests.suite as suite

#v
class TestCpp(unittest.TestCase, metaclass=suite.TestLanguage): # dark magic bitches
    def gen(ast):
        raw = generate(ast, 'cpp')
        return raw[:-1] # no \n end

    def gen_with_imports(ast):
        raw = generate(Node('module', main=[ast]))[:-1]
        lines = raw.split('\n')
        main = '\n'.join([line[4:] for line in lines[lines.find('    int main') + 1:-1]])
        
        l = 0
        imports = []
        while lines[l].startswith('#include'):
            imports.append(lines[l][9:-1])
            l += 1
        source = '\n'.join(main)
        return imports, source

    # make declarative style great again

    # expected c++ translation for each example in suite:

    int_ = '42'

    float_ = '42.42'

    string = '"la"'

    null = 'NULL'

    dictionary = (
        ['iostream', 'unordered_map'],
        'unordered_map<string, int>{ { "la", 0 } };'
    )

    list_ = (
        ['iostream', 'vector'],
        'vector<string>{ "la" };'
    )

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
        (['iostream'], 'string _result;cin << _result'),
        (['math', 'log(ham)'),
        (['fstream', 'string'], 'ifstream ifs("f.py");\nstring _result((istreambuf_iterator<char>(ifs)), (istreambuf_iterator<char>()));')
    ]

    standard_method_call = [
        'l.size()',
        '"l".substr(0, 2)'
    ]

    binary_op = 'ham + egg'

    unary_op = '-a'

    comparison = 'egg > ham'

    if_statement = (
        ['vector'],
        textwrap.dedent('''\
            if (egg == ham) {
                l.sublist(l.begin(), l.begin() + 2);
            } 
            else if (egg == ham) {
                cout << 4.2 << "\n";
            } 
            else {
                z;
            }''')
    )


    for_each_statement = (
        ['vector'],
        textwrap.dedent('''\
        for(auto a = sequence.begin(); a != sequence.end(); a++) {
          a->sub();
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

    this = 'this'

    constructor = (
        ['string'],
        textwrap.dedent('''\
            A(int a, string b) {
                this.a = a;
                this.b = b;
            }'''))

    try_statement = [
        (['stdexcept', 'exception'], 
         textwrap.dedent('''\
            try {
              a();
              h(2);
            } catch (exception& e) {
              cout << e.what() << "\n";
            }''')),

        (['stdexcept', 'exception'], 
         textwrap.dedent('''\
            class NeptunError : runtime_error {
            }

            try {
              a();
              h(2);
            } catch (NeptunError& e) {
              cout << e.what() << "\n";
            }'''))
    ]

    throw_statement = (['stdexcept', 'exception'], 
        textwrap.dedent('''\
        class NeptunError extends runtime_error {
        }

        throw NeptunError("no tea");'''))

