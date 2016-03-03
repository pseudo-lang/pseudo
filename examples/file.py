f = 'apolonia.txt'
with open(f, 'r') as _f:
    source = _f.read()

print(source.split('\n'))
