from pseudon.pseudon_tree import Node


class TreeTransformer:
    '''
    visits recursively nodes of the tree
    with defined transform_<node_type> methods and transforms in place
    '''

    before = None
    after = None

    def transform(self, tree, in_block=False, assignment=None):
        if isinstance(tree, Node):
            if self.before:
                tree = self.before(tree, in_block, assignment)
            handler = getattr(self, 'transform_%s' % tree.type, None)
            if handler:
                tree = handler(tree, in_block, assignment)
            else:
                tree = self.transform_default(tree)
            if self.after:
                tree = self.after(tree, in_block, assignment)
            return tree
        elif isinstance(tree, list):
            return [self.transform(child) for child in tree]
        else:
            return tree

    def transform_default(self, tree):
        for field, child in tree.__dict__.items():
            if not field.endswith('type'):
                print(field)
                if isinstance(child, Node):
                    print(getattr(child, 'value', None))
                    print(getattr(child, 'name', None))
                # input()
                if isinstance(child, Node):
                    setattr(tree, field, self.transform(child, False, tree if tree.type[-10:] == 'assignment' else None))
                elif isinstance(child, list) and field == 'block' or field == 'main':
                    setattr(tree, field, self.transform_block(child))
                elif isinstance(child, list):
                    setattr(tree, field, self.transform(child))
        return tree

    def transform_block(self, tree):
        results = []
        for child in tree:
            result = self.transform(child, True)
            if not isinstance(result, list):
                result.append(result)
            else:
                results += result
        return results
