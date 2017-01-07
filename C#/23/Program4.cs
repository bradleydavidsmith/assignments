using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Xml.Serialization;

namespace Test
{
    class Program
    {
        class EStuff
        {
            static public void Serialize(byte[] blob)
            {
                XmlSerializer serializer = new XmlSerializer(typeof(byte[]));
                using (TextWriter writer = new StreamWriter(@"C:\Users\Brad\Desktop\blob.xml"))
                {
                    serializer.Serialize(writer, blob);
                }
            }

            static public void Deserialize(out byte[] blob)
            {
                XmlSerializer deserializer = new XmlSerializer(typeof(byte[]));
                using (TextReader reader = new StreamReader(@"C: \Users\Brad\Desktop\blob.xml"))
                {
                    object obj = deserializer.Deserialize(reader);
                    blob = (byte[])obj;
                }
            }
        }

        static void Main(string[] args)
        {

            // Make a Blob
            byte[] blob = File.ReadAllBytes(@"C:\Users\Brad\Desktop\pig-carrying.png");
            byte[] deblob;

            // Serialize it:
            EStuff.Serialize(blob);

            // Deserialize it:
            EStuff.Deserialize(out deblob);

            // As a check, write out the desialized blob
            File.WriteAllBytes(@"C:\Users\Brad\Desktop\fic.jpg", deblob);


        }
    }
}
