using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

/////////////////////////////////////////////////////////////////
//
// File Move
//
// DESCRIPTION:
//    Copies all the files from a directory to another if
//    the file was modified in the last 24 hours
//
// WRITTEN FOR: Python 2.7.9
//
// WRITTEN BY: Brad Smith
//
// FUTURE ENHANCEMENTS:
//    1) This program's purpose is to do a backup of the directory.
//       Instead of counting on it being run every 24 hours, have
//       the program keep a database of backed up files, and only
//       back up files that changed in the last 24 hours.
//
//    2) Have the program back up the entire directory structure
//       instead of just a single directory
//////////////////////////////////////////////////////////////////

namespace FileMove24
{
    class Program
    {
        DateTime getModificationDate(string filename)
        {
            return File.GetLastWriteTime(filename);
        }

        DateTime getCreationDate(string filename)
        {
            return File.GetCreationTime(filename);
        }

        public class FM24
        {
            public static void FileMove24()
            {
                // Make the 2 file folder name:
                string desktopFolder = Environment.GetFolderPath(Environment.SpecialFolder.Desktop);
                string src = Path.Combine(desktopFolder, "Folder A");
                string dst = Path.Combine(desktopFolder, "Folder B");
                //Console.WriteLine(src);
                //Console.WriteLine(dst);

                // Make sure the src folder exists
                if (!Directory.Exists(src))
                {
                    //Console.WriteLine(String.Format("Folder '{0}' does not exist.", src));
                    throw new DirectoryNotFoundException(String.Format("Source Folder '{0}' not found.", src));
                }

                // Create the dst folder if it doesn't exist
                // You don't need to check to see if it already exists like in other languages.
                // According to the Docs, if the folder exists, this doesn't do anything.
                System.IO.Directory.CreateDirectory(dst);

                // Determine the date/time from 24 hours ago:
                DateTime T24HoursAgo = DateTime.Now.AddDays(-1);

                // Create a DirectoryInfo of the source directory of the files, to enumerate.
                DirectoryInfo DirInfo = new DirectoryInfo(@src);

                // LINQ query for all files created or modified in the last 24 hours
                var files = from f in DirInfo.EnumerateFiles()
                            where (f.CreationTimeUtc > T24HoursAgo)
                            || (f.LastWriteTimeUtc > T24HoursAgo)
                            select f;

                // Copy the files
                foreach (FileInfo file in files)
                {
                    if (file.CreationTimeUtc > T24HoursAgo)
                        Console.WriteLine(String.Format("{0} was created {1} so copying to {2}", file.FullName, file.CreationTimeUtc, dst));
                    else if (file.LastWriteTimeUtc > T24HoursAgo)
                        Console.WriteLine(String.Format("{0} was last modified {1} so copying to {2}", file.FullName, file.LastWriteTimeUtc, dst));

                    File.Copy(file.FullName, Path.Combine(dst, file.Name), true);

                    //Console.WriteLine(Path.Combine(dst, file.Name));

                    //Console.WriteLine(file.FullName + " " + T24HoursAgo);
                }

                // Write out the number of files copied
                Console.WriteLine(String.Format("Number of *.txt files copied: {0}", files.Count()));
            }
        }



        static void Main(string[] args)
        {
            FM24.FileMove24();
        }
    }
}
