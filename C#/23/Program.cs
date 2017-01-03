using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Drill2
{
    class ModA
    {
        private static void A()
        {
            Console.WriteLine("ModA A");
        }

        public static void B()
        {
            Console.WriteLine("ModA B");
            A();
        }

        class Program
        {
            static void Main(string[] args)
            {
                // B is public, so this works
                ModA.B();
                // A is marked private, so this should result in an error:
                Console.WriteLine("This should be an error:");
                ModA.A();
            }
        }
    }
}
