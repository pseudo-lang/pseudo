import textwrap
from pseudon import generate
from pseudon.pseudon_tree import Node

#v
def gen(ast):
    return generate(ast, 'cpp')[:-1] #without last \n

def gen_with_includes(ast):
    result = generate(Node('module', main=[ast]))[:-1]
    ls = result.split('\n')
    includes, out = [], []
    current = 'include'
    for l in ls:
        l = l.strip()
        if not l:
            continue
        elif l.startswith('int main('):
            current = 'out'
        elif current == 'include' and l.startswith('#include<'):
            includes.append(l[9:-1])
        else:
            out.append(l)
    return includes, '\n'.join(out[:-1])

def test_module():
    source = gen(Node('module', code=[]))
    assert source == '''\
int main() {
}'''

def test_int():
    source = gen(Node('int', value=42))
    assert source == '42'

def test_float():
    source = gen(Node('float', value=42.420))
    assert source == '42.42'

def test_str():
    source = gen(Node('string', value='la'))
    assert source == '"la"'

def test_boolean():
    source = gen(Node('boolean', value=True))
    assert source == 'true'

def test_null():
    source = gen(Node('null'))
    assert source == 'NULL'

def test_dictionary():
    includes, source = gen_with_includes(Node('dictionary', pairs=[
        [Node('string', value='la'), Node('int', 0)]],
        type='Dictionary[String,Int]'))
    assert includes == ['iostream', 'unordered_map']
    assert source == 'unordered_map<string, int>{ { "la", 0 } };'

def test_list():
    includes, source = gen_with_includes(Node('list', elements=[Node('string', value='la')], type='List[String]'))
    assert includes == ['iostream', 'vector']
    assert source == 'vector<string>{ "la" };'

def test_local():
    source = gen(Node('local', name='egg'))
    assert source == 'egg'

def test_typename():
    source = gen(Node('typename', name='Egg'))
    assert source == 'Egg'

def test_instance_variable():
    source = gen(Node('instance_variable', name='egg'))
    assert source == 'this.egg'

def test_attr():
    source = gen(Node('attr', receiver=Node('local', name='e'), attr='egg'))
    assert source == 'e.egg'

def test_local_assignment():
    source = gen(Node('local_assignment', local='egg', value=Node('local', name='ham')))
    assert source == 'egg = ham'

def test_instance_assignment():
    source = gen(Node('instance_assignment', name='egg', value=Node('local', name='ham')))
    assert source == 'this.egg = ham'

def test_attr_assignment():
    source = gen(Node('attr_assignment', 
        attr=Node('attr', receiver=Node('typename', name='T'), attr='egg'), 
         value=Node('local', name='ham')))
    assert source == 'T.egg = ham'

def test_call():
    source = gen(Node('call', function=Node('local', name='map'), args=[Node('local', name='x')]))
    assert source == 'map(x)'

def test_method_call():
    source = gen(Node('method_call', receiver=Node('local', name='e'), message='filter', args=[Node('int', value=42)])
    assert source == 'e.filter(42)'

def test_standard_call():
    includes, source = gen_with_includes(Node('standard_call', function=Node('local', name='display'), args=[Node('int', value=42)]))
    assert source == 'Console.WriteLine(42)'

    includes, source = gen_with_includes(
        Node('local_assignment', 
            local='a',
            value=Node('standard_call', function=Node('local', name='read'), args=[])))
    assert includes == ['iostream']
    assert source == 'cin << a'

def test_standard_method_call():
    includes, source = gen_with_includes(Node('standard_method_call', receiver=Node('local', name='l', type='List[Int]'), message='length', args=[]))
    assert includes == ['vector']
    assert source == 'l.length'

    includes, source = gen_with_includes(Node('standard_method_call', receiver=Node('str', value='l'), message='substr', args=[Node('int', value=0), Node('int', value=2)]))
    assert includes == ['string']
    assert source == 'l.substr(0, 2)'

def test_binary_op():
    source = gen(Node('binary_op', op='+', left=Node('local', name='ham'), right=Node('local', name='egg')))
    assert source == 'ham + egg'

def test_unary_op():
    source = gen(Node('unary_op', op='-', value=Node('local', name='a')))
    assert source == '-a'

def test_standard_math():
    includes, source = gen_with_includes(Node('module', code=[
        Node('standard_math', op='sin', args=[Node('local', name='ham')])]))
    assert includes == ['math']
    assert source == 'sin(ham)'

def test_comparison():
    source = gen(Node('comparison', op='>', left=Node('local', name='egg'), right=Node('local', name='ham')))
    assert source == 'egg > ham'


def test_if():
    includes, source = gen_with_includes(Node('if', 
        test=Node('comparison',
            op='==',
            left=Node('local', name='egg'), 
            right=Node('local', name='ham')),
        block=[
            Node('standard_method_call',
                receiver=Node('local', name='l', type='List[String]'),
                message='sublist',
                args=[Node('int', value=0), Node('int', value=2)])],
        otherwise=Node('if', 
            test=Node('comparison',
                op='==',
                left=Node('local', name='egg'), 
                right=Node('local', name='ham')),
            block=[
                Node('standard_call', function=Node('local', name='display'), args=[Node('float', '4.2')])
            ],
            otherwise=[
                Node('local', 'z', type='List[String]')
            ])))

    assert includes == ['iostream', 'vector']
    assert source == textwrap.dedent('''\
                if (egg == ham) {
                  l.subList(l.begin(), l.begin() + 2);
                }
                else if (egg == ham) {
                  cout << 4.2;
                }
                else {
                    z;
                }''')


