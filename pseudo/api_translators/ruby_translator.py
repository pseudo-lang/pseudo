from pseudo.types import *
from pseudo.api_translator import ApiTranslator, to_op
from pseudo.pseudo_tree import Node, to_node
from pseudo.api_translators.ruby_api_handlers import expand_slice

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

            'map':          lambda receiver, f, pseudo_type: Node('_rb_method_call_block',
                                receiver=receiver,
                                message='map',
                                args=[],
                                f=Node('_rb_block',
                                    params=f.params,
                                    block=f.block,
                                    pseudo_type=f.pseudo_type),
                                pseudo_type=['List', f.pseudo_type[2]])
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
            'concat':       to_op('+')
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
