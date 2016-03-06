from pseudo.types import *
from pseudo.api_translator import ApiTranslator
from pseudo.pseudo_tree import Node, method_call, call


class JSTranslator(ApiTranslator):
    '''
    JS api translator

    The DSL is explained in the ApiTranslator docstring
    '''

    methods = {
        'List': {
            '@equivalent':  'Array',

            'push':         '#push',
            'pop':          '#pop',
            'length':       '.length!',
            'insert':       '#splice(%{self}, 0, %{0})',
            'remove_at':    lambda receiver, index, _: 
                                method_call(
                                    receiver, 
                                    'splice', 
                                    [index, 
                                      to_node(index.value + 1)
                                      if node.type == 'int' else
                                      Node('binary_op', op='+', left=index, right=to_node(1), pseudo_type='Int')],
                                    pseudo_type='Void'),
            'remove':       '_.pull(%{self}, %{0})',
            'slice':        '#slice',
            'slice_from':   '#slice',
            'slice_to':     '#slice(0, %{0})'
        },
        'Dictionary': {
            '@equivalent':  'Object',

            'length':       '.length!',
            'keys':         'Object.keys',
            'values':       'Object.values'
        },
        'Enumerable': {
            '@equivalent':  'Enumerable',

            'map':          '_.map',
            'filter':       '_.filter'
        },
        'String': {
            '@equivalent':  'String',
            'substr':       '#slice',
            'substr_from':  '#slice',
            'length':       '.length!',
            'substr_to':    '#slice(0, %{0})'
        }
    }

    functions = {
        'global': {
            'wat':          lambda _: Node('block', block=[]),
            'exit':         lambda status, _: call('exit', [status])
        },

        'io': {
            'display':      'console.log',
            'read':         'console.read',
            'read_file':    'fs.readFileSync',
            'write_file':   'fs.writeFileSync'
        },

        'http': {
            'get':          'http.get',
            'post':         'http.post',
        },

        'math': {
            'ln':           'math.log',
            'tag':          'math.tag'
        }
    }

    js_dependencies = {
        '_': 'lodash'
    }

    dependencies = {

    }
