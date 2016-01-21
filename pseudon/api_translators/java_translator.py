from pseudon.types import *
from pseudon.api_translator import ApiTranslator
from pseudon.pseudon_tree import Node, method_call, call


class JavaTranslator(ApiTranslator):
    '''
    Java api translator

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

    def new_placeholder(self, receiver, *args, equivalent):
        return Node('new_instance', klass=equivalent, args=[])

    api = {
        'List': {
            '@equivalent':  'Vector',

            'push':         '#add',
            'insert':       '#insert',
            'remove_at':    '#remove(%{1})',
            'length':       '#size'
        },
        'Dictionary': {
            'length':       '#size',
            'keys':         '#keySet',
            'values':       '#values'
        },
        'Enumerable': {
            'map':          lambda receiver, function:
                                method_call(
                                    method_call(method_call(receiver, 'stream', []), 'map', [function]),
                                    'collect',
                                    method_call('Collectors', 'toList', [])),

            'filter':       lambda receiver, function:
                                method_call(
                                    method_call(method_call(receiver, 'stream', []), 'select', [function]),
                                    'collect',
                                    method_call('Collectors', 'toList', []))
        }
    }

    dependencies = {
        'Enumerable': {
            '@all': 'Collectors'
        }
    }
