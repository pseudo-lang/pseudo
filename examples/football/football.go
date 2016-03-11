package main

import (
	"os"
	"strings"
	"fmt"
	"io/ioutil"
	"strconv"
)

func LoadResults(filename string) []Result {
	_contents, _ := ioutil.ReadFile(filename)
	raw := string(_contents)
	lines := strings.Split(raw, "\n")
	var _results []Result
	for _, line := range lines {
		if len(line) > 0 {
			_results = append(_results, ParseResult(line))
		}
	}
	return _results

}

func ParseResult(line string) Result {
	awayIndex := strings.Index(line, " - ") + 3
	resultIndex := awayIndex + strings.Index(line[awayIndex:], " ") + 1
	goals := strings.Split(line[resultIndex:], ":")
	_int, _ := strconv.Atoi(goals[0])
	_int1, _ := strconv.Atoi(goals[1])
	return Result{line[:awayIndex - 3], line[awayIndex:resultIndex - 1], [...]int{_int, _int1}}
}

func CalculatePoints(results []Result, team string) int {
	accumulator := 0
	for _, result := range results {
		accumulator += ResultPoints(team, result)
	}

	return accumulator
}

func ResultPoints(team string, result Result) int {
	if result.Host == team && result.Goals[0] > result.Goals[1] || result.Away == team && result.Goals[0] < result.Goals[1] {
		return 3
	} else if result.Goals[0] == result.Goals[1] && (result.Host == team || result.Away == team) {
		return 1
	} else {
		return 0
	}
}

type Result struct {
	Host string
	Away string
	Goals [2]int
}

func main() {
	if len(os.Args) < 3 {
		fmt.Println("usage: football <stats-file> <team>")
	} else {
		results := LoadResults(os.Args[1])
		fmt.Println(CalculatePoints(results, os.Args[2]))
	}
}
