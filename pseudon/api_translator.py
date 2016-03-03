from pseudon.tree_transformer import TreeTransformer
from pseudon.types import *
from pseudon.env import Env
from pseudon.pseudon_tree import Node, to_node, method_call, call
from pseudon.errors import PseudonStandardLibraryError, PseudonDSLError

def to_op(op, reversed=False):
    '''
    create a function that transforms a method to a binary op

    often we need to convert a pseudon method
    <receiver>.<message>(<z>) to a binary op
    <receiver> <op> <message>
    that's a decorator that helps for that
    '''
    def transformer(receiver, param, pseudo_type):
        if not reversed:
            return Node('binary_op', op=op, left=receiver, right=param, pseudo_type=pseudo_type)
        return Node('binary_op', op=op, left=param, right=receiver, pseudo_type=pseudo_type)
    return transformer


class ApiTranslator(TreeTransformer):

    def __init__(self, tree):
        self.tree = tree

    def api_translate(self):
        self.standard_dependencies = set()
        self.used = set()
        self.weird_assignments = []
        transformed = self.transform(self.tree)

        for l in self.used:
            m = self.dependencies.get(l, {}).get('@all')
            if m:
                self.standard_dependencies.add(m)
        
        transformed.dependencies = [
            Node('dependency', name=name) for name in self.standard_dependencies]

        return transformed

    def after(self, node, in_block, assignment):
        if node and node.type in {'list', 'dictionary', 'set', 'tuple', 'regexp', 'array'}:
            self.used.add(node.type.title())
        elif node and node.type[-10:] == 'assignment':
            print(node.y)
            if node.value_type in {'List', 'Dictionary', 'Set', 'Tuple', 'Regexp', 'Array'}:
                self.used.add(node.value_type)



        if node.type[-10:] == 'assignment' and node.value and node.value.type == 'binary_op':
            
            if node.type == 'instance_assignment':
                print(node.value.left.type == 'instance_variable')
                if node.value.left.type == 'instance_variable':
                    print(node.name == node.value.left.name)
            
            if node.type == 'local_assignment' and node.value.left.type == 'local' and node.local == node.value.left.name or\
               node.type == 'instance_assignment' and node.value.left.type == 'instance_variable' and node.name == node.value.left.name or\
               node.type == 'index_assignment' and node.value.left.type == 'index' and node.index == node.value.left.index and node.sequence == node.value.left.sequence or\
               node.type == 'attr_assignment' and node.attr == node.value.left:
                node = Node('operation_assign', slot=node.value.left, op=node.value.op, value=node.value.right)
        
        if in_block:            
            
            results = [ass for ass in self.weird_assignments]
            if node.type[-10:] != 'assignment' or node.value:
                results.append(node)

            self.weird_assignments = []
            return results
            
        else:
            return node


    def transform_standard_method_call(self, node, in_block=False, assignment=None):
        # print('TRANSLATE METHOD', node)
        l = node.receiver.pseudo_type
        if isinstance(l, list):
            l = l[0]

        node.args = [self.transform(arg) for arg in node.args]
        node.receiver = self.transform(node.receiver)
        
        if 'standard_method_call' in self.weird and l in self.weird['standard_method_call'] and node.message in self.weird['standard_method_call'][l]:
            return self.weird_call('standard_method_call', l, node.message, node, assignment)

        elif l not in self.methods:
            raise PseudonStandardLibraryError(
                'pseudon doesn\'t recognize %s as a standard type' % l)
        elif node.message not in self.methods[l]:
            raise PseudonStandardLibraryError(
                'pseudon doesn\'t have a %s#%s method' % (l, node.message))

        for a in node.args:
            print(a.y)
        self.update_dependencies(l, node.message, [a.pseudo_type for a in node.args])
        return self._expand_api(self.methods[l][node.message], node.receiver, node.args, node.pseudo_type, self.methods[l]['@equivalent'])

    def weird_call(self, node_type, namespace, function, node, assignment):
        w = self.weird[node_type][namespace][function]
        if assignment:
            ass = assignment
        else:
            ass = Node('local_assignment', 
                pseudo_type='Void', value_type=node.pseudo_type[-1], local=w['_temp_name'])
        if node_type == 'standad_method_call':
            ass = w['_translate'](ass, namespace, function, node.receiver, node.args)
        else:
            ass = w['_translate'](ass, namespace, function, node.args)
        if assignment is None:
            self.weird_assignments.append(ass)
            return local(w['_temp_name'])
        else:
            self.weird_assignments.append(ass)
            return []

    def transform_standard_call(self, node, in_block=False, assignment=None):
        # print('TRANSLATE CALL', node)
        namespace = node.namespace or 'global'
        node.args = [self.transform(arg) for arg in node.args]
        if 'standard_call' in self.weird and namespace in self.weird['standard_call'] and node.function in self.weird['standard_call'][namespace]:
            return self.weird_call('standard_call', node.namespace, node.function, node, assignment)
        elif namespace not in self.functions:
            raise PseudonStandardLibraryError(
                'pseudon doesn\'t have a %s namespace' % namespace)
        elif node.function not in self.functions[namespace]:
            raise PseudonStandardLibraryError(
                'pseudon doesn\'t have a %s:%s function' % (namespace, node.function))

        self.update_dependencies(namespace, node.function, [a.pseudo_type for a in node.args])
        return self._expand_api(self.functions[namespace][node.function], None, node.args, node.pseudo_type, node.namespace)

    def update_dependencies(self, namespace, function, arg_types):
        if namespace == 'List':
            self.used_list = True
        elif namespace == 'Dictionary':
            self.used_dictionary = True

        for a in arg_types:
            if isinstance(a, list):
                if a[0] == 'List':
                    self.used_list = True
                elif a[0] == 'Dictionary':
                    self.used_dictionary = True

        if namespace not in self.dependencies:
            return

        for e0 in ['@all', function]:
            if e0 in self.dependencies[namespace]:
                e1 = self.dependencies[namespace][e0]
                if isinstance(e1, list):
                    for f in e1:
                        self.standard_dependencies.add(f)
                else:
                    self.standard_dependencies.add(e1)


    def _expand_api(self, api, receiver, args, pseudo_type, equivalent):
        '''
        the heart of api translation dsl

        function or <z>(<arg>, ..) can be expanded, <z> can be just a name for a global function, or #name for method, <arg> can be %{self} for self or %{n} for nth arg
        '''

        if callable(api):
            if receiver:
                return api(receiver, *(args + [pseudo_type]))
            else:
                return api(*(args + [pseudo_type]))
        elif isinstance(api, str):
            if '(' in api:
                call_api, arg_code = api[:-1].split('(')
                args = [self._parse_part(
                    a.strip(), receiver, args, equivalent) for a in arg_code.split(',')]
            else:
                call_api, arg_code = api, ''
            if '#' in call_api:
                a, b = call_api.split('#')
                method_receiver = self._parse_part(
                    a, receiver, args, equivalent) if a else receiver
                return method_call(method_receiver, b, args, pseudo_type=pseudo_type)
            elif '.' in call_api:
                a, b = call_api.split('.')
                static_receiver = self._parse_part(
                    a, receiver, args, equivalent) if a else receiver
                if b[-1] != '!':
                    return Node('static_call', receiver=static_receiver, message=b, args=args, pseudo_type=pseudo_type)
                else:
                    return Node('attr', object=static_receiver, attr=b[:-1], pseudo_type=pseudo_type)
            else:
                if receiver:
                    return call(call_api, [receiver] + args, pseudo_type=pseudo_type)
                else:
                    return call(call_api, args, pseudo_type=pseudo_type)
        else:
            raise PseudonDSLError('%s not supported by api dsl' % str(api))

    def _parse_part(self, part, receiver, args, equivalent):
        if part[0] == '%':  # %{v}
            inside = part[2:-1]
            if inside.isnum():
                inside = int(inside)
                return args[inside]
            elif inside == 'self':
                if receiver:
                    return receiver
                else:
                    raise PseudonDSLError(
                        '%{self} not working for functions with api dsl')
            elif inside == 'equivalent':
                return to_node(equivalent)
            else:
                return getattr(self, '%s_placeholder' % inside)(receiver, *args, equivalent=equivalent)
        else:
            return to_node(part)
