from pseudon.pseudon_tree import Node


class TreeTransformer:
    '''
    visits recursively nodes of the tree
    with defined transform_<node_type> methods and transforms in place
    '''

    def transform(self, tree):
        if isinstance(tree, Node):
            if hasattr(self, 'transform_%s' % tree.type):
                return getattr(self, 'transform_%s' % tree.type)(tree)
            else:
                return self.transform_default(tree)
        elif isinstance(tree, list):
            return [self.transform(child) for child in tree]
        else:
            return tree

    def transform_default(self, tree):
        for field, child in tree.__dict__.items():
            if not field.endswith('type'):
                if isinstance(tree, (list, Node)):
                    setattr(tree, field, self.transform(child)
        return tree
