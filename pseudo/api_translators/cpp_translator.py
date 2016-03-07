from pseudo.api_translator import ApiTranslator
from pseudo.pseudo_tree import Node, method_call, call, to_node
from pseudo.api_translators.cpp_api_handlers import Read, Slice, ReadFile

class CppTranslator(ApiTranslator):
    '''
    C++ api translator

    The DSL is explained in the ApiTranslator docstring

    C++ specific:

        '%{begin}':
            expands to `%{self}.begin()`, useful for vector methods
        '%{end}':
            expands to `%{self}.end()`, useful for vector methods
        '%{new}':
            expands to `new %{equivalent}`

    '''

    methods = {
        'List': {
            '@equivalent':  'vector',

            'push':         '#push_back',
            'insert':       '#insert(%{begin}, %{0})',
            'remove_at':    '#erase(%{begin}, %{0})',
            'length':       '#size',
            'slice':        Slice,
            'slice_from':   Slice,
            'slice_to':     Slice,
        },
        'Dictionary': {
            '@equivalent':  'unordered_map'
        },
        'String': {
            '@equivalent':  'string',

            'length':       '#length',
            'substr':       '#substr'

        }
    }

    functions = {
        'io': {
            'display':      lambda *args: Node('_cpp_cout', args=list(args[:-1]), pseudo_type=args[-1]),
            'read':         Read,
            'read_file':    ReadFile,
            'write_file':   'write_file'
        },
        'math': {
            'ln':           'log',
            'tan':          'tan'
        }
    }

    dependencies = {
        'List': {
            '@all': ['iostream', 'vector'],
            'remove': 'algorithm'
        },
        'Dictionary': {
            '@all':  ['iostream', 'unordered_map']
        },
        'String': {
            '@all': ['iostream', 'string']
        },
        'Set': {
            '@all': ['iostream', 'set']
        },
        'Tuple': {
            '@all': ['iostream', 'pair', 'tuple']
        },
        'io': {
            'display':  'iostream',
            'read':     ['iostream', 'string'],
            'read_file': ['iostream', 'fstream', 'string'],
            'write_file': ['iostream', 'fstream', 'string']
        },
        'math': {
            '@all': 'math'
        },
        'Exception': {
            '@all': ['stdexcept', 'exception']
        }
    }

    def begin_placeholder(self, receiver, *args, equivalent):
        return method_call(receiver, 'begin', [], 'CppIterator')

    def end_placeholder(self, receiver, *args, equivalent):
        return method_call(receiver, 'end', [], 'CppIterator')

    def new_placeholder(self, receiver, *args, equivalent):
        return Node('new_instance', class_name=equivalent, args=[], pseudo_type=equivalent)


'''

c++: middleware for memory management

add markers for functions:

%lifetime

shared_ptr<Person> person(new Person("peter", 22));
dangling ref: we generate all the code, so we can just never create such
circular: uh uh pls use weak_ptr so maybe
  structs with pointers to a struct of the same type:
    weak_ptr
  what if
    class A:
        b: B
    class B:
        a: A

    a0 = A()
    b0 = B()
    a0.b = b0
    b0.a = a0
    b0.a.b == b0
    hm
    we can follow graphs or always use a weak ref in a class
    to shared_ptr

basically convert all new_instance to shared_ptr
then the variables and arguments too
and similarly change access to pointers from . to ->
and add weak check
'''
