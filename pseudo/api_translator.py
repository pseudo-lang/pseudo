from pseudo.tree_transformer import TreeTransformer
from pseudo.pseudo_tree import Node, to_node, method_call, call, local
from pseudo.errors import PseudoStandardLibraryError, PseudoDSLError
from pseudo.api_handlers import LeakingNode, NormalLeakingNode, BizarreLeakingNode
import copy

TYPES = {'List', 'Dictionary', 'Set', 'Tuple', 'Regexp', 'Array', 'String'}

def to_op(op, reversed=False):
    '''
    create a function that transforms a method to a binary op

    often we need to convert a pseudo method
    <receiver>.<message>(<z>) to a binary op
    <receiver> <op> <message>
    that's a decorator that helps for that
    '''
    def transformer(receiver, param, pseudo_type):
        if not reversed:
            return Node('binary_op', op=op, left=receiver, right=param, pseudo_type=pseudo_type)
        return Node('binary_op', op=op, left=param, right=receiver, pseudo_type=pseudo_type)
    return transformer


class ApiTranslator(TreeTransformer):
    '''
    A base class for the api translators

    DSL:
    you can use either 
      a lambda/function defined in <lang>_api_handlers.py which returns a Node with signature
    `(receiver, *args)` (e.g. `lambda receiver, value: Node('none'))
    or
      a <Name> class inheriting from LeakingNode 
      which can inject nodes in the closest block
    or

    shortcuts:
    '#method_name'  => calls that method of the receiver with the same args
    'function_name' => calls that function with the same args
    'namespace.function_name' => calls the function in the namespace
    '.attr_name!'   => accesses that attribute of the receiver
    '.method_name'  => calls that static method
    `to_op(op)`     => transforms `receiver.method(arg)` to a `receiver op arg` binary

    `class_name<shortcut>` =>
        transforms into the method/attr according to previous rules but of the class_name class,
        not the equivalent one

    `<shortcut>(%{0}, %{self})` =>
        transforms into the call according to previous rules but with args ordered like in the
        placeholders

        %{<number>}      => the n-th arg(starts from 0)
        %{self}          => the receiver of the method
        %{equivalent}    => the equivalent class
        %{<other-name>}  => each language translator can redefine it with
                            def <other-name>_placeholder(self, receiver, *args, equivalent) which
                            should return a Node


    Nodes: Nodes can be either the official pseudo nodes or in special cases
           with `_<special_node>` when they describe syntax typical only for
           the target language of the translator

    helpers: quite useful helpers from pseudo.pseudo_tree are
             `method_call(receiver: str/Node, message: str, args: [Node])`
                 which helps with method call nodes with normal `local` name object receivers

             `call(callee: str/Node, args: [Node])`
                 which helps with call nodes with normal `local` name callees
    '''

    def __init__(self, tree):
        self.tree = copy.deepcopy(tree)

    def api_translate(self):
        self.standard_dependencies = set()
        self.used = set()
        self.leaked_nodes = []
        transformed = self.transform(self.tree)

        for l in self.used:
            m = self.dependencies.get(l, {}).get('@all')
            if m:
                if isinstance(m, list):
                    self.standard_dependencies |= set(m)
                else:
                    self.standard_dependencies.add(m)
        
        transformed.dependencies = [
            Node('dependency', name=name) for name in self.standard_dependencies]

        return transformed

    def after(self, node, in_block, assignment):
        if node and not isinstance(node, Node):
            return node
        if node:
            if node.type.title() in TYPES:
                self.used.add(node.type.title())
            # elif isinstance(node, list) and node.type[0] in TYPES:
            #     self.used.add(node.type[0].title())
        if node and (node.type == 'try_statement' or node.type == 'throw_statement'):
            self.used.add('Exception')
        if node and node.type == 'assignment' and node.value:
            self.update_used(node.value.pseudo_type)

        if node and node.type == 'assignment' and node.value and node.value.type == 'binary_op':
            if node.value.right == node.target:
                node = Node('operation_assign', slot=node.value.left, op=node.value.op, value=node.value.right)
        
        if node and hasattr(node, 'params'):
            self.update_used(node.pseudo_type)

        if node and node.type == 'static_call':
            if node.receiver.type == 'local' and hasattr(self, 'js_dependencies') and node.receiver.name in self.js_dependencies:
                self.standard_dependencies.add(self.js_dependencies[node.receiver.name])                

        if in_block:
            results = [ass for ass in self.leaked_nodes]
            # input(type(self).__name__ )
            if type(self).__name__ == 'GolangTranslator':
                2# 2 input(node)
            if node and not (node.type == 'assignment' and node.value is None):
                results.append(node)
            self.leaked_nodes = []
            return results
            
        else:
            return node


    def transform_standard_method_call(self, node, in_block=False, assignment=None):
        l = node.receiver.pseudo_type
        if isinstance(l, list):
            l = l[0]


        node.args = [self.transform(arg) for arg in node.args]
        node.receiver = self.transform(node.receiver)
        
        if l not in self.methods:
            raise PseudoStandardLibraryError(
                '%s doesn\'t recognize %s as a standard type' % (type(self).__name__, l))
        elif node.message not in self.methods[l]:
            raise PseudoStandardLibraryError(
                '%s doesn\'t have a %s#%s method' % (type(self).__name__, l, node.message))
        
        x = self.methods[l][node.message]
        if isinstance(x, type) and issubclass(x, LeakingNode):
            if in_block:
                args = ['block']
            elif assignment:
                args = ['assignment', assignment.target]
            else:
                args = ['expression']

            result = self.leaking(x, l, node.message, node, *args)
        else:
            result = self._expand_api(x, node.receiver, node.args, node.pseudo_type, self.methods[l]['@equivalent'])
        self.update_dependencies(l, node.message, [a.pseudo_type for a in node.args])
        return result        

    def leaking(self, z, module, name, node, context, *data):
        '''
        an expression leaking ...

        assignment nodes into the nearest block list of nodes
        c++ guys, stay calm
        '''

        # input(node.y)
        args = [node.receiver] + node.args if node.type == 'standard_method_call' else node.args
        z = z(module, name, args)
        if context == 'expression':
            if isinstance(z, NormalLeakingNode):
                leaked_nodes, exp = z.as_expression()
            else:
                leaked_nodes, exp = z.as_expression()
                zz = local(z.temp_name(getattr(z, 'default', '')), node.pseudo_type)
                leaked_nodes = z.as_assignment(zz)
                exp = local(zz, node.pseudo_type)
            if exp is None or exp.pseudo_type == 'Void':
                raise PseudoTypeError("pseudo can't handle values with void type in expression: %s?%s" % (module, name))
            self.leaked_nodes += leaked_nodes
            return exp
        elif context == 'assignment':
            if isinstance(z, NormalLeakingNode):
                leaked_nodes, exp = z.as_expression()
                if exp is None or exp.pseudo_type == 'Void':
                    raise PseudoTypeError("pseudo can't handle values with void type in expression: %s?%s" % (module, name))
                self.leaked_nodes += leaked_nodes
                return assignment(data[0], exp)
            else:
                self.leaked_nodes += z.as_assignment(data[0])
                return None
        elif context == 'block':
            leaked_nodes, exp = z.as_expression()
            self.leaked_nodes += leaked_nodes
            return exp

    def transform_standard_call(self, node, in_block=False, assignment=None):
        namespace = node.namespace or 'global'
        node.args = [self.transform(arg) for arg in node.args]
        if namespace not in self.functions:
            raise PseudoStandardLibraryError(
                '%s doesn\'t have a %s namespace' % (type(self).__name__, namespace))
        elif node.function not in self.functions[namespace]:
            raise PseudoStandardLibraryError(
                '%s doesn\'t have a %s:%s function' % (type(self).__name__, namespace, node.function))
        
        x = self.functions[namespace][node.function]
        if isinstance(x, type) and issubclass(x, LeakingNode):
            if in_block:
                args = ['block']
            elif assignment:
                args = ['assignment', assignment.target]
            else:
                args = ['expression']

            result = self.leaking(x, namespace, node.function, node, *args)
        else:
            result = self._expand_api(x, None, node.args, node.pseudo_type, node.namespace)
        self.update_dependencies(namespace, node.function, [a.pseudo_type for a in node.args])
        return result

    def update_dependencies(self, namespace, function, arg_types):
        if namespace in TYPES:
            self.used.add(namespace)

        for a in arg_types:
            self.update_used(a)

        if namespace not in self.dependencies:
            return

        for e0 in ['@all', function]:
            if e0 in self.dependencies[namespace]:
                e1 = self.dependencies[namespace][e0]
                if isinstance(e1, list):
                    for f in e1:
                        self.standard_dependencies.add(f)
                else:
                    self.standard_dependencies.add(e1)


    def _expand_api(self, api, receiver, args, pseudo_type, equivalent):
        '''
        the heart of api translation dsl

        function or <z>(<arg>, ..) can be expanded, <z> can be just a name for a global function, or #name for method, <arg> can be %{self} for self or %{n} for nth arg
        '''

        if callable(api):
            if receiver:
                return api(receiver, *(args + [pseudo_type]))
            else:
                return api(*(args + [pseudo_type]))
        elif isinstance(api, str):
            if '(' in api:
                call_api, arg_code = api[:-1].split('(')
                new_args = [self._parse_part(
                    a.strip(), receiver, args, equivalent) for a in arg_code.split(',')]
            else:
                call_api, arg_code = api, ''
                new_args = args
            if '#' in call_api:
                a, b = call_api.split('#')
                method_receiver = self._parse_part(
                    a, receiver, args, equivalent) if a else receiver
                return method_call(method_receiver, b, new_args, pseudo_type=pseudo_type)
            elif '.' in call_api:
                a, b = call_api.split('.')
                static_receiver = self._parse_part(
                    a, receiver, args, equivalent) if a else receiver
                if b[-1] != '!':
                    return Node('static_call', receiver=static_receiver, message=b, args=new_args, pseudo_type=pseudo_type)
                else:
                    return Node('attr', object=static_receiver, attr=b[:-1], pseudo_type=pseudo_type)
            else:
                if receiver:
                    return call(call_api, [receiver] + new_args, pseudo_type=pseudo_type)
                else:
                    return call(call_api, new_args, pseudo_type=pseudo_type)
        else:
            raise PseudoDSLError('%s not supported by api dsl' % str(api))

    def _parse_part(self, part, receiver, args, equivalent):
        if part[0] == '%':  # %{v}
            inside = part[2:-1]
            if inside.isnumeric():
                inside = int(inside)
                return args[inside]
            elif inside == 'self':
                if receiver:
                    return receiver
                else:
                    raise PseudoDSLError(
                        '%{self} not working for functions with api dsl')
            elif inside == 'equivalent':
                return typename(equivalent)
            else:
                return getattr(self, '%s_placeholder' % inside)(receiver, *args, equivalent=equivalent)
        else:
            return local(part)

    def update_used(self, t):
        if isinstance(t, list):
            for type_ in t:
                if isinstance(type_, str):
                    if type_ in TYPES:
                        self.used.add(type_)
                else:
                    self.update_used(type_)
        else:
            if t in TYPES:
                self.used.add(t)
