class NeptunError(Exception):
    pass

class IntergallacticError(NeptunError):
    pass

f = 2
try:
    f = 2
    if f == 2:
        raise NeptunError('why f')

    h = 2
except IntergallacticError as e:
    print(e)

except NeptunError as e:
    print(e)



