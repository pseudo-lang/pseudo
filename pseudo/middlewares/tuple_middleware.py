from pseudo.middlewares.middleware import Middleware
from pseudo.pseudo_tree import Node, assignment, local, attr, typename
from pseudo.tree_transformer import TreeTransformer
from pseudo.helpers import safe_serialize_type, general_type, camel_case

class TupleMiddleware(Middleware):
    '''
    middleware for expressing tuples with structs

    currently used with go(to translate all tuples, because no generics)
    and with c#/c++
    (in the future we can also generate NamedTuples for python,
     but for now arrays/lists are capable enough in dynamic languages)
    if Tuple[A, B] is used, create a class/struct with immutable
    fields with those types, convert the tuple to a struct/class initialize

    It works by:
      
      detecting meaningful names corresponding to a tuple
      in function/method params and call args,

      detecting meaningful names for its fields if it sees a 
      call(..t[0], t[1]..t[-1]) kind of use and convert index accesses
      and tuples for that tuple type to the class equivalents 

    If it can't find a good name, it uses tuples for C#/C++ and
    it uses
    an auto-generated ugly name for Go
    '''

    def process(self, tree):
        self.tree = tree
        self.tuple_definitions = {}
        return self.transform_and_create()

    def __init__(self, all=True):
        self.all = all

    def after(self, n, *z):
        if hasattr(n, 'pseudo_type') and isinstance(n.pseudo_type, list):
            n.pseudo_type = self.clean_tuple_class_type(n.pseudo_type)
        if hasattr(n, 'return_type') and isinstance(n.return_type, list):
            n.return_type = self.clean_tuple_class_type(n.return_type)
        if hasattr(n, 'decl_type') and isinstance(n.decl_type, list):
            n.decl_type = self.clean_tuple_class_type(n.decl_type)
        return n

    def clean_tuple_class_type(self, t):
        if isinstance(t, list):
            if t[0] == 'Tuple':
                a = self.tuple_definitions.get(safe_serialize_type(t))
                if a:
                    return camel_case(a[0])
            t[1:] = [self.clean_tuple_class_type(child) for child in t[1:]]
        return t


    def transform_and_create(self):
        self.tuple_definitions = {}
        self.function_index = {'functions': {}}
        self.params = []
        # detect param class
        self.tree = self.function_walk(self.tree)
        # detect arg fields
        self.tree = ArgWalker(self).transform(self.tree)
        # replace
        self.tree = self.transform(self.tree)
        self.tree.tuple_definitions = [self.with_constructor(t) for t in self.tuple_definitions.values()]
        return self.tree

    def with_constructor(self, t):
        t = t[1]
        t.name = camel_case(t.name)
        if self.all == False:
            t.constructor = Node('constructor',
                params=[local(field.name, field.pseudo_type) for field in t.attrs],
                this=typename(t.name),
                pseudo_type = ['Function'] + [field.pseudo_type for field in t.attrs] + [t.name],
                return_type=t.name,
                block=[
                    assignment(
                        Node('instance_variable', name=field.name, pseudo_type=field.pseudo_type),
                        local(field.name, field.pseudo_type),
                        first_mention=False)
                    for field
                    in t.attrs])
        return t

    def transform_tuple(self, node, in_block=False, assignment=None):
        name = safe_serialize_type(node.pseudo_type)
        if name in self.tuple_definitions:
            return Node('simple_initializer',
                name=camel_case(self.tuple_definitions[name][0]),
                args=node.elements)
        else:
            if self.all: # go: we have to change all tuples
                self.tuple_definitions[name] = Node('class_definition',
                    name=name,
                    base=None,
                    constructor=None,
                    attrs=[Node('immutable_class_attr', name='item%d' % j, is_public=True, pseudo_type=q) for j, q in enumerate(node.pseudo_type[1:])],
                    methods=[])
            else: # c#: we can just use tuples
                return node

    def transform_index(self, n, in_block=False, assignment=None):
        if general_type(n.sequence.pseudo_type) == 'Tuple':
            class_name, class_node = self.tuple_definitions.get(safe_serialize_type(n.sequence.pseudo_type), (None, None))
            # we can have only literal int index of tuple because typecheck
            if class_name:
                return attr(local(n.sequence, class_name), camel_case(class_node.attrs[n.index.value].name), pseudo_type=n.pseudo_type)
        return n

    def transform_special_f(self, n, in_block=False, assignment=None):
        for a in n.params:
            if general_type(a.pseudo_type) == 'Tuple':
                s = safe_serialize_type(a.pseudo_type)
                if s not in self.tuple_definitions:
                    self.tuple_definitions[s] = a, Node('class_definition',
                        name=a.name,
                        base=None,
                        attrs=[Node('immutable_class_attr', name='item%d' % j, is_public=True, pseudo_type=q) for j, q in enumerate(a.pseudo_type[1:])],
                        constructor=None,
                        methods=[])
        if n.type == 'constructor':
            if self.current_class.name not in self.function_index:
                self.function_index[self.current_class.name] = {}
            self.function_index[self.current_class.name]['__init__'] = n
        elif n.type == 'method_definition':
            if self.current_class.name not in self.function_index:
                self.function_index[self.current_class.name] = {}
            self.function_index[self.current_class.name][n.name] = n
        else:
            self.function_index['functions'][n.name] = n

        return n

class BlockRewriter(TreeTransformer):
    def __init__(self, old_params, l):
        self.old_params = old_params
        self.l = l

    def transform_local(self, node, in_block=False, assignment=None):
        if node.name in self.old_params:
            return attr(self.l, camel_case(node.name)) # aware of tuple name updates
        else:
            return node

class ArgWalker(TreeTransformer):
    def __init__(self, tuple_definition):
        self.tuple_definition = tuple_definition

    def transform_general_call(self, n, in_block=False, assignment=None):
        for j, arg in enumerate(n.args):
            if (arg.type == 'local' or arg.type == 'instance_variable' or arg.type == 'attr' or arg.type == 'typename') and general_type(arg.pseudo_type) == 'Tuple':
                name = arg.name if arg.type != 'attr' else arg.attr
                pseudo_type = arg.pseudo_type
            elif arg.type == 'index' and arg.sequence.type in {'local', 'instance_variable', 'attr', 'typename'} and general_type(arg.sequence.pseudo_type) == 'Tuple':
                name = arg.sequence.name if arg.sequence.type != 'attr' else arg.sequence.attr
                pseudo_type = arg.sequence.pseudo_type
            else:
                n.args[j] = self.transform(n.args[j])
                continue
            z = safe_serialize_type(pseudo_type)
            if z not in self.tuple_definition.tuple_definitions:
                self.tuple_definition.tuple_definitions[z] = name, Node('class_definition',
                            name=name,
                            base=None,
                            constructor=None,
                            this=typename(name),
                            attrs=[Node('immutable_class_attr', name='item%d' % k, is_public=True, pseudo_type=t) for k, t in enumerate(pseudo_type[1:])],
                            methods=[])
            else:
                self.tuple_definition.tuple_definitions[z] = name, self.tuple_definition.tuple_definitions[z][1]
            for l in self.tuple_definition.params:
                l.name = name
    
        if n.type == 'call':
            if n.function.type != 'local':
                return n
            namespace, name = 'functions', n.function.name
        elif n.type == 'method_call':
            n.receiver = self.transform(n.receiver)
            namespace, name = general_type(n.receiver.pseudo_type), n.message
        elif n.type == 'new_instance':
            namespace, name = general_type(n.class_name), '__init__'
        else:
            return n

        
        if hasattr(namespace, 'y'):
            input(namespace.y)
        if namespace not in self.tuple_definition.function_index or name not in self.tuple_definition.function_index[namespace]:
            return n

        if self.tuple_index(n):
            pseudo_type = n.args[-1].sequence.pseudo_type
            sequence = n.args[-1].sequence
            
            if len(n.args) >= len(pseudo_type) - 1 and all(self.successive(sequence, j, a) for j, a in enumerate(n.args[-len(pseudo_type) + 1:])):
                # s(a, b[0], b[1]) -> s(a, b) and def s(a, x, y) -> s(a, k_name)
                t = safe_serialize_type(pseudo_type)
                tuple_class_name, class_node = self.tuple_definition.tuple_definitions[t]
                old_params = self.tuple_definition.function_index[namespace][name].params[-len(pseudo_type) + 1:]
                l = local(tuple_class_name, pseudo_type) # referencable if we find another tuple name
                self.tuple_definition.params.append(l)
                self.tuple_definition.function_index[namespace][name].params[-len(pseudo_type) + 1:] = [l]
                self.tuple_definition.function_index[namespace][name] = BlockRewriter({old_param.name for old_param in old_params}, l).transform(self.tuple_definition.function_index[namespace][name])
                self.tuple_definition.function_index[namespace][name].pseudo_type[-len(pseudo_type):-1] = [camel_case(tuple_class_name)]
                for class_attr, name in zip(class_node.attrs, old_params):
                    class_attr.name = name.name
                n.args[-len(pseudo_type) + 1:] = [sequence]
                return n
        return n

    transform_call = transform_method_call = transform_new_instance = transform_general_call


    def tuple_index(self, n):
        '''s[<int>] where s is a Tuple[T1..]'''
        return n.args and n.args[-1].type == 'index' and general_type(n.args[-1].sequence.pseudo_type) == 'Tuple' and\
               n.args[-1].index.type == 'int' and\
               (n.args[-1].index.value == -1 or n.args[-1].index.value == len(n.args[-1].sequence.pseudo_type) - 2)


    def successive(self, sequence, j, a):
        # import pdb;pdb.set_trace()
        return a.type == 'index' and a.sequence.y == sequence.y and\
               a.index.type == 'int' and\
               (j - len(sequence.pseudo_type) + 1 == a.index.value or j == a.index.value)
