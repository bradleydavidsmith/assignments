using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Drill1
{
    // Example of Overloading. Overloading is Compile Time
    // Polymorphism. Implemented with functions using the 
    // same names but with different set of parameters.

    class test1
    {
        public void writeIt(int id)
        {
            Console.WriteLine("id = " + id);
        }

        public void writeIt(string id)
        {
            Console.WriteLine("id = " + id);
        }
    }


    // Example of Overriding, which is run time polymorphism. 
    // Functions in the child class with the same name and
    // Same parameters as the base class, but different behaviors.
    // NOTE: This is also an example of a derived class.
    public class basetest2
    {
        public virtual void writeIt(int id)
        {
            Console.WriteLine("id = " + id);
        }
    }

    public class test3 : basetest2
    {
        public override void writeIt(int id)
        {
            base.writeIt(id);
            Console.WriteLine("From Child Class");
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            test1 A = new test1();
            A.writeIt(1);
            A.writeIt("A");

            basetest2 B = new basetest2();
            B.writeIt(2);

            test3 C = new test3();
            C.writeIt(3);
        }
    }
}
