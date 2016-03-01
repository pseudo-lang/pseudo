import unittest

class TestLanguage(type):

    SNAKE_CASE_REGEX = re.compile(r'(_\[a-z])')

    def __new__(cls, name, bases, namespace, **kwargs):

        def generate_test(name, examples, expected):
            def test(self):
                if isinstance(expected, (str, tuple)):
                    expected = [expected]

                for example, exp in zip(examples, expected):
                    if isinstance(exp, str):
                        self.assertEqual(, exp)
                    else:
                        imports, source = self.gen_with_imports(example)
                        self.assertEqual(imports, exp[0])
                        self.assertEqual(source, exp[1])
            return test

        for name, exp in namespace:
            if name[-1] == '_':
                name = name[:-1] # int etc
            examples = getattr(suite, SNAKE_CASE_REGEX.sub(lambda e: e[1].upper(), name.title()))
            if examples:
                test_name = 'test_%s' % name
                namespace[test_name] = generate_test(name, exp)

        return super().__new__(cls, name, bases, namespace)

Module      = [Node('module', code=[])]
Int         = [Node('int', value=42)]
Float       = [Node('float', value=42.420)]
String      = [Node('string', value='la')]
Boolean     = [Node('boolean', value=True)]
Null        = [Node('null')]
Dictionary  = [Node('dictionary', pairs=[
                [Node('string', value='la'), Node('int', 0)]])]
List        = [Node('list', elements=[Node('string', value='la')])]
Local       = [Node('local', name='egg')]
Typename    = [Node('typename', name='Egg')]
InstanceVariable = [Node('instance_variable', name='egg')]
Attr        = [Node('attr', receiver=Node('local', name='e'), attr='egg')]
LocalAssignment = [Node('local_assignment', local='egg', value=Node('local', name='ham'))]
InstanceAssignment = [Node('instance_assignment', name='egg', value=Node('local', name='ham'))]
AttrAssignment = [Node('attr_assignment', 
        attr=Node('attr', receiver=Node('typename', name='T'), attr='egg'), 
         value=Node('local', name='ham'))]
Call        = [Node('call', function=Node('local', name='map'), args=[Node('local', name='x')])]
MethodCall  = [Node('method_call', receiver=Node('local', name='e'), message='filter', args=[Node('int', value=42)])]
StandardCall = [
    Node('standard_call', function='display', args=[Node('int', value=42)]),
    Node('standard_call', function='read', args=[])
]

If = [
    Node('if_statement', 
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
                Node('standard_call', function='display', args=[Node('float', '4.2')])
            ],
            otherwise=[
                Node('local', 'z', type='List[String]')
            ]))
]
