def load_results(filename)
  raw = File.read(filename)
  lines = raw.split("\n")
  lines.select { |line| !line.empty? }.map { |line| parse_result(line) }
end

def parse_result(line)
  away_index = line.index(' - ') + 3
  result_index = line.index(' ', away_index) + 1
  goals = line[result_index..-1].split(':')
  [line[0...away_index - 3], line[away_index...result_index - 1], [goals[0].to_i, goals[1].to_i]]
end

def calculate_points(results, team)
  results.reduce(0) { |memo, result| memo + result_points(team, result[0], result[1], result[2]) }
end

def result_points(team, host, away, goals)
  if host == team && goals[0] > goals[1] || away == team && goals[0] < goals[1]
    3
  elsif goals[0] == goals[1] && (host == team || away == team)
    1
  else
    0
  end

end

if ARGV.length < 2
  puts 'usage: football <stats-file> <team>'
else
  results = load_results(ARGV[0])
  puts calculate_points(results, ARGV[1])
end

