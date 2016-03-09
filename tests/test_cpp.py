import unittest
import textwrap
from pseudo import generate
from pseudo.pseudo_tree import Node
import suite as suite

#v
class TestCpp(unittest.TestCase, metaclass=suite.TestLanguage): # dark magic bitches
    
    _language = 'cpp'
    _import = '#include'
    _parse_import = lambda self, line: line[10:-1]

    def gen(self, custom_exceptions, ast):
        imports, source = self.gen_with_imports(custom_exceptions, ast)
        z = source.strip()
        if z[-1] == ';':
            return z[:-1]
        else:
            return z


    def gen_special(self, source):
        lines = source.lstrip().split('\n')
        main_index = lines.index('int main() {')
        main = '\n'.join([line[4:] for line in lines[main_index + 1:-1]]).strip()
        l = 0

        imports = set()
        while len(lines) > l and (not lines[l] or lines[l].startswith(self._import)):
            if lines[l]:
                imports.add(lines[l][9:-1])
            l += 1

        if len(lines) > l + 1 and lines[l + 1] == 'using namespace std;':
            l += 2

        definitions = '\n'.join(lines[l:main_index]).lstrip()
        
        if not definitions.strip():
            return imports, main
        else:
            # input(definitions)
            # input(definitions + '\n'.join(lines[main_index:]))
            return imports, definitions + '\n' + '\n'.join(lines[main_index:])

    # make declarative style great again

    # expected c++ translation for each example in suite:

    int_ = '42'

    float_ = '42.42'

    string = '"la"'

    null = 'NULL'

    dictionary = (
        {'iostream', 'unordered_map', 'string'},
        'unordered_map<string, int>{{"la": 0}};'
    )

    list_ = (
        {'iostream', 'vector', 'string'},
        '{"la"};'
    )

    local = 'egg'

    typename = 'Egg'

    instance_variable = 'this->egg'

    attr = 'e.egg'

    local_assignment = 'egg = ham'

    instance_assignment = 'this.egg = ham'

    attr_assignment = 'T.egg = ham'

    call = 'map(x)'

    method_call = 'e->filter(42)'

    standard_call = [
        'cout << 42 << endl',
        ({'iostream', 'string'}, textwrap.dedent('''\
            string _dummy;
            cin >> _dummy;''')),
        ({'math'}, 'log(ham);'),
        ({'iostream', 'fstream', 'string'}, textwrap.dedent('''\
            ifstream ifs("f.py");
            string source((istreambuf_iterator<char>(ifs)), (istreambuf_iterator<char>()));'''))
    ]

    standard_method_call = [
        'l.size()',
        '"l".substr(0, 2)'
    ]

    binary_op = 'ham + egg'

    unary_op = '-a'

    comparison = 'egg > ham'

    if_statement = (
        {'iostream', 'vector'},
        textwrap.dedent('''\
            if (egg == ham) {
                vector<string> _sliced(l.begin(), l.begin() + 2);
            } else if (egg == ham) {
                cout << 4.2 << endl;
            } else {
                z;
            }''')
    )


    for_statement = [
        textwrap.dedent('''\
            for(auto a: sequence) {
                log(a);
            }'''),

        textwrap.dedent('''\
            for(int j = 0; j != 42; j += 2) {
                analyze(j);
            }'''),

        textwrap.dedent('''\
          for(int j = 0; j < z.size(); j ++) {
              auto k = z[j];
              analyze(j, k);
          }'''),

        textwrap.dedent('''\
          for(auto& _item : z) {
              auto j = _item.first;
              auto k = _item.second;
              analyze(k, j);
          }'''),
    
        textwrap.dedent('''\
            for(int _index = 0; _index < z.size(); _index ++) {
                auto k = z[_index];
                auto l = zz[_index];
                a(k, l);
            }''')
    ]

    while_statement = textwrap.dedent('''\
        while (f() >= 42) {
            int b = g();
        }''')

    function_definition = textwrap.dedent('''\
        int weird(int z) {
            int fixed = fix(z);
            return fixed;
        }

        int main() {
        }''')

    class_with_method_definition = (
        {'iostream', 'vector', 'string'},
        textwrap.dedent('''\
        class A {
            private int ast;

            vector<string> parse(string source) {
                this->ast = 0;
                return {source};
            }
        }

        int main() {
        }

        '''))

    anonymous_function = [
         '[](string source) { return ves(source.length()); }',

        textwrap.dedent('''\
            [](string source) {
                cout << source << endl;
                return ves(source.length());
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

    class_constructor = textwrap.dedent('''\
        class A {
            private int a;
            private int b;

            A(int a, int b) {
                this->a = a;
                this->b = b;
            }
        }

        int main() {
        }''')

    try_statement = [
        ({'iostream', 'stdexcept', 'exception'}, 
         textwrap.dedent('''\
            try {
                a();
                h(-4);
            }
            catch (exception& e) {
                cout << e.what() << endl;
            }''')),

        ({'iostream', 'stdexcept', 'exception'}, 
         textwrap.dedent('''\
            class NeptunError : runtime_error {
            }

            int main() {
                try {
                    a();
                    h(-4);
                }
                catch (NeptunError& e) {
                    cout << e.what() << endl;
                }
            }
            
            '''))
    ]

    index = '"la"[2]'

    cpp_new_instance = 'smart_ptr<Z> z = new Z()'

    cpp_pointer_method_call = 'z->rave(0)'

    throw_statement = ({'iostream', 'stdexcept', 'exception', 'string'}, 
        textwrap.dedent('''\
        class NeptunError : runtime_error {
        }

        int main() {
            throw NeptunError("no tea");
        }

        '''))

