from pseudo.api_translator import ApiTranslator, to_op
from pseudo.pseudo_tree import Node, method_call, call, to_node, attr, local
from pseudo.api_translators.js_api_handlers import empty, present, object_len

LODASH = local('_', 'Library')

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
                                      if index.type == 'int' else
                                      Node('binary_op', op='+', left=index, right=to_node(1), pseudo_type='Int')],
                                    pseudo_type='Void'),
            'remove':       '_.pull(%{self}, %{0})',
            'slice':        '#slice',
            'slice_from':   '#slice',
            'slice_to':     '#slice(0, %{0})',
            'map':          '_.map(%{self}, %{0})',
            'filter':       '_.filter(%{self}, %{0})',
            'reduce':       '_.reduce(%{self}, %{0}, %{1})',
            'any?':         '_.any(%{self}, %{0})',
            'all?':         '_.all(%{self}, %{0})',
            'sort':         '#sort',
            'empty?':       empty,
            'present?':     present,
            'find':         '#indexOf',
            'contains?':    '_.contains(%{self}, %{0})'
        },
        'Dictionary': {
            '@equivalent':  'Object',

            'length':       object_len,
            'keys':         'Object.keys(%{self})',
            'values':       'Object.values(%{self})',
            'contains?':    '#hasOwnProperty',
            'present?':     present,
            'empty?':       empty
        },
        'String': {
            '@equivalent':  'String',
            'substr':       '#slice',
            'substr_from':  '#slice',
            'length':       '.length!',
            'substr_to':    '#slice(0, %{0})',
            'find':         '#search',
            'find_from':    lambda f, value, index, _: Node('binary_op', op='+', pseudo_type='Int', left=index, right=method_call(
                                method_call(f, 'slice', [index], 'String'),
                                'search',
                                [value],
                                'Int')),
            'count':        lambda f, count, _: attr(method_call(LODASH, 'where', [count], ['List', 'String']), 'length', 'Int'),
            'concat':       to_op('+'),
            'partition':    lambda f, delimiter, _: Node('index', sequence=method_call(LODASH, 'partition', [delimiter], 'String'), index=to_node(1), pseudo_type=['Tuple', 'String', 'String', 'String']),
            'split':        '#split',
            'trim':         '#trim',
            'reversed':     lambda f, _: method_call(
                                method_call(
                                    method_call(
                                        f,
                                        'split',
                                        [to_node('')],
                                        ['List', 'String']),
                                    'reverse',
                                    [],
                                    ['List', 'String']),
                                'join',
                                [to_node('')],
                                'String'),
            'center':      '_.pad(%{self}, %{0}, %{1})',
            'present?':     lambda f, _: f,
            'empty?':       lambda f, _: Node('unary_op', op='not', value=f, pseudo_type='Boolean'),
            'contains?':    '_.contains(%{self}, %{0})',
            'to_int':       'parseInt',
            'pad_left':     '_.padLeft(%{self}, %{0}, %{1})',
            'pad_right':    '_.padRight(%{self}, %{0}, %{1})'
        },
        'Tuple': {
            '@equivalent':  'Array',

            'length':       '.length!'
        },
        'Array': {
            '@equivalent':  'Array',

            'length':       '.length!'
        },
        'Set': {
            '@equivalent': 'Object',

            'length':       object_len,
            'contains?':    '_.contains(%{self}, %{0})',
            'intersection': '_.intersection(%{self}, %{0})',
            'union':        '_.union(%{self}, %{0})',
            'present?':     present,
            'empty?':       empty
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
        }
    }

    functions = {
        'global': {
            'wat':          lambda _: Node('block', block=[]),
            'exit':         lambda status, _: call('exit', [status])
        },

        'system': {
            'args':         'process.argv!',
            'arg_count':    lambda _: Node('binary_op',
                                op='-',
                                left=attr(
                                    attr(local('process', 'Library'), 
                                    'argv', 
                                    ['List', 'String']), 
                                    'length', 
                                    'Int'),
                                right=to_node(1),
                                pseudo_type='Int'),
            'index':        lambda value, _: Node('index',
                                sequence=attr(local('process', 'Library'), 'argv', ['List', 'String']),
                                index=to_node(value.value + 1) if value.type == 'int' else Node('binary_op', op='+', left=value, right=value, pseudo_type='Int'),
                                pseudo_type='String')                                
        },
        'io': {
            'display':      'console.log',
            'read_file':    "fs.readFileSync(%{0}, 'utf8')",
            'write_file':   "fs.writeFileSync(%{0}, %{1}, 'utf8')",
        },

        'math': {
            'ln':           'Math.log',
            'log':          'Math.log',
            'tan':          'Math.tan',
            'sin':          'Math.sin',
            'cos':          'Math.cos',
            'pow':          'Math.pow'
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
