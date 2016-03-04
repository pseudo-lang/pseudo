from pseudon.types import *
from pseudon.api_translator import ApiTranslator, to_op
from pseudon.pseudon_tree import Node, method_call, call, to_node, local, assignment_updated


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

    def expand_map(receiver, func):
        if func.type == 'lambda':
            return Node(
                '_list_comp',
                sequence=receiver)
        else:
            return call('map', [func, receiver])

    def expand_filter(receiver, func):
        if func.type == 'lambda':
            return Node(
                '_list_comp')
        else:
            return call('filter', [func, receiver])

    def expand_slice(receiver, from_=None, to=None, pseudo_type=None):
        if from_:
            if to:
                if from_.type == 'int' and from_.value == 0:
                    return Node('_slice_to', sequence=receiver, to=to, pseudo_type=pseudo_type)
                else:
                    return Node('_slice', sequence=receiver, from_=from_, to=to, pseudo_type=pseudo_type)
            else:
                return Node('_slice_from', sequence=receiver, from_=from_, pseudo_type=pseudo_type)
        elif to:
            return Node('_slice_to', sequence=receiver, to=to, pseudo_type=pseudo_type)
        else:
            return None

    def read_file(assignment, namespace, function, args):
        return Node('_with', call=call('open', [args[0], to_node("'r'")], pseudo_type='File'), 
                        context='_f', 
                        block=[
                            assignment_updated(
                                assignment, 
                                value=method_call(
                                    local('_f'), 
                                    'read', 
                                    [], 
                                    pseudo_type='String'))],
                        pseudo_type='Void',
                        value_type='String')

    methods = {
        'List': {
            '@equivalent':  'list',

            'push':         '#append',
            'pop':          '#pop',
            'length':       'len',
            'insert':       '#insert',
            'remove_at':    lambda receiver, index, _: Node('_del', node=Node('index', z=receiver, index=index), pseudo_type='Void'),
            'remove':       '#remove',
            'slice':        expand_slice,
            'slice_from':   expand_slice,
            'slice_to':     lambda receiver, to, pseudo_type: expand_slice(receiver, None, to, pseudo_type),
            'repeat':       to_op('*'),
            'set_slice':    expand_set_slice,
            'set_slice_from': expand_set_slice,
            'set_slice_to': lambda receiver, to, pseudo_type: expand_set_slice(receiver, None, to, pseudo_type),            
            'find':         '#find',
            'join':         lambda receiver, delimiter, _: method_call(delimiter, 'join', [receiver], pseudo_type='String')

        },
        'Dictionary': {
            '@equivalent':  'dict',

            'length':       'len',
            'keys':         '#keys',
            'values':       '#values'
        },
        'Enumerable': {
            '@equivalent':  'list',

            'map':          expand_map,
            'filter':       expand_filter,
            'reduce':       'functools.reduce'
        },
        'String': {
            '@equivalent':  'str',
            'substr':       expand_slice,
            'substr_from':  expand_slice,
            'length':       'len',
            'substr_to':    lambda receiver, to, _: expand_slice(receiver, None, to, pseudo_type=pseudo_type),
            'find':         '#find',
            'count':        '#count',
            'partition':    '#partition',
            'split':        '#split',
            'trim':         '#strip',
            'format':       '#format',
            'concat':       to_op('+'),
            'c_format':     to_op('%')
        },
        'Set': {
            '@equivalent':  'set',
            'union':        to_op('-'),
            'intersection': to_op('&')
        },
        'Tuple': {
            '@equivalent':  'tuple'
        },
        'Array': {
            '@equivalent':  'tuple'
        },
        'Regexp': {
            '@equivalent':  '_sre.SRE_Pattern',
            'match':        '#match'
        },
        'RegexpMatch': {
            '@equivalent':  '_sre.SRE_Match',
            'group':        '#group',
            'has_match':    lambda receiver, _: receiver
        }
    }

    functions = {
        'global': {
            'wat':          lambda _: Node('block', block=[]),
            'exit':         lambda status, _: call('exit', [status])
        },

        'io': {
            'display':      'print',
            'read':         'input',
            'write_file':    lambda filename, content, _: _Node('_with', 
                                call=call('open', [filename, to_node("'w'")]), 
                                context='_f', 
                                block=[method_call(local('_f'), 'write', [content])],
                                pseudo_type='Void')
        },

        'http': {
            'get':          'requests.get',
            'post':         'requests.post',
        },

        'math': {
            'ln':           'math.log',
            'tan':          'math.tan'
        },

        'regexp': {
            'compile':      're.compile',
            'escape':       're.escape'
        }
    }

    '''
    weird has tree matches with handlers 
    that can expand into the nearest block, not only in-place
    '''

    weird = {
        'standard_call': {
            'io': {
                'read_file': {
                    '_translate':   read_file,
                    '_temp_name':   '_file_contents'
                }
            }
        }
    }

    dependencies = {
        'Enumerable': {
            'map':  'functools'
        },

        'Regexp': {
            '@all': 're'
        },

        'http': {
            '@all': 'requests'
        },

        'math': {
            '@all': 'math'
        },

        'regexp': {
            '@all': 're'
        }
    }
