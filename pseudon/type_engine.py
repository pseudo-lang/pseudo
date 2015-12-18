from pseudon.tree_transformer import TreeTransformer
from pseudon.env import Env
import pseudon.types


class TypeEngine(TreeTransformer):

    def __init__(self):
        self.env = Env()
        self.scope = 'static'
        self.types = TYPES

    def inference(self, tree):
        # go thru stuff
        # on assign, hints, literals add types

        return self.transform(tree)

    def transform_function(self, node):
        self.env.values[node.name] = self.to_type(node.type_hint[-1])
        node.pseudon_type = [self.to_type(
            arg.type_hint) for arg in node.args] + [self.env.values[node.name]]
        self.env = self.env.child_env(
            {arg.name: self.to_type(arg.type_hint) for arg in node.args})
        node.body = self.transform(node.body)
        self.env = self.env.motherify()
        return node

    def transform_assignment(self, node):
        self.transform(node.right)
        self.env[node.left.name] = node.right.pseudon_type
        node.left.pseudon_type = node.right.pseudon_type
        return node

    def transform_int(self, node):
        node.pseudon_type = Int
        return node

    def to_type(self, type_hint):
        if isinstance(type_hint, str):
            if type_hint in self.types:
                return self.types[type_hint]
            else:
                return CustomType(type_hint)
        elif isinstance(type_hint, list):
            return GenericInstance(List, self.to_type(type_hint[0]))
        elif isinstance(type_hint, dict):
            return GenericInstance(Dictionary, self.to_type(type_hint.keys[-1]), self.to_type(type_hint.values[-1]))
        elif isinstance(type_hint, int):
            return Int
        else:
            raise TypeError("Unmatchable type hint %s" % str(type_hint))
