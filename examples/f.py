def f():
    return ''

print(f())
try:
    2
    f()
except Exception as e:
    print(e)



