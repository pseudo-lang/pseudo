from pseudon.tree_transformer import TreeTransformer
from pseudon.types import *
from pseudon.env import Env
from pseudon.pseudon_tree import Node, to_node, method_call, call
from pseudon.errors import PseudonStandardLibraryError, PseudonDSLError

class ApiTranslator(TreeTransformer):

    def __init__(self, tree):
        self.tree = tree

    def api_translate(self):
        return self.transform(self.tree)

    def transform_standard_method_call(self, node):
        print('TRANSLATE METHOD', node)
        l = node.receiver.pseudon_type
        if l not in self.api:
            raise PseudonStandardLibraryError('pseudon doesn\'t recognize %s as a standard type' % l)
        if node.message.name not in self.api[l]:
            raise PseudonStandardLibraryError('pseudon doesn\'t have a %s#%s method' % (l, node.message.name))            
        return self._expand_api(self.api[l][node.message.name], node.receiver, node.args, self.api[l]['@equivalent'])

    def transform_standard_call(self, node):
        print('TRANSLATE CALL', node)
        namespace = node.namespace or 'global'
        if namespace not in self.functions:
            raise PseudonStandardLibraryError('pseudon doesn\'t have a %s namespace' % namespace)
        if node.function not in self.functions[namespace]:
            raise PseudonStandardLibraryError('pseudon doesn\'t have a %s:%s function' % (namespace, node.function))

        return self._expand_api(self.functions[namespace][node.function], None, node.args, node.namespace)
        
    def _expand_api(self, api, receiver, args, equivalent):
        '''
        the heart of api translation dsl

        function or <z>(<arg>, ..) can be expanded, <z> can be just a name for a global function, or #name for method, <arg> can be %{self} for self or %{n} for nth arg
        '''

        if callable(api):
            return api(*([receiver] + args))
        elif isinstance(api, str):
            if '(' in api:
                call_api, arg_code = api[:-1].split('(')
                args = [self._parse_part(a.strip(), receiver, args, equivalent) for a in arg_code.split(',')]
                is_call = True
            else:
                call_api, arg_code, is_call = api, '', False
            if '#' in call_api:
                a, b = call_api.split('#')
                method_receiver = self._parse_part(a, receiver, args, equivalent) if a else receiver
                return method_call(method_receiver, b, args)
            elif '.' in call_api:
                a, b = call_api.split('.')
                static_receiver = self._parse_part(a, receiver, args, equivalent) if a else receiver
                if is_call:
                    return Node('static_call', receiver=static_receiver, message=b, args=args)
                else:
                    return Node('attr', object=static_receiver, attr=b)
            else:
                return call(call_api, args)
        else:
            raise PseudonDSLError('%s not supported by api dsl' % str(api))

    def _parse_part(self, part, receiver, args, equivalent):
        if part[0] == '%': #%{v}
            inside = part[2:-1]
            if inside.isnum():
                inside = int(inside)
                return args[inside]
            elif inside == 'self':
                if receiver:
                    return receiver
                else:
                    raise PseudonDSLError('%{self} not working for functions with api dsl')
            elif inside == 'equivalent':
                return to_node(equivalent)
            else:
                return getattr(self, '%s_placeholder' % inside)(receiver, *args, equivalent=equivalent)
        else:
            return to_node(part)
