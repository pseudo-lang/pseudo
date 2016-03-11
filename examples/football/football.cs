using System;
using System.Text;
using System.Collections.Generic;
using System.Linq;
using System.IO;

public class Result
{
    private readonly string host;
    public string Host { get { return host; } }

    private readonly string away;
    public string Away { get { return away; } }

    private readonly int[] goals;
    public int[] Goals { get { return goals; } }

    public Result(string host, string away, int[] goals)
    {
        this.host = host;
        this.away = away;
        this.goals = goals;
    }
}

public class Program
{
    static List<Result> LoadResults(string filename)
    {
        var raw = File.ReadAllText(filename);
        var lines = raw.Split('\n');
        return lines
            .Where(line => line.Length != 0)
            .Select(line => ParseResult(line))
            .ToList();
    }

    static Result ParseResult(string line)
    {
        var awayIndex = line.IndexOf(" - ") + 3;
        var resultIndex = line.IndexOf(" ", awayIndex) + 1;
        var goals = line.Substring(resultIndex).Split(':');
        return new Result(line.Substring(0, awayIndex - 3), line.Substring(awayIndex, resultIndex - 1 - awayIndex), new[] { Int32.Parse(goals[0]), Int32.Parse(goals[1]) });
    }

    static int CalculatePoints(List<Result> results, string team)
    {
        return results.Aggregate(0, (memo, result) => memo + ResultPoints(team, result));
    }

    static int ResultPoints(string team, Result result)
    {
        if (result.Host == team && result.Goals[0] > result.Goals[1] || result.Away == team && result.Goals[0] < result.Goals[1])
        {
            return 3;
        }
        else if (result.Goals[0] == result.Goals[1] && (result.Host == team || result.Away == team))
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
