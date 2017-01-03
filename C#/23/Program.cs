using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ModLibrary;

namespace Drill2
{
    // PUBLIC, PRIVATE
    class ModA
    {
        // Since the public keyword is not used, this is private by default:
        static void A()
        {
            Console.WriteLine("ModA A");
        }

        public static void B()
        {
            Console.WriteLine("ModA B");
            A();
        }
    }

    class ModB
    {
        protected static void A()
        {
            Console.WriteLine("ModB A");
        }

        public static void B()
        {
            Console.WriteLine("ModB B");
            A();


        }
    }

    // MODIFIERS IN INHERITANCE
    class ModBase
    {
        static void A()
        {
            Console.WriteLine("ModBase A");
        }

        public static void B()
        {
            Console.WriteLine("ModBase B");
        }

        protected static void C()
        {
            Console.WriteLine("ModBase C");
        }
    }

    class ModDerived:ModBase
    {
        public static void X()
        {
            //A(); Causes error, A not accessable from derived class
            B();
            C();
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            // B is public, so this works
            ModA.B();

            // A is not marked public, so is private by default. So the following line results
            // in the error: 'ModA.A()' is inaccessible due to its protection level
            //
            // ModA.A();

            ModB.B();

            // ModB.A(): // Results in error because A is protected

            ModDerived.X();
            
            ModLibA mla = new ModLibA();
            mla.MethodA();

            Console.ReadKey();
        }
    }
}
