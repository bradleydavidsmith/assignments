using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Xml.Serialization;

namespace Drill2
{
    // PUBLIC, PRIVATE
    class ModA
    {
        // private Method:
        private static void A()
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

        // Protected means C() can be accessed by it's own class, 
        // and derived classes.
        protected static void C()
        {
            Console.WriteLine("ModBase C");
        }

        // protected internal means that D can be accessed by it's
        // own class and derived classes. --OR-- it can be accessed by
        // classes in the same assembly.
        protected internal void D()
        {
            Console.WriteLine("ModBase D");
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

    // 'sealed' prevents other classes from inheriting from the class ModC:
    sealed class ModD { }

    //class ModE : ModD { } //causes the error 'Mod E cannot derive from sealed type Modd
    

    // This class cannot be called by programs outside this assembly. Which
    // means outside the .DLL file which contains this class.
    internal class ModC
    {
        public void MethodC() { }
    }

    // INTERFACE
    interface myInterface
    {
        void myMethod();
    }

    class myImplementation : myInterface
    {
        public void myMethod()
        {
            Console.WriteLine("Implementation of myInterface");
        }
    }

    // USE OF THE 'this' KEYWORD. USED TO ACCESS A VARIABLE WHEN ANOTHER
    // VARIABLE IS SHADOWING IT:

    class ModE
    {
        int i;
        int j;
        int k;

        public ModE(int i, int j, int k)
        {
            this.i = i;
            this.j = j;
            this.k = k;
        }
    }

    class ModF
    {
        static public void Serialize(AddressDetails details)
        {
            XmlSerializer serializer = new XmlSerializer(typeof(AddressDetails));
            using (TextWriter writer = new StreamWriter(@"C:\Xml.xml"))
            {
                serializer.Serialize(writer, details);
            }
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            // B is public, so this works
            ModA.B();

            // A is private. So the following line results
            // in the error: 'ModA.A()' is inaccessible due to its protection level
            //
            // ModA.A();

            ModB.B();

            // ModB.A(): // Results in error because A is protected

            ModDerived.X();
            
            // EXAMPLES OF REFERENCE TYPES, classes, string, and array:
            ModC mla = new ModC();
            mla.MethodC();

            string A = "myString";

            int[] odds = new int[] { 1, 3, 5, 7, 9 };

            myImplementation mi = new myImplementation();

            mi.myMethod();

            // TRY, CATCH, FINALLY
            // WRITE EXCEPTION TO LOG FILE
            // ON LOCAL MACHINE
            try
            {
                // Examples of VALUE TYPES:
                int i = 5;
                int j = 10;
                int k = i + j;
                float a = 0.5F;
                bool tf = true;
                char myChar = 'b';

            }
            catch (Exception e)
            {
                // Write error to logfile on local machine:
                string logFile = "Error.txt";

                using (StreamWriter writer = new StreamWriter(logFile, true))
                {
                    writer.WriteLine(e.Message);
                }
            }
            finally
            {
                Console.WriteLine("Executed");
            }

            Console.ReadKey();


        }
    }
}
