using System;
using System.Text;
using System.Collections.Generic;
using System.Linq;
using System.IO;

public class Program
{
    static List<Tuple<string, string, int[]>> LoadResults(string filename)
    {
        var raw = File.ReadAllText(filename);
        var lines = raw.Split('\n');
        return lines.Where(
            line => line.Length != 0
        ).Select(
            line => ParseResult(line)
        ).ToList();
    }

static Tuple<string, string, int[]> ParseResult(string line)
    {
        var awayIndex = line.IndexOf(" - ") + 3;
        var resultIndex = line.IndexOf(" ", awayIndex) + 1;
        var goals = line.Substring(resultIndex).Split(':');
        return Tuple.Create(
            line.Substring(0, awayIndex - 3),
            line.Substring(awayIndex, resultIndex - 1 - awayIndex),
            new[] { Int32.Parse(goals[0]), Int32.Parse(goals[1]) }
        );
    }

static int CalculatePoints(List<Tuple<string, string, int[]>> results, string team)
    {
        return results.Aggregate(0, (memo, result) => memo + ResultPoints(team, result.Item1, result.Item2, result.Item3));
    }

static int ResultPoints(string team, string host, string away, int[] result)
    {
        if (host == team && result[0] > result[1] || away == team && result[0] < result[1])
        {
            return 3;
        }
        else if (result[0] == result[1] && (host == team || away == team))
        {
            return 1;
        }
        else 
        {
            return 0;
        }
    }

    public static void Main(string[] args)
    {
        if (args.Length < 2)
        {
            Console.WriteLine("usage: football <stats-file> <team>");
        }
        else 
        {
            var results = LoadResults(args[0]);
            Console.WriteLine(CalculatePoints(results, args[1]));
        }
    }
}
