from pseudon.types import *
from pseudon.api_translator import ApiTranslator
from pseudon.pseudon_tree import Node


class RubyTranslator(ApiTranslator):
    '''
    Ruby

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

    def expand_slice(receiver, from_=None, to=None):
        if from_:
            if to:
                return Node('_slice', sequence=receiver, from_=from_, to=to)
            else:
                return Node('_slice_from', sequence=receiver, from_=from_)
        elif to:
            return Node('_slice', sequence=receiver, from_=to_node(0), to=to)
        else:
            return None


    methods = {
        'List': {
            '@equivalent':  'Array',

            'push':         '#push',
            'pop':          '#pop',
            'length':       '#length',
            'insert':       '#insert',
            'remove_at':    '#delete_at',
            'remove':       '#delete',
            'slice':        expand_slice,
            'slice_from':   expand_slice,
            'slice_to':     lambda receiver, to: expand_slice(receiver, to_node(0), to)
        },
        'Dictionary': {
            '@equivalent':  'Hash',

            'length':       '#length',
            'keys':         '#keys',
            'values':       '#values'
        },
        'Enumerable': {
            '@equivalent':  'Enumerable',

            'map':          '#map',
            'filter':       '#select'
        },
        'String': {
            '@equivalent':  'String',
            'substr':       expand_slice,
            'substr_from':  expand_slice,
            'length':       '#length',
        }
    }

    functions = {
        'global': {
            'wat':          lambda: Node('block', block=[]),
            'exit':         lambda status: call('exit', [status])
        },

        'io': {
            'display':      'puts',
            'read':         'gets',
            'read_file':    'File.read',
            'write_file':   'File.write'
        },

        'http': {
            'get':          'Requests.get',
            'post':         'Requests.post',
        },

        'math': {
            'ln':           'Math.log',
            'tag':          'Math.tag'
        }
    }

    dependencies = {
        'http':     {
            '@all':     'Requests'
        }
    }
