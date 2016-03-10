from pseudo.middlewares.middleware import Middleware
from pseudo.pseudo_tree import Node

class AugAssignmentMiddleware(Middleware):
    '''
    changes `%<x> = %<x> op %<value>`  to `%<x> += %<value>` nodes
    `
    '''

    @classmethod
    def process(cls, tree):
        return cls().transform(tree)

    def transform_assignment(self, node, in_block=False, assignment=None):
        if node.value.type == 'binary_op' and node.target == node.value.left:
            return Node('aug_assignment', 
                        op=node.value.op,
                        target=node.target,
                        value=node.value.right)
        else:
            return node

