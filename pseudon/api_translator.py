from pseudon.tree_transformer import TreeTransformer
from pseudon.types import *
from pseudon.env import Env
from pseudon.pseudon_tree import Node


class ApiTranslator(TreeTransformer):

    def __init__(self):
        pass
        # self.env = Env()
        # self.current_class = None

    def api_translate(typed_tree):
        return self.transform(typed_tree)

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
            node = self._expand_api(self.api[l][
                                    node.message.name], node.receiver, node.args, node.pseudon_type) or node
        return node

    def _expand_api(self, api, receiver, args, pseudon_type):
        if isinstance(api, dict):
            for j, path in api.items():
                if self._match_api(pseudon_type, j, args):
                    args = [arg for arg, other
                            in zip(pseudon_type, j)
                            if isinstance(other, PseudonType)]
                    return self._expand_api(path, receiver, args, pseudon_type)
        elif not isinstance(api, str):
            return
        elif api[0] == '#':
            return Node('method_call', {receiver: receiver, message: api[1:], args: args})
        elif api[0] == '.':
            return Node('attr', {receiver: receiver, slot: api[1:]})

    def _match_api(self, original, api_type, args):
        for o, a, r in zip(original, api_type, args):
            if not (isinstance(a, PseudonType) and o.is_compatible_with(a) or
                    getattr(r, 'value', None) == a):
                return False
        return True

    def _to_pseudon_type(self, value):
        if hasattr(pseudon.types, str):
            return getattr(pseudon.types, str)
        else:
            return pseudon.CustomType(value)
