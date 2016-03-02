using System.Collections.Generic;

public class Program
{
    static int f(Dictionary<int, int> h)
    {
        return h[2];
    }


    public static void Main()
    {
        f(new Dictionary<int, int> { {2, 2} });
    }
}
