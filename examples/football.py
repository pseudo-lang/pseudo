import sys

def load_results(filename):
    with open(filename, 'r') as f:
        raw = filename.read()

    lines = raw.split('\n') # readlines support in v0.3
    return [parse_result(line) for line in lines]

def parse_result(line):
    away_index = line.index(' - ') + 3
    result_index = line.index(' ', away_index) + 1
    goals = line[result_index:].split(':')
    return line[:away_index - 3], line[away_index:result_index - 1], (int(goals[0]), int(goals[1]))

def calculate_points(results, team): # call(*arg) supported only for tuples
    return sum(result_points(*result, team) for result in results)

def result_points(host, away, goals, team):
    if host == team and result[0] > result[1] or away == team and result[0] < result[1]:
        return 3
    elif result[0] == result[1] and (host == team or away == team):
        return 1
    else:
        return 0

if len(sys.argv) < 2:
    print('usage: football <stats-file> <team>')
else:
    results = load_results(sys.argv[1])
    print(calculate_points(results, sys.argv[2]))
