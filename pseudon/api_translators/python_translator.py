from pseudon.types import *
from pseudon.api_translator import ApiTranslator
from pseudon.pseudon_tree import Node, method_call, call


class PythonTranslator(ApiTranslator):
    '''
    Python api translator

        Java specific:

        `%{new}`:
            expands to new %{equivalent}

    DSL:
        you can use either a lambda/function which returns a Node with signature
        `(receiver, *args)` (e.g. `lambda receiver, value: Node('none'))
        or

        shortcuts:
        `#method_name`  => calls that method of the equivalent class with the same args
        `function_name` => calls that function with the same args
        `.attr_name`    => accesses that attribute of the equivalent class
        `!method_name`  => calls that static method of the equivalent class with the same args

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

        Nodes: Nodes can be either the official pseudon nodes or in special cases
               with `_<special_node>` when they describe syntax typical only for
               the target language of the translator

        helpers: quite useful helpers from pseudon.pseudon_tree are
                 `method_call(receiver: str/Node, message: str, args: [Node])`
                     which helps with method call nodes with normal `local` name object receivers

                 `call(callee: str/Node, args: [Node])`
                     which helps with call nodes with normal `local` name callees
    '''

    @staticmethod
    def expand_map(receiver, func):
        if func.type == 'lambda':
            return Node(
                '_list_comp',
                sequence=receiver)
        else:
            return call('map', [func, receiver])

    @staticmethod
    def expand_filter(receiver, func):
        if func.type == 'lambda':
            return Node(
                '_list_comp')
        else:
            return call('filter', [func, receiver])

    @staticmethod
    def expand_slice(receiver, from_=None, to=None):
        if from_:
            if to:
                return Node('_slice', receiver=receiver, from_=from_, to=to_)
            else:
                return Node('_slice_from', receiver=receiver, from_=from_)
        elif to:
            return Node('_slice_to', receiver=receiver, to=to)
        else:
            return Node('_slice_', receiver=receiver)

    methods = {
        'List': {
            'push':         '#append',
            'pop':          '#pop',
            'length':       'len',
            'insert':       '#insert',
            'remove_at':    lambda receiver, index: Node('_del', node=Node('index', z=receiver, index=index)),
            'remove':       'remove',
            'slice':        expand_slice,
            'slice_from':   expand_slice,
            'slice_to':     lambda receiver, to: expand_slice(receiver, None, to)
        },
        'Dictionary': {
            'length':       'len',
            'keys':         '#keys',
            'values':       '#values'
        },
        'Enumerable': {
            'map':          expand_map,
            'filter':       expand_filter,
            'reduce':       'functools.reduce'
        }
    }

    functions = {
        'global': {
            'wat':          lambda: Node('block', block=[]),
            'exit':         lambda status: call('exit', [status])
        },

        'io': {
            'display':      'print',
            'read':         'input'
        }
    }

    dependencies = {
        'Enumerable': {
            'map':  'functools'
        }
    }
