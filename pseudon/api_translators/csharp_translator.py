from pseudon.types import *
from pseudon.api_translator import ApiTranslator
from pseudon.pseudon_tree import Node, method_call, call
from pseudon.api_translators.csharp_api_handlers import expand_slice

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
        }
    }

    functions = {
        'io': {
            'display':    'Console.WriteLine',
            'read':       'Console.ReadLine',
            'read_file':  'File.ReadAllText',
            'write_file': 'File.WriteAllText'
        },

        'math': {
            'ln':          'Math.Log',
            'tan':         'Math.Tan'
        }
    }

    dependencies = {
        'Enumerable': {
            '@all':     'System.Linq'
        },
        'List': {
            '@all':     'System.Collections.Generic'
        },

        'Dictionary': {
            '@all':     'System.Collections.Generic'
        }
    }
