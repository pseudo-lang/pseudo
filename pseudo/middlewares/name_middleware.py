from pseudo.middlewares.middleware import Middleware

class NameMiddleware(Middleware):
    '''
    changes names according to language conventions

    can accept rules for normal_name, method_name and function_name
    available rules: snake_case, camel_case, pascal_case

    currently used c#, go, javascript and php
    '''

    def __init__(self, normal_name=None, method_name=None, function_name=None, attr_name=None):
        self.normal_name = normal_name
        self.method_name = method_name
        self.function_name = function_name
        self.attr_name = attr_name
        self.current_class_ = None

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
            pass
            # print('NORM', node.name.y)
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

    def transform_this_method_call(self, node, in_block=False, assignment=None):
        if self.method_name:
            node.message = getattr(self, 'convert_to_%s' % self.method_name)(node.message)
        node.args = self.transform(node.args)
        return node

    def transform_attr(self, node, in_block=False, assignment=None):
        if self.attr_name:
            node.attr = getattr(self, 'convert_to_%s' % self.attr_name)(node.attr)
        node.object = self.transform(node.object)
        return node
    
    def transform_class_definition(self, node, in_block=False, assignment=None):
        self.current_class_ = node
        node.attrs = [self.transform_attr_name(child) for child in node.attrs]
        node.constructor = self.transform(node.constructor)
        node.methods = self.transform(node.methods)
        return node

    def transform_attr_name(self, node, in_block=False, assignment=None):
        if self.attr_name:
            if node.type == 'instance_variable' and self.current_class_:
                for l in self.current_class_.attrs:
                    if l.name.lower() == node.name.replace('_', ''):
                        node.name = l.name
                        if l.is_public:
                            node.name = node.name[0].upper() + node.name[1:]
                        else:
                            node.name = node.name[0].lower() + node.name[1:]
                        return node
            node.name = getattr(self, 'convert_to_%s' % self.attr_name)(node.name)
            if node.type in ['class_attr', 'immutable_class_attr'] and node.is_public:
                node.name = node.name[0].upper() + node.name[1:]
            elif node.type in ['class_type', 'immutable_class_attr'] or node.type == 'instance_variable' and not self.current_class_:
                node.name = node.name[0].lower() + node.name[1:]

        return node

    transform_class_attr = transform_instance_variable = transform_immutable_class_attr = transform_attr_name
    
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
        if '_' in name[1:]:
            z = [n.lower() for n in name.split('_')]
            # if name[0] == '_':
            #     z[:2] = ['_%s' % z[1]]
            return z
        else:

            words = [name[0]]
            for c in name[1:]:
                if c.isupper():
                    words.append(c.lower())
                else:
                    words[-1] += c
            # if name[0] == '_' and name[1:]:
            #     input(words)
            return words
