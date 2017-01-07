using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Drill3
{
    class Program
    {
        // DIFFERENCES BETWEEN ABSTRACT CLASSES AND AN INTERFACE
        // On the differences between abstract classes and interfaces
        // The documentation I've read says that there really isn't much
        // except for the keyword "abstract".

        // The main difference is that a class can only inherit from one base
        // class, but can implement multiple interfaces. Another difference
        // is that abstract classes can implement methods that can be
        // overidded, but interfaces can't. They can only have
        // method signatures.

        // Example of an abstract class. Used to create a base class.
        // You can't create objects of this type, just inherit from it.
        abstract class FourLeggedAnimal
        {
            // The "virtual" keyword allows the class to be overridden in
            // derived classes
            public virtual string Describe()
            {
                return "Not much is known, but it does have 4 legs!";
            }
        }

        // Derived class inheriting from a base class:
        abstract class Dog : FourLeggedAnimal
        {
            public override string Describe()
            {
                return base.Describe() + " Plus it's a dog!";

            }
        }

        // Example of an a class implementing multiple interfaces:
        public interface IFirst { void FirstMethod(); }
        public interface ISecond { void SecondMethod(); }


        public class FirstAndSecond : IFirst, ISecond
        {
            void IFirst.FirstMethod() { Console.WriteLine("IFirst.FirstMethod"); }
            void ISecond.SecondMethod() { Console.WriteLine("ISecond.SecondMethod"); }

        }

        // EXAMPLE OF A DELEGATE:
        class DelegateDemo1
        {
            // The Delegate
            delegate void PointToSub(int numberOne, int numberTwo);

            static public void Demo()
            {
                PointToSub pointToSub = SubTwoNumbers;

                // Invoking the delegate:
                pointToSub.Invoke(30, 10);
            }

            static void SubTwoNumbers(int num1, int num2)
            {
                Console.WriteLine((num1 - num2).ToString());
            }
        }

        // MultiCast Delegates: assign multiple methods to a delegate, and 
        // Invoke them in the order assigned.

        public class DelegateDemo2
        {
            delegate void SendMessage();

            public class Broadcast
            {
                static public void ViaSMS()
                {
                    Console.WriteLine("Message Send to cell phone.");
                }

                static public void ViaEmail()
                {
                    Console.WriteLine("Email send to mailbox.");
                }

                static public void ViaFax()
                {
                    Console.WriteLine("Message send via fax.");
                }
            }

            static public void Demo()
            {
                Broadcast broadcast = new Broadcast();
                SendMessage sendMessage = Broadcast.ViaSMS;
                sendMessage += Broadcast.ViaFax;
                sendMessage += Broadcast.ViaEmail;
                sendMessage.Invoke();
            }

        }

        // CREATION OF A STRUCT:
        // A structure is like a class, except it can't inherit.
        // Also, Structs are value types. Classes are reference types. 
        // This means structs, like all value types, always have a value.
        struct myStruct
        {
            private int xval;
            public int X
            {
                get
                {
                    return xval;
                }
                set
                {
                    if (value < 100)
                        xval = value;
                }
            }
            public void DisplayX()
            {
                Console.WriteLine("The stored value is: {0}", xval);
            }
        }

        class TestClass
        {
            public static void TestIt()
            {
                myStruct ms = new myStruct();
                ms.X = 5;
                ms.DisplayX();
                Console.WriteLine("The getter returns: {0}", ms.X);
            }
        }

        // NULLABLE TYPES
        class NullableDemo
        {
            static public void Demo()
            {

                int? num = null;
                Nullable<int> num2 = 4;

                // Because num2 is null, num3 will be null:
                int? num3 = num + num2;

                // Assign the default value for a nullable, if num is null:
                int? num4 = num ?? -85;

                if (num.HasValue)
                {
                    System.Console.WriteLine(num.Value);
                }
                else
                {
                    System.Console.WriteLine("num Undefined");
                }

                if (num2.HasValue)
                {
                    System.Console.WriteLine(num2.Value);
                }
                else
                {
                    System.Console.WriteLine("num2 Undefined");
                }

                //Set y to num's default value, zero:
                int y = num.GetValueOrDefault();

                // num.Value throws an InvalidOperationException if num.HasValue is false
                try
                {
                    y = num.Value;
                }
                catch (System.InvalidOperationException e)
                {
                    System.Console.WriteLine(e.Message);
                }
            }
        }

        class EnumDemo
        {
            // Simple Demo:
            static public IEnumerable<int> YieldReturn()
            {
                yield return 1;
                yield return 2;
                yield return 3;
            }

            static public IEnumerable<int> GetNumbers(int min, int max)
            {
                for (; min <= max; min++)
                    yield return min;
            }
        }

        static void Main(string[] args)
        {
            DelegateDemo1.Demo();
            DelegateDemo2.Demo();
            TestClass.TestIt();
            NullableDemo.Demo();

            // Simple Enumerable Demo 1
            foreach (int i in EnumDemo.YieldReturn())
            {
                Console.WriteLine(i);
            }

            // Simple Enumerable Demo 2
            foreach (int i in EnumDemo.GetNumbers(0,10))
            {
                Console.WriteLine(i);
            }

            Console.Read();
        }
    }
}
