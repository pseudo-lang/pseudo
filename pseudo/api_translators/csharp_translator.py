from pseudo.api_translator import ApiTranslator
from pseudo.pseudo_tree import Node, method_call, call, attr, to_node
from pseudo.api_translators.csharp_api_handlers import expand_slice, Display

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
            'substr':       '#Substring',
            'find':         '#Find'
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

            'length':       lambda _, pseudo_type: to_node(pseudo_type[1])
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
