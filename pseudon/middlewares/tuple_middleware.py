from pseudon.middlewares.middleware import Middleware
from pseudon.pseudon_tree import Node, assignment
from pseudon.tree_transformer import TreeTransformer
from pseudon.helpers import safe_serialize_type

class TupleMiddleware(Middleware):
    '''
    middleware for expressing tuples with structs

    currently used only with go (surprisingly)
    (rationale: arrays/lists are capable enough in dynamic languages
     and c++/c# support generic types)
    if Tuple[A, B] is used, create a struct like that and convert the tuple to a struct
    values to {} initializers
    translate constructors starting with nodes like
      newA(b int, x int) ..
        this.z = b + x
        this.z2 = b
        other
    to nodes like
      newA(b int, x int) ..
        this = A{b + x, b}
        other
    '''

    @classmethod
    def process(cls, tree):
        return cls(tree).transform_and_create()

    def __init__(self, tree):
        self.tree = tree
        self.tuple_definitions = {}

    def transform_and_create(self):
        self.tree = self.transform(self.tree)
        self.tree.tuple_definitions = []
        for t, types in self.tuple_definitions.items():
            self.tree.tuple_definitions.append(
                Node('class_definition',
                    name=t,
                    base=None,
                    constructor=None,
                    attrs=[Node('class_attr', name='item%d' % x, is_public=True, pseudo_type=g) for x, g in enumerate(types)],
                    methods=[]))
        return self.tree

    def transform_tuple(self, node, in_block=False, assignment=None):
        name = safe_serialize_type(node.pseudo_type)
        self.tuple_definitions[name] = node.pseudo_type[1:]
        return Node('_go_simple_initializer', 
            name=name,
            args=node.elements)
