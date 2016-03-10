from pseudo.tree_transformer import TreeTransformer

class Middleware(TreeTransformer):
    def function_walk(self, node):
        for j, child in enumerate(node.definitions):
            if child.type == 'function_definition':
                node.definitions[j] = self.transform_special_f(child)
            elif child.type == 'class_definition':
                self.current_class = child
                if child.constructor:
                    child.constructor = self.transform_special_f(child.constructor)
                for k, definition in enumerate(child.methods):
                    child.methods[k] = self.transform_special_f(definition)
        return node