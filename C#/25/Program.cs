using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Drill
{
    class Program
    {
        static void Main(string[] args)
        {
            // Difference between string and StringBuilder:
            // strings are immutable, StringBuilder is mutable
            // Immutable objects have some good properties,
            // But can cause performance and memory problems:

            // This example creates 1002 strings, of which 1000 are
            // thrown away

            string s = String.Empty;
            for (var i = 0; i < 1000; i++)
            {
                s += i.ToString() + " ";
            }

            // This is the same example, using StringBuilder. 
            // Note that only 1 StringBuilder is created, along
            // with 1 string.

            StringBuilder sb = new StringBuilder();
            for (var i = 0; i < 1000; i++)
            {
                sb.Append(i);
                sb.Append(" ");
            }

            Console.WriteLine("s = " + s);
            Console.WriteLine("sb = " + sb);
        }
    }
}
