import unittest
import textwrap
from pseudo import generate
from pseudo.pseudo_tree import Node
import suite as suite

def dedent_with_tabs(source):
    a = textwrap.dedent(source)
    return a.replace('    ', '\t')

#v
class TestGo(unittest.TestCase, metaclass=suite.TestLanguage): # dark magic bitches

    _language = 'go'
    _import = 'import'

    def gen(self, custom_exceptions, ast):
        imports, source = self.gen_with_imports(custom_exceptions, ast)
        return source.strip()


    def gen_special(self, source):
        lines = source.split('\n')[2:] # package main
        main_index = lines.index('func main() {')
        main = '\n'.join([line[1:] for line in lines[main_index + 1:-2]]).strip()
        l = 0

        if lines[0].startswith('import'):
            if lines[0][7] == '"':
                imports = {lines[0][8:-1]}
                m = 1
            else:
                m = lines.index(')')
                imports = {line.strip()[1:-1] for line in lines[1:m]}
            definitions = '\n'.join(lines[m + 1:main_index])
        else:
            imports = set()
            definitions = '\n'.join(lines[:main_index])
        return imports, definitions + main

    # make declarative style great again

    # expected go translation for each example in suite:

    int_ = '42'

    float_ = '42.42'

    string = '"la"'

    null = 'nil'

    dictionary = 'map[string]int { "la": 0 }'

    neg_index = '"la"[len("la") - 2]'

    list_ = '[]string {"la"}'

    local = 'egg'

    typename = 'Egg'

    instance_variable = 'this.egg'

    attr = 'e.Egg'

    local_assignment = 'egg = ham'

    instance_assignment = 'this.egg = ham'

    attr_assignment = 'T.egg = ham'

    call = 'map(x)'

    method_call = 'e.Filter(42)'

    standard_call = [
        ({'fmt'}, 'fmt.Println(42)'),
        ({'bufio', 'os'}, dedent_with_tabs('''\
            reader, err := bufio.NewReader(os.Stdin)
            reader.ReadString("\\n")''')),
        ({'math'}, 'math.Log(ham)'),
        ({'io/ioutil'}, dedent_with_tabs('''\
                            _contents, _ := ioutil.ReadFile("f.py")
                            source := string(_contents)'''))
    ]

    standard_method_call = [
        'len(l)',
        '"l"[:2]'
    ]

    # io
    io_display          = ({'fmt'}, 'fmt.Println(2, "z")')
    io_read             = ({'bufio', 'os'}, dedent_with_tabs('''\
                                reader, err := bufio.NewReader(os.Stdin)
                                source := reader.ReadString("\\n")'''))
    io_read_file        = dedent_with_tabs('''\
                            _contents, _ := ioutil.ReadFile("z.py")
                            source := string(_contents)''')
    io_write_file       = 'ioutil.WriteFile("z.py", source)'

    math_ln             = ({'math'}, 'math.Log(z)')
    math_log            = ({'math'}, 'math.Log(z, 2.0)')
    math_tan            = ({'math'}, 'math.Tan(z)')
    math_sin            = ({'math'}, 'math.Sin(z)')
    math_cos            = ({'math'}, 'math.Cos(z)')
    
    # regexp    
    regexp_compile      = ({'regexp'}, 'regexp.MustCompile(s)')
    regexp_escape       = ({'regexp'}, 'regexp.QuoteMeta(s)')

    set_length          = 'len(words)'
    set_contains        = dedent_with_tabs('''\
                            _, _contains := words[s]
                            _contains''')

    dictionary_length   = 'len(pointers)'
    dictionary_contains = dedent_with_tabs('''\
                            _, _contains := pointers[s]
                            _contains''')

    dictionary_keys     =  dedent_with_tabs('''\
                            _pointersKeys := make([]string, "", len(pointers))
                            _pointersIndex := 0
                            for _pointersKey, _ := range pointers {
                                _pointersKeys[_pointersIndex] = _pointersKey
                                _pointersIndex += 1
                            }

                            _pointersKeys''')
    dictionary_values   = dedent_with_tabs('''\
                            _pointersValues := make([]int, 0, len(pointers))
                            _pointersIndex := 0
                            for _, _pointersValue := range pointers {
                                _pointersValues[_pointersIndex] = _pointersValue
                                _pointersIndex += 1
                            }

                            _pointersValues''')

    tuple_length        = '2'

    array_length        = '10'

    list_push           = "cpus := append(cpus, \"\")"
    list_pop            = "cpus := cpus[:len(cpus) - 1]"
    list_length         = "len(cpus)"
    list_map            = dedent_with_tabs('''\
                            _results := make([]string, "", len(cpus))
                            for _index, value := range cpus {
                                _results[_index] = value + "a"
                            }

                            _results''')
        
    list_filter         = dedent_with_tabs('''\
                            var _results []string
                            for _index, value := range cpus {
                                if len(value) == 0 {
                                    _results := append(_results, value)
                                } 

                            }

                            _results''')
    
    list_find           = dedent_with_tabs('''\
                            _found := -1
                            for _cpusIndex, _cpusElement := range cpus {
                                if _cpusElement == s {
                                    _found := _cpusIndex
                                    break
                                } 

                            }

                            _found''')

    list_reduce         = dedent_with_tabs('''\
                            value := ""
                            for _, other := range cpus {
                                result := value + other
                                value := result
                            }

                            value''')

    list_contains       = dedent_with_tabs('''\
                            _contains := false
                            for _, _cpusElement := range cpus {
                                if _cpusElement == s {
                                    _contains := true
                                    break
                                } 

                            }

                            _contains''')

    list_present        = 'len(cpus) > 0'

    list_empty          = 'len(cpus) == 0'

    list_slice          = 'cpus[2:len(cpus) - 1]'
    list_slice_from     = 'cpus[2:]'
    list_slice_to       = 'cpus[:2]'

    string_length       = 'len(s)'
    string_contains     = 'strings.Contains(s, t)'
    string_empty        = 'len(s) == 0'
    string_substr       = 's[1:len(s) - 1]'
    string_substr_from  = 's[2:]'
    string_substr_to    = 's[:len(s) - 2]'
    string_find         = 'strings.Index(s, t)'
    string_find_from    = 'z + strings.Index(s[z:], t)'
    string_count        = ({'strings'}, 'strings.Count(s, t)')
    string_split        = ({'strings'}, 'strings.Split(s, t)')
    string_to_int       = ({'strconv'}, dedent_with_tabs('''\
                            _int, _ := strconv.Atoi(s)
                            _int'''))

        # # String

        # 'name[i:j]',
        # 'name[i:]',
        # 'name[:j + h()]',
        # 'len(name)',
        # (['strings'],
        # 'strings.Index(name, help)'), # name.find(help)
        # (['strings'],
        # 'strings.Count(name, help)'), # name.count(help)
        # (['fmt'],
        # 'fmt.Println("wow %s", wtf)'), # print('wow %s' % wtf)
        # (['strings'],
        # 'strings.Repeat(name, count)'),  # name * count
        # (['buffer', 'fmt'],
        # dedent_with_tabs('''
        #     var buffer bytes.Buffer
        #     for h := cpus {
        #         buffer.writeString(h)
        #         buffer.writeString(" h")
        #     }
        #     ''')), # buffer = [h + ' h' for h in cpus]
        # (['strings'],
        #   's.Trim("Achtung !!!  ", " ")'), # 'Achtung !!!  '.strip() 
        # (['strings'],
        #   's.Split(help)'), # s.split(help)
        # (['strings'],
        #  dedent_with_tabs('''
        #     result := s.SplitN(help, 2)'
        #     separator := help            
        #     b := result[1]
        #     sh(separator, b)
        #     ''')), # _, separator, b = s.partition(help)
        #            # sh(separator, b)


    binary_op = 'ham + egg'

    unary_op = '-a'

    comparison = 'egg > ham'

    if_statement = (
        {'fmt'},
        dedent_with_tabs('''\
            if egg == ham {
                l[:2]
            } else if egg == ham {
                fmt.Println(4.2)
            } else {
                z
            }''')
    )
    


    for_statement = [
        dedent_with_tabs('''\
            for _, a := range sequence {
                log(a)
            }'''),
        dedent_with_tabs('''\
            for j := 0; j != 42; j += 2 {
                analyze(j)
            }'''),
        dedent_with_tabs('''\
            for j, k := range z {
                analyze(j, k)
            }'''),
        dedent_with_tabs('''\
            for j, k := range z {
                analyze(k, j)
            }'''),
        dedent_with_tabs('''\
            for _index, _ := range len(z) {
                k := z[_index]
                l := zz[_index]
                a(k, l)
            }''')
    ]

    while_statement = dedent_with_tabs('''\
        for f() >= 42 {
            b := g()
        }''')

    function_definition = dedent_with_tabs('''\
        func Weird(z int) int {
            fixed := fix(z)
            return fixed
        }''')

    method_definition = (
        dedent_with_tabs('''\
            func (this *A) Parse(source string) []string {
                this.ast = 0
                return []string {source}
            }'''))

    anonymous_function = [
        'func (source string) { return ves(len(source)) }',

        dedent_with_tabs('''\
            func (source string) {
                fmt.Println(source)
                return ves(len(source))
            }''')
    ]

    class_statement = [dedent_with_tabs('''\
        struct A {
            a int
        }

        func parse(this *A) int {
            return 42
        }''')]

    this = 'this'

    go_constructor = textwrap.dedent('''\
        struct A {
            z int
        }

        func newA(a int, b int) *A {
          return A{a + b}
        }''')

    index = '"la"[2]'

    # try_statement = [
    #     textwrap.dedent('''\
    #         result, err := h(-4)
    #         if err != nil {
    #             fmt.Printf("%s", err)
    #             return 0
    #         } else {
    #             result += 2
    #         }
    #         return x(result)
    #         '''),

    #     textwrap.dedent('''\
    #         type NeptunError struct {
    #             s string
    #         }

    #         func (this *NeptunError) Error() string {
    #             return this.s
    #         }

    #         result, err := h(-4)
    #         if _err, ok := err.(*NeptunError); ok {
    #             fmt.Printf("%s", err)
    #             return 0
    #         } else {
    #             result += 2
    #         }
    #         return x(result)
    #         ''')
    # ]

    # throw_statement = textwrap.dedent('''\
    #     type NeptunError struct {
    #         s string
    #     }

    #     func (this *NeptunError) Error() string {
    #         return this.s
    #     }
        
    #     func h(s int) (int, error) {
    #         if s > 0 {
    #             return 0, &NeptunError{"no tea"}
    #         }
    #         return -s
    #     }
    #     ''')



    