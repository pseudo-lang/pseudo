from pseudon.types import *
from pseudon.api_translator import ApiTranslator, to_op
from pseudon.pseudon_tree import Node, method_call, call, if_statement, for_each_with_index_statement, assignment, attr
from pseudon.api_translators.go_api_handlers import expand_insert, expand_slice, expand_map, expand_filter, read, ReadFile, WriteFile

class GolangTranslator(ApiTranslator):
    '''
    Go api translator

    The DSL is explained in the ApiTranslator docstring
    '''
    
    methods = {
        'List': {
            '@equivalent':  'slice',

            'push':         'append',
            'pop':          lambda assignment, *l, receiver, pseudo_type: 
                                    assignment_updated(assignment, value=go_last(receiver)),
            'length':       '.length',
            'insert':       expand_insert

        },
        'Dictionary': {
        },
        'Enumerable': {
            'map':          expand_map,
            'filter':       expand_filter
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
        }
    }

    functions = {
        'regexp':  {
            'compile':      'regexp.Compile',
            'escape':       'regexp.QuoteMeta'
        },
        'io': {
            'display':      'fmt.Println',
            'read':         read,
            'read_file':    ReadFile,
            'write_file':   WriteFile
        }
    }


    dependencies = {
        'regexp': {
            '@all':     'regexp'
        }
    }



