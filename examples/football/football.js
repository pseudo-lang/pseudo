var _ = require('lodash');
var fs = require('fs');
function load_results(filename) {
  var raw = fs.readFileSync(filename, 'utf8');
  var lines = raw.split('\n');
  return _.filter(lines, function (line) {
    return line;
  }).map(function (line) {
    return parse_result(line);
  });
}

function parse_result(line) {
  var away_index = line.search(' - ') + 3;
  var result_index = away_index + line.slice(away_index).search(' ') + 1;
  var goals = line.slice(result_index).split(':');
  return [line.slice(0, away_index - 3), line.slice(away_index, result_index - 1), [parseInt(goals[0]), parseInt(goals[1])]];
}

function calculate_points(results, team) {
  return _.reduce(results, function (memo, result) {
    return memo + result_points(team, result[0], result[1], result[2]);
  }, 0);
}

function result_points(team, host, away, goals) {
  if (host == team && goals[0] > goals[1] || away == team && goals[0] < goals[1]) {
    return 3;
  } else if (goals[0] == goals[1] && (host == team || away == team)) {
    return 1;
  } else {
    return 0;
  }
}

if (process.argv.length < 4) {
  console.log('usage: football <stats-file> <team>');
} else {
  var results = load_results(process.argv[2]);
  console.log(calculate_points(results, process.argv[3]));
}

