from pseudon.middlewares.middleware import Middleware

class GoErrorHandlingMiddleware(Middleware):
    '''
    go: middleware for translation of error handlers

    builtin / custom

    add markers for functions:

    %error can raise an error from function

    [] possible errors

    builtin functions:
      can only raise BuiltinException in pseudo terms
      can raise CustomException in pseudo terms but BuiltinException too

      manually mark the supported functions from the pseudo-go bridge

      then analyze the pseudo tree

      a f:
        if f is calling g: 
          if g is builtin:
            if g raises an error, add BuiltinException to f errors and mark f %error
          else:
            if g is not analyzed:
              a g
            if g is %error look at f possible errors
              if handler in f for them: add an if err and connect them
              if handlers left: mark f %error and add unhandled errors to sig
    ok so it seems it can be done and yepp
    '''

    @classmethod
    def process(cls, tree):
        result = cls(tree).transform(tree)
        return result

    def __init__(self, tree):
        self.function_index = {}

    def transform_module(self, node, in_block=False, assignment=None):
        node.failing_with = []
        node.definitions = self.transform(node.definitions)
        node.main = self.transform(node.main)
        return node

    def transform_f(self, node, in_block=False, assignment=None):
        self.envs.append(set(node.params))
        self.current_function, old_function = node, self.current_function
        node.local_declarations = []
        node.block = self.transform(node.block)
        self.current_function = old_function
        self.envs.pop()
        return node

    transform_function = transform_methods = transfrom_anonymous_function = transform_f

    def transform_assignment(self, node, in_block=False, assignment=None):
        if node.target.type == 'local' and node.target.name not in self.envs[-1]:
            node.first_mention = True
            self.current_function.local_declarations.append(node.target.name)
        else:
            node.first_mention = False
        node.value = self.transform(node.value) # lambda can be somewhere here
        return node

    '''
        also if this.e = ... rewrite to {} constructor and add flag to top
        that uses short syntax
        
        else create newA but
        first n lines this.x = turn to this = A{..}
        and if its a return just return it
    '''
