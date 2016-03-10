var _ = require('lodash');

function VerbalExpression() {
  this.raw_source = '';
}

VerbalExpression.prototype.compile = function () {
  return new RegExp(this.raw_source);
}

VerbalExpression.prototype.start_of_line = function () {
  this.raw_source += '^';
  return this;
}

VerbalExpression.prototype.maybe = function (letter) {
  this.raw_source += '(' + _.escapeRegExp(letter) + ')?';
  return this;
}

VerbalExpression.prototype.find = function (word) {
  this.raw_source += '(' + _.escapeRegExp(word) + ')';
  return this;
}

VerbalExpression.prototype.anything_but = function (letter) {
  this.raw_source += '[^' + _.escapeRegExp(letter) + ']*';
  return this;
}

VerbalExpression.prototype.end_of_line = function () {
  this.raw_source += '$';
  return this;
}

VerbalExpression.prototype.match = function (word) {
  return this.compile().exec(word);
}

VerbalExpression.prototype.source = function () {
  return this.raw_source;
}

var v = new VerbalExpression();
var a = v.start_of_line().find('http').maybe('s').find('://').maybe('www.').anything_but(' ').end_of_line();
var test_url = 'https://www.google.com';
if (a.match(test_url)) {
  console.log('Valid URL');
} else {
  console.log('Invalid URL');
}

console.log(a.source());