from pseudo.api_translator import ApiTranslator, to_op
from pseudo.pseudo_tree import Node, method_call, call, to_node, local, attr
from pseudo.api_translators.python_api_handlers import contains, expand_slice, expand_set_slice, to_py_generatorcomp, ReadFile, WriteFile

class PythonTranslator(ApiTranslator):
    '''
    Python api translator

    The DSL is explained in the ApiTranslator docstring
    '''

    methods = {
        'List': {
            '@equivalent':  'list',

            'push':         '#append',
            'pop':          '#pop',
            'length':       'len',
            'insert':       '#insert',
            'remove_at':    lambda receiver, index, _: Node('_py_del', value=Node('index', sequence=receiver, index=index), pseudo_type='Void'),
            'remove':       '#remove',
            'slice':        expand_slice,
            'slice_from':   expand_slice,
            'slice_to':     lambda receiver, to, pseudo_type: expand_slice(receiver, None, to, pseudo_type),
            'repeat':       to_op('*'),
            'set_slice':    expand_set_slice,
            'set_slice_from': expand_set_slice,
            'set_slice_to': lambda receiver, to, value, pseudo_type: expand_set_slice(receiver, None, to, value, pseudo_type),            
            'find':         '#index',
            'join':         lambda receiver, delimiter, _: method_call(delimiter, 'join', [receiver], pseudo_type='String'),
            # map and filter have implicit or explicit return because otherwise they wouldnt type check
            'map':          lambda receiver, f, pseudo_type: Node('_py_listcomp', 
                                sequences=Node('for_sequence', sequence=receiver),
                                iterators=Node('for_iterator', iterator=local(f.params[0].name, f.pseudo_type[1])),
                                block=f.block[0].value,
                                test=None,
                                pseudo_type=['List', f.pseudo_type[2]]),
            'filter':       lambda receiver, test, pseudo_type: Node('_py_listcomp', 
                                sequences=Node('for_sequence', sequence=receiver),
                                iterators=Node('for_iterator', iterator=local(test.params[0].name, test.pseudo_type[1])),
                                block=local(test.params[0].name, test.pseudo_type[1]),
                                test=test.block[0].value,
                                pseudo_type=['List', test.pseudo_type[1]]),
            'reduce':       lambda receiver, aggregator, initial, pseudo_type: Node('static_call',
                                receiver=local('functools', 'Library'),
                                message='reduce',
                                args=[aggregator, receiver, initial],
                                pseudo_type=pseudo_type),
            'any?':         to_py_generatorcomp('any'),
            'all?':         to_py_generatorcomp('all'),
            'sort':         '#sort',
            'present?':     lambda receiver, _: receiver,
            'empty?':       lambda receiver, _: Node('unary_op', op='not', value=receiver, pseudo_type='Boolean'),
            'contains?':    contains
        },
        'Dictionary': {
            '@equivalent':  'dict',

            'length':       'len',
            'keys':         '#keys',
            'values':       '#values',
            'contains?':    contains,
            'keys':         lambda receiver, pseudo_type: call(
                                local('list', ['Function', 'Any', 'List']),
                                [method_call(receiver, 'keys', [], ['dict_keys', pseudo_type[1]])],
                                pseudo_type=pseudo_type),
            'values':       lambda receiver, pseudo_type: call(
                                local('list', ['Function', 'Any', 'List']),
                                [method_call(receiver, 'values', [], ['dict_values', pseudo_type[1]])],
                                pseudo_type=pseudo_type),
            'present?':     lambda receiver, _: receiver,
            'empty?':       lambda receiver, _: Node('unary_op', op='not', value=receiver, pseudo_type='Boolean')
        },
        'String': {
            '@equivalent':  'str',

            'substr':       expand_slice,
            'substr_from':  expand_slice,
            'length':       'len',
            'substr_to':    lambda receiver, to, _: expand_slice(receiver, None, to, 'String'),
            'find':         '#index',
            'find_from':    '#index',
            'count':        '#count',
            'partition':    '#partition', 
            'split':        '#split',
            'trim':         '#strip',
            'format':       '#format',
            'concat':       to_op('+'),
            'c_format':     to_op('%'),
            'center':       '#center',
            'reversed':     'reversed',
            'empty?':       lambda receiver, _: Node('unary_op',
                                op='not',
                                value=receiver,
                                pseudo_type='Boolean'),
            'present?':     lambda receiver, _: receiver,
            'contains?':    lambda receiver, element, _: Node('_py_in', sequence=receiver, value=element, pseudo_type='Boolean'),
            'to_int':       'int',
            'pad_left':     '#ljust',
            'pad_right':    '#rjust'
        },
        'Int': {
            'to_float':     'float(%{self})'
        },
        'Float': {
            'to_int':       'int(%{self})'
        },
        'Set': {
            '@equivalent':  'set',

            'length':       'len',
            'contains?':    contains,
            'union':        to_op('|'),
            'intersection': to_op('-'),
            'present?':     lambda receiver, _: receiver,
            'empty?':       lambda receiver, _: Node('unary_op', op='not', value=receiver, pseudo_type='Boolean')
        },
        'Tuple': {
            '@equivalent':  'tuple',

            'length':       'len'
        },
        'Array': {
            '@equivalent':  'tuple',

            'length':       'len'
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
            'write_file':   WriteFile,
            'read_file':    ReadFile
        },

        'system': {
            'args':         'sys.argv!',
            'arg_count':    lambda _: call('len', [attr(local('sys', 'Library'), 'argv', ['List', 'String'])], 'Int'),
            
            'index':        lambda value, _: Node('index',
                                                sequence=attr(local('sys', 'Library'),
                                                              'argv',
                                                              ['List', 'String']),
                                                index=value,
                                                pseudo_type='String')
        },

        'http': {
            'get':          'requests.get',
            'post':         'requests.post',
        },

        'math': {
            'ln':           'math.log',
            'log':          'math.log',
            'tan':          'math.tan',
            'sin':          'math.sin',
            'cos':          'math.cos',
            'pow':          lambda left, right, pseudo_type: Node('binary_op',
                                op='**', left=left, right=right, pseudo_type=pseudo_type)
        },

        'regexp': {
            'compile':      're.compile',
            'escape':       're.escape'
        }
    }
    
    dependencies = {
        'Regexp': {
            '@all': 're'
        },

        'List': {
            'reduce': 'functools'
        },

        'http': {
            '@all': 'requests'
        },

        'math': {
            '@all': 'math'
        },

        'regexp': {
            '@all': 're'
        },

        'system': {
            '@all': 'sys'
        }
    }

#lambda receiver, on, _: Node(
# '_py_step',
# sequence=method_call(
#     receiver, 
#     'partition', 
#     [on], 
#     ['Tuple', 'String', 'String', 'String']),
# step=to_node(2),
# pseudo_type=['Tuple', 'String', 'String']),
