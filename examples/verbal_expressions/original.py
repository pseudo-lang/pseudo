import re

class VerbalExpression:
    def __init__(self):
        self.raw_source = ''

    def compile(self):
        return re.compile(self.raw_source)

    def start_of_line(self):
        self.raw_source += '^'
        return self

    def maybe(self, letter):
        self.raw_source += '(%s)?' % re.escape(letter)
        return self

    def find(self, word):
        self.raw_source += '(%s)' % re.escape(word)
        return self

    def anything_but(self, letter):
        self.raw_source += '[^%s]*' % re.escape(letter)
        return self

    def end_of_line(self):
        self.raw_source += '$'
        return self

    def match(self, word):
        return self.compile().match(word)

    def source(self):
        return self.raw_source


v = VerbalExpression()
a = (v.
        start_of_line().
        find('http').
        maybe('s').
        find('://').
        maybe('www.').
        anything_but(' ').
        end_of_line())

test_url = 'https://www.google.com'
if a.match(test_url):
    print('Valid URL')
else:
    print('Invalid URL')
print(a.source())
