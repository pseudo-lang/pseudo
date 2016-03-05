from pseudon.types import *
from pseudon.api_translator import ApiTranslator
from pseudon.pseudon_tree import Node, method_call, call


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

    def begin_placeholder(self, receiver, *args, equivalent):
        return method_call(receiver, 'begin', [])

    def end_placeholder(self, receiver, *args, equivalent):
        return method_call(receiver, 'end', [])

    def new_placeholder(self, receiver, *args, equivalent):
        return Node('new_instance', klass=equivalent, args=[])

    api = {
        'List': {
            '@equivalent':  'vector',

            'push':         '#push_back',
            'insert':       '#insert(%{begin}, %{0})',
            'remove_at':    '#erase(%{begin}, %{0})',
            'length':       '#size'
        },
        'Dictionary': {
        },
        'Enumerable': {
        }
    }

    dependencies = {
        'List': {
            '@all': 'vector',
            'remove': 'algorithm'
        }
    }

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
