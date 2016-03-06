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
        return '%s_%s_' % (l[0], ''.join(map(serialize_type, l[1:])))
    else:
        return str(l)
