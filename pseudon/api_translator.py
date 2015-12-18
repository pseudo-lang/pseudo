from pseudon.tree_transformer import TreeTransformer
from pseudon.types import *
from pseudon.env import Env
from pseudon.pseudon_tree import Node, to_node


class ApiTranslator(TreeTransformer):
    '''Api translator'''

    def __init__(self, tree):
        self.tree = tree

    def api_translate(self):
        return self.transform(tree)

    # def tranform_class(self, node):
    #     self.env[node.name] = node.pseudon_type
    #     self.env[node.name].methods = {}
    #     self.current_class = self.env[node.name]
    #     node.methods = self.transform(node.methods)
    #     self.current_class = None  # currently one level of classes allowed
    #     return node

    # def transform_function(self, node):
    #     if self.current_class:
    #         self.current_class[node.name] = node.pseudon_type
    #     else:
    #         self.env[node.name] = node.pseudon_type
    #     self.env = self.env.child_env()
    #     node.body = self.transform(node.body)
    #     self.env = self.env.parent
    #     return node

    def transform_method_call(self, node):
        l = node.receiver.pseudon_type.label
        if l in self.api and node.message.name in self.api[l]:
            node = self._expand_api(self.api[l][node.message.name], node.receiver, node.args, self.api[l]['@equivalent']) or node
        return node

    def _expand_api(self, api, receiver, args, equivalent):
        if callable(api):
            return api(receiver, *args)
        elif isinstance(api, str):
            if '(' in api:
                call, arg_code = api[:-1].split('(')
                args = [self._parse_part(a.strip(), receiver, args, equivalent) for a in arg_code.split(',')]
            else:
                call, arg_code = api, ''
            
            if '#' in call:
                a, b = call.split('#')
                method_receiver = self._parse_part(a, receiver, args, equivalent) if a else receiver
                return Node('method_call', receiver=method_receiver, message=b, args=args)
            elif '.' in call:
                a, b = call.split('.')
                static_receiver = self._parse_part(a, receiver, args, equivalent) if a else receiver
                if arg_code:
                    return Node('static_call', receiver=static_receiver, message=b, args=args)
                else:
                    return Node('attr', object=static_receiver)
            else:
                return Node('call', message=call, args=[])
        else:
            return

    def _parse_part(self, part, receiver, args, equivalent):
        if part[0] == '%': #%{v}
            inside = part[2:-1]
            if inside.isnum():
                inside = int(inside)
                return args[inside]
            elif inside == 'self':
                return receiver
            elif inside == 'equivalent':
                return to_node(equivalent)
            else:
                return getattr(self, '%s_placeholder' % inside)(receiver, *args, equivalent=equivalent)
        else:
            return to_node(part)
