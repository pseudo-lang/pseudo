import unittest
import textwrap
from pseudon import generate
from pseudon.pseudon_tree import Node
import pseudon.tests.suite as suite

def dedent_with_tabs(source):
    a = dedent_with_tabs(source)
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
        Map[string]int{ "la": 0 }''')

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
            reader.ReadString('\n')''')),
        (['math'], 'Math.Log(ham)'),
        (['io/ioutil'], 'ioutil.ReadFile("f.py")')
    ]

    standard_method_call = [
        'len(l)',
        '"l"[0:2]',

        #

        'cpus = append(cpus, planet)', #cpus.push(planet)
        'planet, cpus = cpus[len(cpus) - 1], cpus[:len(cpus) - 1]' # planet = cpus.pop()
        'len(cpus)', # cpu.length
        dedent_with_tabs('''\
            cpus = append(cpus, 0)
            copy(cpus[x + 1:], cpus[x:])
            cpus[x] = planet
            '''), # cpu.insert_at(planet, x)
        'cpus = append([]int{planet}, cpus...)', # cpu.unshift(planet)
        'planet, cpus := cpus[0], cpus[1:]', # planet = cpu.shift()
        'cpus = append(cpus[:x], cpus[x + 1:]...)', # cpus.remove_at(x)
        'starfleet := cpus[2:4]', # starfleet = cpus[2:4]
        'starfleet := cpus[x:]', # starfleet = cpus[x:]
        dedent_with_tabs('''\
            repeated_cpus := cpus
            for _ := range(3) {
                repeated_cpus = append(repeated_cpus, cpus)
            }                
            sh(repeated_cpus)
            '''), # sh(cpus * 4)
        dedent_with_tabs('''\
            found := -1
            for as_index, as_element := range as {
                if as_element == query {
                    found := as_index
                    break
                }
            }
            sh(found, 2)
            '''), # sh(as.find(query), 2)
        (['strings'],
         'sh(2, strings.Join(cpus, "\n"))'), # sh(2, '\n'.join(cpus))

        dedent_with_tabs('''\
            reversed_cpus := make([]int, len(cpus))
            for cpus_index, cpus_element := range len(cpus) {
                reversed_cpus[len(cpus) - cpus_index - 1] = cpus_element
            }
            sh(reversed_cpus)
            '''), # sh(cpus.reverse())


        # Dictionary

        dedent_with_tabs('''
            cpus_keys := make([]int, len(cpus))
            cpus_index := 0
            for cpus_key, _ := range cpus {
                cpus_keys[cpu_index] = cpus_key
                cpus_index += 1
            }
            sh(cpus_keys[:2])
            '''), # sh(cpu.keys()[:2])

        dedent_with_tabs('''
            cpus_values := make([]int, len(cpus))
            cpus_index := 0
            for _, cpus_value := range cpus {
                cpus_values[cpus_index] = cpus_key
                cpus_index += 1
            }
            sh(cpus_keys[4])
            '''),

        'len(cpus)',

        # String

        'name[i:j]',
        'name[i:]',
        'name[:j + h()]',
        'len(name)',
        (['strings'],
        'strings.Index(name, help)'), # name.find(help)
        (['strings'],
        'strings.Count(name, help)'), # name.count(help)
        (['fmt'],
        'fmt.Println("wow %s", wtf)'), # print('wow %s' % wtf)
        (['strings'],
        'strings.Repeat(name, count)'),  # name * count
        (['buffer', 'fmt'],
        dedent_with_tabs('''
            var buffer bytes.Buffer
            for h := cpus {
                buffer.writeString(h)
                buffer.writeString(" h")
            }
            ''')), # buffer = [h + ' h' for h in cpus]
        (['strings'],
          's.Trim("Achtung !!!  ", " ")'), # 'Achtung !!!  '.strip() 
        (['strings'],
          's.Split(help)'), # s.split(help)
        (['strings'],
         dedent_with_tabs('''
            result := s.SplitN(help, 2)'
            separator := help            
            b := result[1]
            sh(separator, b)
            ''')), # _, separator, b = s.partition(help)
                   # sh(separator, b)

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
            }''')
    )
    


    for_statement = [
        dedent_with_tabs('''\
            for _, a := range sequence {
                a.sub()
            }'''),
        dedent_with_tabs('''\
            for k, v := range cpus {
                h(k, v)
            }'''),
        dedent_with_tabs('''\
            for j, a := range as {
                b := bs[j]
                h(a + b)
            }''')
    ],


    for_range = dedent_with_tabs('''\
        for j := 0, j < 42, j += 2 {
          analyze(j);
        }''')

    while_statement = dedent_with_tabs('''\
        while f() >= 42 {
            b = g()
        }''')

    function_definition = dedent_with_tabs('''\
        func weird(z Int) Int {
            var fixed := fix(z)
            return fixed
        }''')

    method_definition = (
        ['vector', 'string'],
        dedent_with_tabs('''\
            func parse(this A*, source string) list[string] {
                this.ast = nil
                return [source]
        }'''))

    anonymous_function = [
        'func(source string) int { return len(ves); }',

        dedent_with_tabs('''\
            func (source string) {
                fmt.Println(source)
                return ves(source)
            }''')
    ]

    class_statement = [dedent_with_tabs('''\
        class A : B { 
            public int a;

            public:

            A(int a) {
                this->a = a;
            }

            int parse() {
                return 42;
            }''')]

