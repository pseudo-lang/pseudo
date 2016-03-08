import unittest
import textwrap
from pseudo import generate
from pseudo.pseudo_tree import Node
import suite

#v
class TestCSharp(unittest.TestCase, metaclass=suite.TestLanguage): # dark magic bitches

    _language = 'csharp'
    _import = 'using'
    _parse_import = lambda self, line: line[6:-1]
    _ignore_import = 'System'
    _no_strip = True

    def gen_with_imports(self, custom_exceptions, ast):
        imports, source = suite.TestHelpers.gen_with_imports(self, custom_exceptions, ast)
        lines = source.split('\n')
        main_index = lines.index('    public static void Main()')
        if main_index == 2:
            x = '\n'.join(l[8:] for l in lines[main_index + 2:-3]).strip()
            if x[-1] == ';':
                return imports, x[:-1]
            else:
                return imports, x

        if lines[main_index + 2] == '    }':
            if lines[main_index - 2] == 'public class Program':
                return imports, '\n'.join(lines[0:main_index - 2]).strip()
            else:
                return imports, '\n'.join(lines[0:main_index - 1]) + '\n}'
        else:
            return imports, source

    def gen(self, custom_exceptions, ast):
        return self.gen_with_imports(custom_exceptions, ast)[1]

    # make declarative style great again

    # expected c# translation for each example in suite:

    int_ = '42'

    float_ = '42.42'

    string = '"la"'

    boolean = 'true'

    null = 'null'

    dictionary = 'new Dictionary<string, int> { {"la", 0} }'

    list_ = 'new List<string> {"la"}'

    local = 'egg'

    typename = 'Egg'

    instance_variable = 'this.egg'

    attr = 'e.egg'

    local_assignment = 'egg = ham'

    instance_assignment = 'this.egg = ham'

    attr_assignment = 'T.egg = ham'

    call = 'map(x)'

    method_call = 'e.Filter(42)'

    # io
    io_display          = textwrap.dedent('''\
                            Console.WriteLine(2);
                            Console.WriteLine("z")''')

    io_read             = 'var source = Console.ReadLine()'
    io_read_file        = (['System.IO'], 'var source = File.ReadAllText("z.py")')
    io_write_file       = (['System.IO'], 'File.WriteAllText("z.py", source)')

    # math
    math_ln             = 'Math.Log(z)'
    math_tan            = 'Math.Tan(z)'
    math_sin            = 'Math.Sin(z)'
    math_cos            = 'Math.Cos(z)'

    # regexp
    regexp_compile      = (["System.Text.RegularExpressions"], 'new Regex(s)')
    regexp_escape       = (["System.Text.RegularExpressions"], 'Regex.Escape(s)')



    standard_call = [
        'Console.WriteLine(42)',
        'Console.ReadLine()',
        'Math.Log(ham)',
        'var source = File.ReadAllText("f.py")'
    ]

    standard_method_call = [
        'l.Count',
        '"l".Substring(0, 2)'
    ]

    # Regexp
    regexp_match        = 'r.Match(s)'

    # RegexpMatch   # result of s.scan is an array, fix regex in next versions
    regexp_match_group  = 'm.Groups[3].Captures[0]'
    regexp_match_has_match = 'm.Success'

    # Tuple
    tuple_length        = '2' # we know the size of a tuple at constant time, easiest for now

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


    for_statement = [
        textwrap.dedent('''\
            foreach(var a in sequence)
            {
                log(a);
            }'''),

        textwrap.dedent('''\
            for (int j = 0; j != 42; j += 2)
            {
                analyze(j);
            }'''),

        textwrap.dedent('''\
            for (int j = 0; j < z.Count; j ++)
            {
                var k = z[j];
                analyze(j, k);
            }'''),

        textwrap.dedent('''\
            foreach(var _item in z)
            {
                var j = _item.key;
                var k = _item.value;
                analyze(k, j);
            }'''),

        textwrap.dedent('''\
            for (int _index = 0; _index < z.Count; _index ++)
            {
                var k = z[_index];
                var l = zz[_index];
                a(k, l);
            }''')
    ]

    while_statement = textwrap.dedent('''\
        while (f() >= 42)
        {
            var b = g();
        }''')

    function_definition = textwrap.dedent('''\
        public class Program
        {
            static int Weird(int z)
            {
                var fixed = fix(z);
                return fixed;
            }
        }''')

    class_with_method_definition = textwrap.dedent('''\
        public class A
        {
            private int ast;

            List<string> Parse(string source)
            {
                this.ast = 0;
                return new List<string> {source};
            }
        }''')

    anonymous_function = [
        'source => ves(source.Length)',

        textwrap.dedent('''\
            source =>
            {
                Console.WriteLine(source);
                return ves(source.Length);
            }''')
    ]

    class_definition = [textwrap.dedent('''\
        public class A : X
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

    class_constructor = textwrap.dedent('''\
        public class A
        {
            private int a;
            private int b;

            A(int a, int b)
            {
                this.a = a;
                this.b = b;
            }
        }''')

    try_statement = [
        textwrap.dedent('''\
            try
            {
                a();
                h(-4);
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
            }'''),

        textwrap.dedent('''\
            public class NeptunError : Exception
            {
                public NeptunError(string message)
                    : base(message)
                {
                }
            }

            public class Program
            {
                public static void Main()
                {
                    try
                    {
                        a();
                        h(-4);
                    }
                    catch (NeptunError e)
                    {
                        Console.WriteLine(e);
                    }
                }
            }
            ''')
    ]

    throw_statement = textwrap.dedent('''\
        public class NeptunError : Exception
        {
            public NeptunError(string message)
                : base(message)
            {
            }
        }

        public class Program
        {
            public static void Main()
            {
                throw new NeptunError("no tea");
            }
        }
        ''')


