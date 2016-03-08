from pseudo.api_translator import ApiTranslator
from pseudo.pseudo_tree import Node, method_call, call, to_node


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
            'slice_to':     '#slice(0, %{0})',
            'map':          '_.map',
            'filter':       '_.filter'
        },
        'Dictionary': {
            '@equivalent':  'Object',

            'length':       '.length!',
            'keys':         'Object.keys',
            'values':       'Object.values'
        },
        'String': {
            '@equivalent':  'String',
            'substr':       '#slice',
            'substr_from':  '#slice',
            'length':       '.length!',
            'substr_to':    '#slice(0, %{0})'
        },
        'Tuple': {
            '@equivalent':  'Array',

            'length':       '.length!'
        },
        'Array': {
            '@equivalent':  'Array'
        },
        'RegexpMatch': {
            '@equivalent':  'Array',

            'group':        lambda receiver, index, _: Node('index',
                                sequence=receiver,
                                index=to_node(1 + index.value) if index.type == 'int' else Node('binary_op', op='+', left=to_node(1), right=index, pseudo_type='Int'),
                                pseudo_type='String'),

            'has_match':    lambda receiver, _: receiver                                
        },
        'Regexp': {
            '@equivalent':  'Regexp',

            'match':        '#exec'
        },
        'Set': {
            '@equivalent': 'Object'
        },

    }

    functions = {
        'global': {
            'wat':          lambda _: Node('block', block=[]),
            'exit':         lambda status, _: call('exit', [status])
        },

        'io': {
            'display':      'console.log',
            'read_file':    'fs.readFileSync',
            'write_file':   'fs.writeFileSync'
        },

        'http': {
            'get':          'http.get',
            'post':         'http.post',
        },

        'math': {
            'ln':           'Math.log',
            'tan':          'Math.tan',
            'sin':          'Math.sin',
            'cos':          'Math.cos'
        },

        'regexp': {
            'compile':      lambda value, _: Node('new_instance', 
                                class_name='RegExp',
                                args=[value],
                                pseudo_type='Regexp'),
            'escape':       '_.escapeRegExp'
        }
    }

    js_dependencies = {
        '_': 'lodash'
    }

    dependencies = {
        'io': {
            'read_file':    'fs',
            'write_file':   'fs'
        },
        'regexp': {
            'escape':       'lodash'
        }
    }
