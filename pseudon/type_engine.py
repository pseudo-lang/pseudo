from pseudon.tree_transformer import TreeTransformer
from pseudon.env import Env
import pseudon.types


class TypeEngine(TreeTransformer):

    def __init__(self):
        self.env = Env()
        self.scope = 'static'

    def inference(self, tree):
        # go thru stuff
        # on assign, hints, literals add types
        return self.transform(tree)

    def transform_function(self, node):
        self.env = self.env.child_env({arg.name: = self.to_type(arg.type_hint) for arg in node.args})
        node.body = self.transform(node.body)
        self.env.motherify()
        return node

    def to_type(self, type_hint):
        return getattr(pseudon.types, type_hint)()
