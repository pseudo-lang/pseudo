class VerbalExpression
  def initialize
    @raw_source = ''
  end

  def compile
    /#{@raw_source}/
  end

  def start_of_line
    @raw_source += '^'
    self
  end

  def maybe(letter)
    @raw_source += "(#{Regexp.escape(letter)})?"
    self
  end

  def find(word)
    @raw_source += "(#{Regexp.escape(word)})"
    self
  end

  def anything_but(letter)
    @raw_source += "[^#{Regexp.escape(letter)}]*"
    self
  end

  def end_of_line
    @raw_source += '$'
    self
  end

  def match(word)
    word.scan(compile)
  end

  def source
    @raw_source
  end

end

v = VerbalExpression.new
a = v.start_of_line.find('http').maybe('s').find('://').maybe('www.').anything_but(' ').end_of_line
test_url = 'https://www.google.com'
if !a.match(test_url).empty?
  puts 'Valid URL'
else
  puts 'Invalid URL'
end

puts a.source

