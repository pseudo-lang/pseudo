using System;
using System.Text.RegularExpressions;
using System.Text;

public class VerbalExpression
{
    private string rawSource;

    public VerbalExpression()
    {
        this.rawSource = "";
    }

    public Regex Compile()
    {
        return new Regex(this.rawSource);
    }

    public VerbalExpression StartOfLine()
    {
        this.rawSource += "^";
        return this;
    }

    public VerbalExpression Maybe(string letter)
    {
        this.rawSource += string.Format("({0})?",  Regex.Escape(letter));
        return this;
    }

    public VerbalExpression Find(string word)
    {
        this.rawSource += string.Format("({0})",  Regex.Escape(word));
        return this;
    }

    public VerbalExpression AnythingBut(string letter)
    {
        this.rawSource += string.Format("[^{0}]*",  Regex.Escape(letter));
        return this;
    }

    public VerbalExpression EndOfLine()
    {
        this.rawSource += "$";
        return this;
    }

    public Match Match(string word)
    {
        return this.Compile().Match(word);
    }

    public string Source()
    {
        return this.rawSource;
    }
}

public class Program
{
    public static void Main(string[] args)
    {
        var v = new VerbalExpression();
        var a = v.StartOfLine().Find("http").Maybe("s").Find("://").Maybe("www.").AnythingBut(" ").EndOfLine();
        var testUrl = "https://www.google.com";
        if (a.Match(testUrl).Success)
        {
            Console.WriteLine("Valid URL");
        }
        else 
        {
            Console.WriteLine("Invalid URL");
        }

        Console.WriteLine(a.Source());
    }
}
