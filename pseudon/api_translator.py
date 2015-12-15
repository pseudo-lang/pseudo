from pseudon.tree_transformer import TreeTransformer


class ApiTranslator(TreeTransformer):

    def api_translate(typed_tree):
        return self.transform(typed_tree)

    def transform_call(self, node):
        return node
