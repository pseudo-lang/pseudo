from pseudo.api_translator import ApiTranslator, to_op
from pseudo.pseudo_tree import Node, method_call, call, if_statement, for_each_with_index_statement, assignment, attr
from pseudo.api_translators.go_api_handlers import expand_insert, expand_slice, expand_map, expand_filter, Read

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
            'length':       'len',
            'insert':       expand_insert,
            'slice':        expand_slice,
            'slice_from':   expand_slice,
            'slice_to':     lambda receiver, to, pseudo_type: expand_slice(receiver, None, to, pseudo_type),
            'map':          expand_map,
            'filter':       expand_filter        
        },
        'Dictionary': {
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
            'read':         Read,
            'read_file':    'ioutil.ReadFile',
            'write_file':   'ioutil.WriteFile'
        },
        'math': {
            'ln':       'Math.Log',
            'tan':      'Math.Tan' 
        }
    }


    dependencies = {
        'regexp': {
            '@all':     'regexp'
        },
        'io': {
            'display': 'fmt',
            'read':    ['bufio', 'os'],
            'read_file': ['io/ioutil'],
            'write_file': ['io/ioutil']
        },
        'math': {
            '@all':     'math'
        }
    }


    errors = {

    }
