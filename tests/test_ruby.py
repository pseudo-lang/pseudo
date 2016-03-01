from pseudon import generate
from pseudon.pseudon_tree import Node

#v
def gen(ast):
    return generate(ast, 'ruby')[:-1] #without last \n

def test_module():
    source = gen(Node('module', code=[]))
    assert source == ''

def test_int():
    source = gen(Node('int', value=42))
    assert source == '42'

def test_float():
    source = gen(Node('float', value=42.420))
    assert source == '42.42'

def test_str():
    source = gen(Node('string', value='la'))
    assert source == "'la'"

def test_boolean():
    source = gen(Node('boolean', value=True))
    assert source == 'True'

def test_null():
    source = gen(Node('null'))
    assert source == 'nil'

def test_dictionary():
    source = gen(Node('dictionary', pairs=[
        [Node('string', value='la'), Node('int', 0)]]))
    assert source == '{la: 0}'

def test_list():
    source = gen(Node('list', elements=[Node('string', value='la')]))
    assert source == "['la']"

def test_local():
    source = gen(Node('local', name='egg'))
    assert source == 'egg'

def test_typename():
    source = gen(Node('typename', name='Egg'))
    assert source == 'Egg'

def test_instance_variable():
    source = gen(Node('instance_variable', name='egg'))
    assert source == '@egg'

def test_attr():
    source = gen(Node('attr', receiver=Node('local', name='e'), attr='egg'))
    assert source == 'e.egg'

def test_local_assignment():
    source = gen(Node('local_assignment', local='egg', value=Node('local', name='ham')))
    assert source == 'egg = ham'

def test_instance_assignment():
    source = gen(Node('instance_assignment', name='egg', value=Node('local', name='ham')))
    assert source == '@egg = ham'

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
    source = gen(Node('standard_call', function=Node('local', name='display'), args=[Node('int', value=42)]))
    assert source == 'puts 42'

    source = gen(Node('standard_call', function=Node('local', name='read'), args=[]))
    assert source == 'gets'

def test_standard_method_call():
    source = gen(Node('standard_method_call', receiver=Node('local', name='l', type='List[Int]'), message='length', args=[]))
    assert source == 'l.length'

    source = gen(Node('standard_method_call', receiver=Node('str', value='l'), message='substr', args=[Node('int', value=0), Node('int', value=2)]))
    assert source == 'l[0...2]'

def test_binary_op():
    source = gen(Node('binary_op', op='+', left=Node('local', name='ham'), right=Node('local', name='egg')))
    assert source == 'ham + egg'

def test_unary_op():
    source = gen(Node('unary_op', op='-', value=Node('local', name='a')))
    assert source == '-a'

def test_standard_math():
    source = gen(Node('module', code=[
        Node('standard_math', op='sin', args=[Node('local', name='ham')])]))
    assert source == 'Math.sin(ham)'

def test_comparison():
    source = gen(Node('comparison', op='>', left=Node('local', name='egg'), right=Node('local', name='ham')))
    assert source == 'egg > ham'


def test_if():
    source = gen(Node('if', 
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

    assert source == \
'''if egg == ham
  l[0...2]
elsif egg == ham
  puts 4.2
else
  z'''
