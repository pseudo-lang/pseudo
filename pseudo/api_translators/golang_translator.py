from pseudo.api_translator import ApiTranslator, to_op
from pseudo.pseudo_tree import Node, method_call, call, if_statement, for_each_with_index_statement, assignment, attr, to_node, local
from pseudo.api_translators.go_api_handlers import present, empty, expand_insert, expand_slice, expand_map, expand_filter, expand_reduce, DictKeys, DictValues, ReadFile, Find, Int, Contains, ListContains, Read

class GolangTranslator(ApiTranslator):
    '''
    Go api translator

    The DSL is explained in the ApiTranslator docstring
    '''

    methods = {
        'List': {
            '@equivalent':  'slice',

            'push':         lambda receiver, element, _: assignment(receiver, call('append', [receiver, element], receiver.pseudo_type)),
            'pop':          lambda receiver, _: assignment(receiver, Node('_go_slice_to', sequence=receiver, to=Node(
                                                    'binary_op', op='-', left=call('len', [receiver], 'Int'), right=to_node(1), pseudo_type='Int'), pseudo_type=receiver.pseudo_type)),
            'length':       'len',
            'insert':       expand_insert,
            'slice':        expand_slice,
            'slice_from':   expand_slice,
            'slice_to':     lambda receiver, to, pseudo_type: expand_slice(receiver, None, to, pseudo_type),
            'join':         'strings.Join(%{self}, %{0})',
            'map':          expand_map,
            'filter':       expand_filter,
            'find':         Find,
            'reduce':       expand_reduce,
            'contains?':    ListContains,
            'present?':     present,
            'empty?':       empty
        },
        'Dictionary': {
            '@equivalent':  'map',

            'length':       'len',
            'contains?':     Contains,
            'keys':          DictKeys,
            'values':        DictValues,
            'present?':      present,
            'empty?':        empty
        },
        'String': {
            '@equivalent':  'str',

            'substr':       expand_slice,
            'substr_from':  expand_slice,
            'length':       'len',
            'substr_to':    lambda receiver, to, _: expand_slice(receiver, None, to, pseudo_type='String'),
            'find':         'strings.Index(%{self}, %{0})',
            'count':        'strings.Count(%{self}, %{0})',
            'split':        'strings.Split(%{self}, %{0})',
            'concat':       to_op('+'),
            'contains?':    'strings.Contains(%{self}, %{0})',
            'present?':     present,
            'empty?':       empty,
            'find_from':    lambda f, value, index, _: Node('binary_op', op='+', pseudo_type='Int', left=index, right=Node('static_call',
                                    receiver=local('strings', 'Library'),
                                    message='Index',
                                    args=[
                                        Node('_go_slice_from', sequence=f, from_=index, pseudo_type='String'),
                                        value
                                    ],
                                    pseudo_type='Int')),
            'to_int':       Int
        },
        'Regexp': {
            '@equivalent':   'Regexp',

            'match':        lambda receiver, word, _: method_call(
                                receiver,
                                'FindAllSubmatch',
                                [Node('_go_bytes', value=word, pseudo_type='Bytes'),
                                 to_node(-1)],
                                 pseudo_type='RegexpMatch')
        },
        'RegexpMatch': {
            '@equivalent':  'R',

            'group':        lambda receiver, index, _: Node('index',
                                    sequence=receiver,
                                    index=Node('binary_op', op='+', left=index, right=to_node(1), pseudo_type='Int'),
                                    pseudo_type='String'),

            'has_match':    lambda receiver, _: Node('comparison',
                                    op='!=',
                                    left=receiver,
                                    right=Node('null', pseudo_type='None'),
                                    pseudo_type='Boolean')
        },
        'Set': {
            '@equivalent':  'map[bool]struct{}',

            'length':       'len',
            'contains?':    Contains,
            'present?':     present,
            'empty?':       empty
        },
        'Tuple': {
            '@equivalent':  'L',

            'length':       lambda receiver, _: to_node(len(receiver.pseudo_type) - 1)
        },
        'Array': {
            '@equivalent':  'int[]',

            'length':       lambda receiver, _: to_node(receiver.pseudo_type[2])
        }
    }

    functions = {
        'regexp':  {
            'compile':      'regexp.MustCompile',
            'escape':       'regexp.QuoteMeta'
        },
        'io': {
            'display':      'fmt.Println',
            'read':         Read,
            'read_file':    ReadFile,
            'write_file':   'ioutil.WriteFile'
        },
        'math': {
            'ln':       'math.Log',
            'log':      'math.Log',
            'tan':      'math.Tan',
            'sin':      'math.Sin',
            'cos':      'math.Cos',
            'pow':      'math.Pow'
        },
        'system': {
            'args':         'os.Args!',
            'arg_count':    lambda _: call('len', [attr(local('os', 'Library'), 'Args', ['List', 'String'])], 'Int'),
            
            'index':        lambda value, _: Node('index',
                                                sequence=attr(local('os', 'Library'),
                                                              'Args',
                                                              ['List', 'String']),
                                                index=value,
                                                pseudo_type='String')
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
        },
        'List': {
            'join':     'strings'
        },
        'String': {
            'find':     'strings',
            'count':    'strings',
            'split':    'strings',
            'contains?': 'strings',
            'find_from': 'strings',
            'to_int':   'strconv'
        },
        'system': {
            '@all':     'os'
        }
    }


    errors = {

    }
