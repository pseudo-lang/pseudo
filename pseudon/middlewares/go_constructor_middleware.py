from pseudon.middlewares.middleware import Middleware
from pseudon.pseudon_tree import Node, assignment
from pseudon.tree_transformer import TreeTransformer

class GoConstructorMiddleware(Middleware):
    '''
    go: middleware for translation of constructors

    translate constructor calls which just initialize
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
        s = ConstructorTransformer()
        tree = s.transform(tree)
        result = cls(tree, s.classes_with_simple_initializers).transform(tree)
        return result

    def __init__(self, tree, classes_with_simple_initializers):
        self.current_class, self.current_function = None, None
        self.classes_with_simple_initializers = classes_with_simple_initializers

    def transform_new_instance(self, node, in_block=False, assignment=None):
        if isinstance(node.pseudo_type, str) and node.pseudo_type in self.classes_with_simple_initializers:
            return Node('_go_simple_initializer', name=typename(node.pseudo_type, node.pseudo_type), args=node.args)
        else:
            return node

class ConstructorTransformer(TreeTransformer):
    whitelist = {'class_definition', 'constructor'}
    
    def __init__(self):
        self.classes_with_simple_initializers = set()

    def transform_constructor(self, node, in_block=False, assignment=None):
        simple_initializer = True
        simple_args = []

        for e, a in zip(node.block, self.current_class.attrs):
            if e.type == 'assignment' and e.target.type == 'instance_variable' and e.target.name == a.name:
                simple_args.append(e.value)
                if e.value.type != 'local' or e.value.name != a.name:
                    simple_initializer = False
            else:
                break

        if simple_initializer:
            self.classes_with_simple_initializers.add(self.current_class.name)
            return []
        
        else:
            ass = assignment(Node('this', pseudo_type=self.current_class.name), 
                Node('_go_simple_initializer', name=typename(self.current_class.name, self.current_class), args=simple_args))
            node.block = [ass] + node.block[len(simple_args):]
            return node

# go is a really simple language and one of its 
# strengths is that a shitload of stuff is completely
# different than in all other mainstream languages
# but hey, at least it doesn't have erlang syntax right
# or elixir macroses, *faints when imagining so much power
# in a programming language*
