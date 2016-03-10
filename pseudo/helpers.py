def serialize_type(l):
    if isinstance(l, str):
        return l
    elif isinstance(l, list):
        return '%s[%s]' % (l[0], ', '.join(map(serialize_type, l[1:])))
    else:
        return str(l)

def safe_serialize_type(l):
    '''serialize only with letters, numbers and _'''

    if isinstance(l, str):
        return l
    elif isinstance(l, list):
        return '%s_%s_' % (l[0], ''.join(map(safe_serialize_type, l[1:])))
    else:
        return str(l)

def general_type(l):
    if isinstance(l, list):
        return l[0]
    else:
        return l

def camel_case(t):
    return t.title().replace('_', '')

def snake_case(t):
    if not t:
        return t
    words = t[0]
    for letter in t[1:]:
        if letter.isupper():
            words.append(letter)
        else:
            words[-1] += letter
    return '_'.join(words)
