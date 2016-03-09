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
        main_index = lines.index('    public static void Main(string[] args)')
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

    list_ = 'new[] {"la"}'

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
    io_read_file        = (['System.IO', 'System.Text'], 'var source = File.ReadAllText("z.py")')
    io_write_file       = (['System.IO', 'System.Text'], 'File.WriteAllText("z.py", source)')

    # math
    math_ln             = 'Math.Log(z)'
    math_tan            = 'Math.Tan(z)'
    math_sin            = 'Math.Sin(z)'
    math_cos            = 'Math.Cos(z)'

    # regexp
    regexp_compile      = (["System.Text.RegularExpressions", "System.Text"], 'new Regex(s)')
    regexp_escape       = (["System.Text.RegularExpressions", "System.Text"], 'Regex.Escape(s)')



    standard_call = [
        'Console.WriteLine(42)',
        'Console.ReadLine()',
        'Math.Log(ham)',
        'var source = File.ReadAllText("f.py")'
    ]

    standard_method_call = [
        'l.Length',
        '"l".Substring(0, 2)'
    ]
    # List
    list_push       = 'cpus.Insert("")'
    list_pop        = 'cpus.RemoveAt(cpus.Length - 1)'
    list_length     = 'cpus.Length'
    list_map        = 'cpus.Select(value => value + "a").ToList()' # v.4 support IEnumerable?
    list_remove     = "cpus.Remove(s)"
    list_remove_at  = "cpus.RemoveAt(0)"
    list_slice      = 'cpus.Take(cpus.Length - 1).Drop(2)'
    list_slice_from = 'cpus.Drop(2)'
    list_slice_to   = 'cpus.Take(2)'
    list_filter     = 'cpus.Where(value => value.Length == 0).ToList()'
    list_reduce     = textwrap.dedent('''\
                        cpus.Aggregate("", (value, other) => {
                            var result = value + other;
                            return result;
                        })''')
    list_any        = 'cpus.Any(value => value.Length == 0).ToList()'
    list_all        = 'cpus.All(value => value.Length == 0).ToList()'

    # # Hash
    dictionary_length   = 'pointers.length'
    dictionary_contains = 'pointers.include?(s)'
    dictionary_keys     = 'pointers.keys'
    dictionary_values   = 'pointers.values'

    # # Set
    set_length          = 'words.Length'
    set_contains        = 'words.Contains(s)'
    set_union           = 'words.Union(words)'
    set_intersection    = 'words.Intersection(words)'

    # Tuple
    tuple_length        = '2' # we know the size of a tuple at constant time, easiest for now

    # Array
    array_length        = '10'

    # String
    string_substr       = 's.Substring(1, s.Length - 2)'
    string_substr_from  = 's.Substring(2)'
    string_substr_to    = 's.Substring(0, s.Length - 2)'
    string_length       = 's.Length'
    string_find         = 's.IndexOf(t)'
    string_find_from    = 's.IndexOf(t, z)'
    string_count        = 's.Count(sub => sub == s)'
    string_concat       = 's + t'
    # string_partition    = 's.split(t)[0]' #FIXV3
    string_split        = 's.Split(new[] { t }, StringSplitOptions.None)'
    string_trim         = 's.Trim()'
    # string_reversed     = 's.everse' #FIXV3
    string_center       = 's.PadLeft((z - s.Length) / 2 + s.Length, t).PadRight(z, t)'
    string_present      = 's.Length != 0'
    string_empty        = 's.Length == 0'
    string_contains     = 's.Contains(t)'
    string_to_int       = 'Int32.Parse(s)'
    string_pad_left     = 's.PadLeft(0, t)'
    string_pad_right    = 's.PadRight(0, t)'

    # Regexp
    regexp_match        = 'r.Match(s)'

    # RegexpMatch   # result of s.scan is an array, fix regex in next versions
    regexp_match_group  = 'm.Groups[3].Captures[0]'
    regexp_match_has_match = 'm.Success'

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
            for (int j = 0; j < z.Length; j ++)
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
            for (int _index = 0; _index < z.Length; _index ++)
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
                return new[] {source};
            }
        }''')

    anonymous_function = [
        'source => ves(source.Length)',

        textwrap.dedent('''\
            source => {
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
                public static void Main(string[] args)
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
            public static void Main(string[] args)
            {
                throw new NeptunError("no tea");
            }
        }
        ''')


