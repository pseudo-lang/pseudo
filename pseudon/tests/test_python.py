from pseudon import generate
from pseudon.pseudon_tree import Node

def gen(ast):
	return generate(ast, 'python')

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
	assert source == 'None'

def test_dictionary():
	source = gen(Node('dictionary', pairs=[
		[Node('string', value='la'), Node('int', 0)]]))
	assert source == "{'la': 0}"

def test_list():
	source = gen(Node('list', elements=[Node('string', value='la')]))
	assert source == 'la'

def test_local():
	source = gen(Node('local', name='egg'))
	assert source == 'egg'

def test_typename():
	source = gen(Node('typename', name='Egg'))
	assert source == 'Egg'

def test_instance_variable():
	source = gen(Node('instance_variable', name='egg'))
	assert source == 'self.egg'

def test_attr():
	source = gen(Node('attr', receiver=Node('local', name='e'), attr='egg'))
	assert source == 'e.egg'

def test_local_assignment():
	source = gen(Node('local_assignment', local='egg', value=Node('local', name='ham')))
	assert source == 'egg = ham'

def test_instance_assignment():
	source = gen(Node('instance_assignment', name='egg', value=Node('local', name='ham')))
	assert source == 'self.egg = ham'

def test_attr_assignment():
	source = gen(Node('attr_assignment', 
		attr=Node('attr', receiver=Node('typename', name='T'), attr='egg'), 
		 value=Node('local', name='ham')))
	assert source == 'T.egg = ham'





