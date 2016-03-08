from pseudo.api_translator import ApiTranslator, to_op
from pseudo.pseudo_tree import Node, method_call, attr, to_node, local, call
from pseudo.api_translators.csharp_api_handlers import expand_slice, Display, normalize, pad

class CSharpTranslator(ApiTranslator):
    '''
    CSharp api translator

    The DSL is explained in the ApiTranslator docstring
    '''

    methods = {
        'List': {
            '@equivalent':  'List',

            'push':         '#Insert',

            'insert':       '#Insert',

            'remove_at':    '#RemoveAt',

            'remove':       '#Remove',

            'length':       '.Count!',

            'slice':        expand_slice,

            'slice_from':   '#Drop',

            'slice_to':     '#Take',

            'slice_':       '#Slice'
        },
        'Dictionary': {
            '@equivalent':  'Dictionary',

            'length':       '.Count!',
            'keys':         '#Keys',
            'values':       '#Values'
        },
        'String': {
            '@equivalent':  'String',

            'length':       '.Length!',
            'substr':       lambda f, from_, to, pseudo_type: method_call(
                                f, 'Substring', [from_, normalize(f, from_, to)], pseudo_type),

            'substr_from':  '#Substring',
            'substr_to':    lambda f, to, pseudo_type: method_call(
                                f, 'Substring', [to_node(0), normalize(f, to_node(0), to)], pseudo_type),
            'find_from':    '#IndexOf',
            'find':         '#IndexOf',
            'count':        lambda f, element, pseudo_type: method_call(
                                    f,
                                    'Count',
                                    [Node('anonymous_function',
                                        params=['sub'],
                                        block=[
                                            Node('comparison',
                                                op='==',
                                                left=local('sub', 'String'),
                                                right=local('s', 'String'),
                                                pseudo_type='Boolean')
                                        ],
                                        return_type='Boolean',
                                        pseudo_type=['Function', 'String', 'Boolean'])],
                                    pseudo_type='Int'),
            'concat':       to_op('+'),
            'split':        '#Split',
            'trim':         '#Trim',
            'center':       pad,
            'present?':     lambda f, _: Node('comparison',
                                op='!=',
                                left=attr(f, 'Length', 'Int'),
                                right=to_node(0),
                                pseudo_type='Boolean'),
            'empty?':       lambda f, _: Node('comparison',
                                op='==',
                                left=attr(f, 'Length', 'Int'),
                                right=to_node(0),
                                pseudo_type='Boolean'),
            'contains?':    '#Contains',
            'to_int':       'Int32.Parse(%{self})',
            'pad_left':     '#PadLeft',
            'pad_right':    '#PadRight'
        },
        'Set': {
            '@equivalent':  'Set'
        },
        'Regexp': {
            '@equivalent': 'Regexp',

            'match':        '#match'
        },
        'RegexpMatch': {
            '@equivalent': 'RegexpMatch',



            'group':        lambda receiver, index, _: Node('index',
                                sequence=attr(Node('index',
                                    sequence=attr(receiver, 'Groups', ['List', 'CSharpRegexGroup']),
                                    index=to_node(1 + index.value) if index.type == 'int' else Node('binary_op', op='+', left=to_node(1), right=index, pseudo_type='Int'),
                                    pseudo_type='CSharpRegexGroup'),
                                    'Captures',
                                    ['List', 'RegexpMatch']),
                                index=to_node(0),
                                pseudo_type='RegexpMatch'),
            'has_match':    '.Success!'
        },
        'Array': {
            '@equivalent':  'Any[]',

            'length':       lambda receiver, _: to_node(receiver.pseudo_type[2])
        },
        'Tuple': {
            '@equivalent': 'Tuple',

            'length':       lambda _, pseudo_type: to_node(len(pseudo_type) - 1)
        }
    } 

    functions = {
        'io': {
            'display':    Display,
            'read':       'Console.ReadLine',
            'read_file':  'File.ReadAllText',
            'write_file': 'File.WriteAllText'
        },

        'math': {
            'ln':          'Math.Log',
            'tan':         'Math.Tan',
            'sin':         'Math.Sin',
            'cos':         'Math.Cos'
        },

        'http': {
        },

        'regexp': {
            'compile':      lambda value, _: Node('new_instance', 
                                class_name='Regex',
                                args=[value],
                                pseudo_type='Regexp'),
            'escape':       'Regex.Escape'
        }
    }

    dependencies = {
        'List': {
            '@all':     'System.Collections.Generic'
        },

        'Dictionary': {
            '@all':     'System.Collections.Generic'
        },

        'io': {
            'read_file':    'System.IO',
            'write_file':   'System.IO'
        },

        'regexp': {
            '@all':     'System.Text.RegularExpressions'
        }
    }
