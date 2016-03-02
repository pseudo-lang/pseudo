from pseudon.tree_transformer import TreeTransformer
from pseudon.types import *
from pseudon.env import Env
from pseudon.pseudon_tree import Node, to_node, method_call, call
from pseudon.errors import PseudonStandardLibraryError, PseudonDSLError


class ApiTranslator(TreeTransformer):

    def __init__(self, tree):
        self.tree = tree

    def api_translate(self):
        self.standard_dependencies = set()
        transformed = self.transform(self.tree)
        transformed.dependencies = [
            Node('dependency', name=name) for name in self.standard_dependencies]
        return transformed

    def transform_standard_method_call(self, node):
        # print('TRANSLATE METHOD', node)
        l = node.receiver.pseudo_type
        if '[' in l:
            l = l[:l.find('[')]
        if l not in self.methods:
            raise PseudonStandardLibraryError(
                'pseudon doesn\'t recognize %s as a standard type' % l)
        if node.message not in self.methods[l]:
            raise PseudonStandardLibraryError(
                'pseudon doesn\'t have a %s#%s method' % (l, node.message))

        self.update_dependencies(l, node.message)
        return self._expand_api(self.methods[l][node.message], node.receiver, node.args, self.methods[l]['@equivalent'])

    def transform_standard_call(self, node):
        # print('TRANSLATE CALL', node)
        namespace = node.namespace or 'global'
        if namespace not in self.functions:
            raise PseudonStandardLibraryError(
                'pseudon doesn\'t have a %s namespace' % namespace)
        if node.function not in self.functions[namespace]:
            raise PseudonStandardLibraryError(
                'pseudon doesn\'t have a %s:%s function' % (namespace, node.function))

        self.update_dependencies(namespace, node.function)
        return self._expand_api(self.functions[namespace][node.function], None, node.args, node.namespace)

    def update_dependencies(self, namespace, function):
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

    def _expand_api(self, api, receiver, args, equivalent):
        '''
        the heart of api translation dsl

        function or <z>(<arg>, ..) can be expanded, <z> can be just a name for a global function, or #name for method, <arg> can be %{self} for self or %{n} for nth arg
        '''

        if callable(api):
            if receiver:
                return api(receiver, *args)
            else:
                return api(*args)
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
                return method_call(method_receiver, b, args)
            elif '.' in call_api:
                a, b = call_api.split('.')
                static_receiver = self._parse_part(
                    a, receiver, args, equivalent) if a else receiver
                if b[-1] != '!':
                    return Node('static_call', receiver=static_receiver, message=b, args=args)
                else:
                    return Node('attr', object=static_receiver, attr=b[:-1])
            else:
                if receiver:
                    return call(call_api, [receiver] + args)
                else:
                    return call(call_api, args)
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
