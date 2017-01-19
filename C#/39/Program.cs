// Program: Bulk Copy: Excel to SQL Server Database
// Author: Brad Smith
// Date: 1/18/2017
//
// Purpose: This program performs a bulk copy of data from an Excel 
// spreadsheet to a SQL Server Database Table
//


using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Data.OleDb;
using System.Data.SqlClient;

namespace ExcelToSQLBulkCopy
{
    class Program
    {
        static void EToSQL()
        {
            // Set initial parameters (Future enhancement: Set by a GUI
            string excelFilePath = @"F:\Courses\Tech Academy\12 C#\39\Test1.xlsx";
            string sourceConnectionString = GetExcelConnectionString(excelFilePath);
            string destConnectionString = GetDBConnectionString();
            string sqlTable = "Table1";

            // Open a SQL connection to count the number rows in the table.
            using (SqlConnection sqlConnection =
                        new SqlConnection(destConnectionString))
            {
                sqlConnection.Open();

                // Perform an initial row count on the destination table.
                SqlCommand commandRowCount = new SqlCommand(
                    "SELECT COUNT(*) FROM " +
                    sqlTable + ";",
                    sqlConnection);
                long countStart = System.Convert.ToInt32(
                    commandRowCount.ExecuteScalar());
                Console.WriteLine("Starting row count = {0}", countStart);

                // Open a OleDbConnection to the Excel spreadsheet
                using (OleDbConnection sourceOleDbConnection =
                                new OleDbConnection(sourceConnectionString))
                {
                    sourceOleDbConnection.Open();

                    // Get data from the Excel spreadsheet as a OleDb DataReader.
                    OleDbCommand oledbcmd = new OleDbCommand(
                        "SELECT student,rollno,course " +
                        "FROM [Sheet1$]", sourceOleDbConnection);
                    OleDbDataReader reader =
                        oledbcmd.ExecuteReader();

                    // Set up the bulk copy object using a connection string.
                    using (SqlBulkCopy bulkCopy =
                               new SqlBulkCopy(destConnectionString))
                    {
                        bulkCopy.DestinationTableName = sqlTable;

                        try
                        {
                            // Write from the source(the spreadsheet) 
                            // to the destination (a database table)
                            bulkCopy.WriteToServer(reader);
                        }
                        catch (Exception ex)
                        {
                            Console.WriteLine(ex.Message);
                        }
                        finally
                        {
                            // Close the OleDb DataReader. The SqlBulkCopy
                            // object is automatically closed at the end
                            // of the using block.
                            reader.Close();
                        }

                        // Perform a final count on the destination
                        // table to see how many rows were added.
                        long countEnd = System.Convert.ToInt32(
                            commandRowCount.ExecuteScalar());
                        Console.WriteLine("Ending row count = {0}", countEnd);
                        Console.WriteLine("{0} rows were added.", countEnd - countStart);
                        Console.WriteLine("Press Enter to finish.");
                        Console.ReadLine();
                    }
                }
            }
        }


        private static string GetExcelConnectionString(string excelFilePath)
        {
            return "Provider=Microsoft.ACE.OLEDB.12.0;" +
                    "Data Source=\"" + excelFilePath +
                    "\";Extended Properties=Excel 12.0";
        }



        private static string GetDBConnectionString()
        // To avoid storing the sourceConnection string in the code, 
        // it can be retrieved from a configuration file instead.
        {
            return @"Server=HOME\SQLSERVER2012; " +
                    "Database=LoadTest;" +
                    "Integrated Security=True";
        }



        static void Main(string[] args)
        {
            EToSQL();
        }
    }
}
