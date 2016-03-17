from pseudo.api_translator import ApiTranslator, to_op
from pseudo.pseudo_tree import Node, to_node, method_call, typename, local
from pseudo.api_translators.ruby_api_handlers import expand_slice, to_method_rb_block, display

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
            'join':         '#join',
            'map':          to_method_rb_block('map'),
            'filter':       to_method_rb_block('select'),
            'reduce':       to_method_rb_block('reduce'),
            'any?':         to_method_rb_block('any?'),
            'all?':         to_method_rb_block('all?'),
            'sort':         '#sort!',
            'present?':     lambda receiver, _: Node('unary_op', 
                                op='not',
                                value=method_call(receiver, 'empty?', [], 'Boolean'),
                                pseudo_type='Boolean'),
            'empty?':       '#empty?',
            'find':         '#index',
            'contains?':    '#include?'
        },
        'Dictionary': {
            '@equivalent':  'Hash',

            'length':       '#length',
            'keys':         '#keys',
            'values':       '#values',
            'contains?':    '#include?',
            'present?':     lambda receiver, _: Node('unary_op', 
                                op='not',
                                value=method_call(receiver, 'empty?', [], 'Boolean'),
                                pseudo_type='Boolean'),
            'empty?':       '#empty?'
        },
        'Set': {
            '@equivalent':  'Set',

            'length':       '#length',
            'contains?':    '#include?',
            'union':        to_op('|'),
            'intersection': '#intersection',
            'present?':     lambda receiver, _: Node('unary_op', 
                                op='not',
                                value=method_call(receiver, 'empty?', [], 'Boolean'),
                                pseudo_type='Boolean'),
            'empty?':       '#empty?'
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
            'find':         '#index',
            'find_from':    '#index',
            'count':        '#count',
            'partition':    '#partition',
            'split':        '#split',
            'trim':         '#trim',
            'reversed':     '#reverse',
            'center':       '#center',
            'present?':     lambda receiver, _: Node('unary_op', 
                                op='not',
                                value=method_call(receiver, 'empty?', [], 'Boolean'),
                                pseudo_type='Boolean'),
            'empty?':       '#empty?',
            'contains?':    '#include?',
            'to_int':       '#to_i',
            'pad_left':     '#ljust',
            'pad_right':    '#rjust'
        },
        'Regexp': {
            '@equivalent':  'Regexp',

            'match':        '%{0}#scan(%{self})'
        },
        'Int': {'to_float': '#to_f'},
        'Float': {'to_int': '#to_i'},
        'RegexpMatch': {
            '@equivalent':  'Regexp_',

            'group':        lambda receiver, index, _: Node('index',
                                sequence=Node('index', sequence=receiver, index=index, pseudo_type=['List', 'String']),
                                index=to_node(0),
                                pseudo_type='String'),
            'has_match':    lambda receiver, _: Node('unary_op',
                                op='not',
                                value=method_call(receiver, 'empty?', [], 'Boolean'),
                                pseudo_type='Boolean')
        }
    }

    functions = {
        'global': {
            'wat':          lambda _: Node('block', block=[]),
            'exit':         lambda status, _: call('exit', [status])
        },

        'io': {
            'display':      display,
            'read':         'gets',
            'read_file':    'File.read',
            'write_file':   'File.write'
        },

        'math': {
            'ln':           'Math.log',
            'log':          'Math.log',
            'tan':          'Math.tan',
            'sin':          'Math.sin',
            'cos':          'Math.cos',
            'pow':          lambda left, right, pseudo_type: Node('binary_op',
                                op='**', left=left, right=right, pseudo_type=pseudo_type)
        },

        'regexp': {
            'compile':      lambda value, _: Node('_rb_regex_interpolation', value=value, pseudo_type='Regexp'),
            'escape':       'Regexp.escape'
        },

        'system': {
            'args':         lambda _: typename('ARGV', ['List', 'String']),
            'arg_count':    lambda _: Node('binary_op', op='+', left=method_call(local('ARGV', ['List', 'String']), 'length', [], 'Int'), right=to_node(1), pseudo_type='Int'),
            'index':        lambda value, _: Node('index',
                                        sequence=local('ARGV', ['List', 'String']),
                                        index=to_node(value.value - 1) if value.type == 'int' else Node('binary_op', op='-', left=value, right=to_node(1), pseudo_type='Int'),
                                        pseudo_type='String')
            # in ruby args counting starts from 0, not 1
        }
    }

    dependencies = {
        'http':     {
            '@all':     'Requests'
        },

        'Set': {
            '@all': 'set'
        }
    }
