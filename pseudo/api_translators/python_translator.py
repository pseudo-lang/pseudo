from pseudo.types import *
from pseudo.api_translator import ApiTranslator, to_op
from pseudo.pseudo_tree import Node, method_call, call, to_node, local, assignment_updated
from pseudo.api_translators.python_api_handlers import expand_map, expand_filter, expand_slice, expand_set_slice, to_py_generatorcomp, ReadFile, WriteFile

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
            'find':         '#find',
            'join':         lambda receiver, delimiter, _: method_call(delimiter, 'join', [receiver], pseudo_type='String'),
            'map':          lambda receiver, f, pseudo_type: Node('_py_listcomp', 
                                sequences=Node('for_sequence', sequence=receiver),
                                iterators=Node('for_iterator', iterator=local(f.params[0], f.pseudo_type[1])),
                                block=f.block[0],
                                test=None,
                                pseudo_type=['List', f.pseudo_type[2]]),
            'filter':       lambda receiver, test, pseudo_type: Node('_py_listcomp', 
                                sequences=Node('for_sequence', sequence=receiver),
                                iterators=Node('for_iterator', iterator=local(test.params[0], test.pseudo_type[1])),
                                block=local(test.params[0], test.pseudo_type[1]),
                                test=test.block[0],
                                pseudo_type=['List', test.pseudo_type[1]]),

            'reduce':       lambda receiver, aggegator, initial, pseudo_type: Node('static_call',
                                receiver=local('functools', 'Library'),
                                message='reduce',
                                args=[aggegator, initial],
                                pseudo_type=pseudo_type),

            'any?':         to_py_generatorcomp('any'),

            'all?':         to_py_generatorcomp('all')

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
            'write_file':   WriteFile,
            'read_file':    ReadFile
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
    
    dependencies = {
        'Enumerable': {
            'map':  'functools'
        },

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
        }
    }
