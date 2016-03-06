class PseudoType:

    def is_compatible_with(self, other):
        return self.child_of(other) or other.child_of(self)

    def child_of(self, other):
        current = self
        while current is not None:
            if current == other:
                return True
            current = current.parent
        return False


class SimpleType(PseudoType):

    def __init__(self, label, parent=None):
        self.label = label
        self.parent = parent

    def __repr__(self):
        return '~%s' % self.label

    def __eq__(self, other):
        return self.label == other.label

    def __hash__(self):
        return hash(repr(self))


class Any(PseudoType):

    def __eq__(self, other):
        return True

    def is_compatible_with(self, other):
        return True

    def __hash__(self):
        return hash(repr(self))


class Unknown(PseudoType):
    pass


class GenericType(PseudoType):

    def __init__(self, label, generic_args, parent=None):
        self.label = label
        self.generic_args = generic_args
        self.parent = parent

    def __repr__(self):
        return '~%s<%s>' % (self.label, ' '.join(map(repr, self.generic_args)))

    def __eq__(self, other):
        return self.label == other.label and self.generic_args == other.generic_args


class CustomType(PseudoType):

    def __init__(self, label, fields=None, parent=None):
        self.label = label
        self.fields = fields or {}
        self.parent = parent

    def __repr__(self):
        return '~%s!<%s>' % (self.label, ' '.join('%s:%s' % (k, repr(v)) for k, v in self.fields.items()))

    def __eq__(self, other):
        return self.label == other.label


class GenericInstance(PseudoType):

    def __init__(self, generic, args):
        self.generic = generic
        self.args = args

    def __eq__(self, other):
        return self.generic.label == other.generic.label and self.args == other.args

    def __repr__(self):
        return '~%s<%s>' % (self.generic.label, ' '.join(map(repr, self.args)))


Object = SimpleType('Object')
Number = SimpleType('Number', Object)
Int = SimpleType('Int', Number)
Float = SimpleType('Float', Number)
String = SimpleType('String', Object)
Boolean = SimpleType('Boolean', Object)
Null = SimpleType('')
# for now we will support only one instance of a generic type
# we can have List[t], but not List[t, u] in the same time
Collection = GenericType('Collection', ['y', 'z'], Object)
List = GenericType('List', ['t'], Collection)
Dictionary = GenericType('Dictionary', ['k', 'v'], Collection)
t = Any()
Unknown0 = Unknown()

TYPES = {type.label: type for type in [Object, Number, Int, Float, String, Boolean, Null,
                                       Collection, List, Dictionary]}
TYPES['t'] = t
TYPES['@unknown'] = Unknown0
