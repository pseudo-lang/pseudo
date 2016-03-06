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

    def gen(self, custom_exceptions, ast):
        imports, source = self.gen_with_imports(custom_exceptions, ast)
        lines = source.split('\n')
        main_index = lines.index('    public static void Main()')
        if main_index == 2:
            x = '\n'.join(l[8:] for l in lines[4:-3]).strip()
            if x[-1] == ';':
                return x[:-1]
            else:
                return x
        if lines[main_index + 2] == '    }':
            if lines[main_index - 2] == 'public class Program':
                return '\n'.join(lines[0:main_index - 2]).strip()
            else:
                return '\n'.join(lines[0:main_index - 1]) + '}'
        else:
            return source

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


