from pseudo.middlewares.middleware import Middleware

class NameMiddleware(Middleware):
    '''
    changes names according to language conventions

    can accept rules for normal_name, method_name and function_name
    available rules: snake_case, camel_case, pascal_case

    currently used c#, go, javascript and php
    '''

    def __init__(self, normal_name=None, method_name=None, function_name=None):
        self.normal_name = normal_name
        self.method_name = method_name
        self.function_name = function_name
        
    def process(self, tree):
        self.tree = tree
        self.defined_functions = {q.name for q in self.tree.definitions if q.type == 'function_definition'}
        return self.transform(tree)

    def transform_normal_name(self, node, in_block=False, assignment=None):
        if isinstance(node.name, str):
            # import pdb; pdb.set_trace()
            if node.type == 'local' and node.name in self.defined_functions:
                if self.function_name:
                    node.name = getattr(self, 'convert_to_%s' % self.function_name)(node.name)
            else:
                if self.normal_name:
                    node.name = getattr(self, 'convert_to_%s' % self.normal_name)(node.name)
        elif self.normal_name:
            print('NORM', node.name.y)
            # input()
        return node
    
    transform_local = transform_instance_variable = transform_normal_name

    def transform_f(self, node, in_block=False, assignment=None):
        if node.type == 'function_definition' and self.function_name:
            node.name = getattr(self, 'convert_to_%s' % self.function_name)(node.name)
        elif node.type == 'method_definition' and self.method_name:
            node.name = getattr(self, 'convert_to_%s' % self.method_name)(node.name)
        if self.normal_name:
            new_name = getattr(self, 'convert_to_%s' % self.normal_name)
            node.params = [new_name(param.name) for param in node.params]

        node.block = self.transform(node.block)
        
        return node

    transform_function_definition = transform_method_definition = transfrom_anonymous_function = transform_f

    def transform_method_call(self, node, in_block=False, assignment=None):
        if self.method_name:
            node.message = getattr(self, 'convert_to_%s' % self.method_name)(node.message)
        node.receiver = self.transform(node.receiver)
        node.args = self.transform(node.args)
        return node

    def convert_to_pascal_case(self, name):
        return ''.join(q.title() for q in self.words(name))

    def convert_to_camel_case(self, name):
        words = self.words(name)
        return words[0] + ''.join(q.title() for q in words[1:])

    def convert_to_snake_case(self, name):
        return '_'.join(self.words(name))

    def words(self, name):
        if not isinstance(name, str):
            import pdb;pdb.set_trace()
        if '_' in name:
            return [n.lower() for n in name.split('_')]
        else:
            words = [name[0]]
            for c in name[1:]:
                if c.isupper():
                    words.append(c.lower())
                else:
                    words[-1] += c
            return words
