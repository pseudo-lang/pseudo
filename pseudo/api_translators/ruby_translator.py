from pseudo.api_translator import ApiTranslator, to_op
from pseudo.pseudo_tree import Node, to_node
from pseudo.api_translators.ruby_api_handlers import expand_slice, to_method_rb_block

class RubyTranslator(ApiTranslator):
    '''
    Ruby api translator

    The DSL is explained in the ApiTranslator docstring
    '''

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
            'slice_to':     lambda receiver, to, pseudo_type: expand_slice(receiver, to_node(0), to, pseudo_type),
            'map':          to_method_rb_block('map'),
            'filter':       to_method_rb_block('select'),
            'reduce':       to_method_rb_block('reduce'),
            'any?':         to_method_rb_block('any?'),
            'all?':         to_method_rb_block('all?')
        },
        'Dictionary': {
            '@equivalent':  'Hash',

            'length':       '#length',
            'keys':         '#keys',
            'values':       '#values',
            'contains?':    '#include?'
        },
        'Set': {
            '@equivalent':  'Set',

            'length':       '#length',
            'contains?':    '#include?',
            'union':        to_op('|'),
            'intersection': '#intersection'
        },
        'Tuple': {
            '@equivalent':  'Array',

            'length':       '#length'
        },
        'Array': {
            '@equivalent':  'Array',

            'length':       '#length'
        },
        'String': {
            '@equivalent':  'String',
            'substr':       expand_slice,
            'substr_from':  expand_slice,
            'substr_to':    lambda receiver, to, _: expand_slice(receiver, None, to, 'String'),
            'length':       '#length',
            'concat':       to_op('+'),
            'find':         '#find',
            'count':        '#count',
            'partition':    '#partition',
            'split':        '#split',
            'trim':         '#trim',
            'reversed':     '#reverse',
            'justify':      '#center'
        }
    }

    functions = {
        'global': {
            'wat':          lambda _: Node('block', block=[]),
            'exit':         lambda status, _: call('exit', [status])
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
