using System;
public class Program
{
    static int Fib(int n)
    {
        if (n <= 1)
        {
            return 1;
        }
        else 
        {
            return Fib(n - 1) + Fib(n - 2);
        }
    }

    public static void Main(string[] args)
    {
        Console.WriteLine(Fib(4));
    }
}
