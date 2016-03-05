from pseudon.types import *
from pseudon.api_translator import ApiTranslator
from pseudon.pseudon_tree import Node, call, local


class PHPTranslator(ApiTranslator):
    '''
    PHP api translator

    The DSL is explained in the ApiTranslator docstring
    '''

    methods = {
        'List': {
            'push':         'array_push',
            'pop':          'array_pop',
            'length':       'array_length',
            'insert':       'array_insert',
            'remove_at':    None,
            'remove':       'array_remove'
        },
        'Dictionary': {
            'length':       'array_length',
            'keys':         'array_keys',
            'values':       'array_values'
        },
        'Enumerable': {
            'map':          'array_map',
            'filter':       'array_filter',
            'reduce':       'array_reduce'
        }
    }

    functions = {
        'math': {
            'ln':           'log',
            'tan':          'tan'
        },
        'io': {
            'display':      lambda receiver, *args, _: Node('_echo', args=args, pseudo_type='Void'),
            'read':         lambda args, _: call(local('fgets', ['Function', 'File', 'String']), [Node('constant', name='STDIN', pseudo_type='File')], 'String'),
            'read_file':    'read_file_contents',
            'write_file':   'write_file_contents'
        }            
    }
