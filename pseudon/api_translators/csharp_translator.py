from pseudon.types import *
from pseudon.api_translator import ApiTranslator
from pseudon.pseudon_tree import Node, method_call, call


class CSharpTranslator(ApiTranslator):
    '''
    CSharp api translator

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

    api = {
        'List': {
            '@equivalent':  'List',

            'push':         '#Insert'

            'insert':       '#Insert',

            'remove_at':    '#RemoveAt',

            'remove':       '#Remove'
        },
        'Dictionary': {
            'length':       'array_length',
            'keys':         'array_keys',
            'values':       'array_values'
        },
        'Enumerable': {
            'map':          '#Select',
            'filter':       '#Where',
            'reduce':       '#Aggregate'
        }
    }

    dependencies = {
        'Enumerable': {
            '@all':     'Linq'
        }
    }
