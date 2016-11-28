##############################################
# Title: Backup *.txt Files
#
# Written for: Python 3.4.3
#
# Purpose: To copy all files modified or
#    created in the last 24 hours
#
#
# Author: Brad Smith
#
# DESIGN DECISIONS:
#
# DATE IN SQLITE
# Since SQLite does not have a date type,
# there are 3 options for timestamps,
# outlined in paragraph 2.2 of this page:
# https://www.sqlite.org/datatype3.html
#
# I chose to use a timestamp (INTEGER)
# since it takes up the least space and
# I was most familiar with the functions
# in Python for dealing with converting
# an integer timestamp to a date.
# 
# DB REPRESENTATION USED:
# I also chose to store the last back up
# date in a configuration table in the
# database that I called intconfig.
#
# The intconfig table is a set of key/value
# pairs, where the values are integers.
# Currently, there is only 1 pair
# in the database, a key/value pair with
# the key of "budate" that returns the
# timestamp integer representation of
# date of the last backup. The configuration
# table is now available for future enhancements
# that might have other configuration
# key/value pairs to store.
#
#
# FUTURE ENHANCEMENTS:
# 1) Change the button's color as it copies
# 2) Enable the y-scroll bar, and turn off
#    text wrap in the text box, so the user
#    can copy out cleaner looking text.
# 3) Pretty up the UI. Style it up, instead
#    of using the default sizes.
#
# 4) Add error handling of the dB. Right
#    now, the program assumes that if the
#    db file exists, that the table and
#    columns also exist.
#
# 5) Add which folders have been backed up
#    (along with the backup date of the
#    individual folders) to the database.
#
# 6) Especially when there are more key/value
#    pairs in the inconfig table, download the
#    entire table into a dictionary, instead
#    of accessing the dB table for every
#    key/value pair. For efficiency.
#
# 7) Account for daylight savings time. For
#    example, if a backup starts at 1:30 AM
#    the day of the time change, where
#    2 PM daylight time changes to 1 PM
#    standard time, files edited between
#    1-1:30 PM standard time won't be
#    backed up in the next backup.
#
##############################################

from tkinter import *
from tkinter import ttk
import os, shutil, time, datetime, sqlite3

class BigCopy:

    def __init__(self, root):

        # The name of the database file
        self.dbfile = 'bu.db'

        # Access the dB to access that last backup date
        self.lastbudateTS = self.getLastBUDate()
        self.lastbudate = datetime.datetime.fromtimestamp(self.lastbudateTS)

        # Setup of the root window
        root.title('The Big Text File Copy')
        root.resizable(False, False)

        # Create the top Frame area to hold the date field, selectors
        # for the 2 folders, along with the copy button
        self.frame1 = Frame(root, bd=2, relief=SUNKEN)
        self.frame1.pack(side=TOP)

        # Display the last backup date on the GUI. 
        if self.lastbudateTS == 0:
            lastbudatestring = "Not Backed Up"
        else:
            lastbudatestring = datetime.datetime.fromtimestamp(self.lastbudateTS).strftime('%Y-%m-%d %H:%M:%S')
        self.lbuDate = ttk.Label(self.frame1, text = "Last Backed Up: " + lastbudatestring)
        self.lbuDate.grid(row = 0, column = 3, sticky = N)   

        # Entry field for the source Folder
        self.src = StringVar()
        self.slabel = ttk.Label(self.frame1, text = "Enter the text file source folder:")
        self.sfolder = ttk.Entry(self.frame1, width = 60, textvariable = self.src)#, validate="all", validatecommand = self.validate)
        self.src.trace("w", self.validate)
        self.sbrowseBut = ttk.Button(self.frame1, text = "Browse...", command = self.sourceFolder)
        self.slabel.grid(row = 1, column = 1, sticky = W)
        self.sfolder.grid(row = 1, column = 2, columnspan = 5)
        self.sbrowseBut.grid(row = 1, column = 7, sticky = E)

        # Entry field for the destination Folder
        self.dst = StringVar()
        self.dlabel = ttk.Label(self.frame1, text = "Enter the text file destination folder:")
        self.dfolder = ttk.Entry(self.frame1, width = 60, textvariable = self.dst)#, validate=ALL, validatecommand = self.validate)
        self.dst.trace("w", self.validate)
        self.dbrowseBut = ttk.Button(self.frame1, text = "Browse...", command = self.destFolder)
        self.dlabel.grid(row = 2, column = 1, sticky = W)
        self.dfolder.grid(row = 2, column = 2, columnspan = 5)
        self.dbrowseBut.grid(row = 2, column = 7, sticky = E)

        # Create the Copy button
        self.b = Button(self.frame1, text="Copy", command=self.copyThem, state=DISABLED)
        self.b.grid(row = 3, column = 3, sticky = S)

        # Create the frame to hold the text box and scroll bar
        self.frame2 = Frame(root, bd=2, relief=SUNKEN)
        self.frame2.pack(side=TOP)

        self.frame2.grid_rowconfigure(0, weight=1)
        self.frame2.grid_columnconfigure(0, weight=1)

        self.yscrollbar = Scrollbar(self.frame2)
        self.yscrollbar.grid(row=0, column=1, sticky=N+S)

        self.text = Text(self.frame2, wrap=WORD, bd=0,
                    yscrollcommand=self.yscrollbar.set,
                    state = DISABLED)

        # Test Code:
        #self.text.config(state = NORMAL)
        #self.text.insert(END, test)
        #self.text.config(state = DISABLED)

        self.text.grid(row=0, column=0, sticky=N+S+E+W)

        self.yscrollbar.config(command=self.text.yview)


    # The Text File Source Folder Picker Method
    # Displays a dialog box for the user to pice the source folder
    def sourceFolder(self):
        folder = filedialog.askdirectory()
        self.sfolder.delete(0,END)
        self.sfolder.insert(0, folder)
        self.validate()


    # The Text File Dest. Folder Picker Method
    # Displays a dialog box for the user to pice the destination folder
    def destFolder(self):
        folder = filedialog.askdirectory()
        self.dfolder.delete(0,END)
        self.dfolder.insert(0, folder)
        self.validate()


    # Validate the source and destination folders BEFORE turning on the Copy button.
    # This routine is called whenever you make a change in either of the two
    # folder fields.
    def validate(self, *args):

        # Source exists and is a folder:
        sourceIsFolder = os.path.isdir(self.src.get())

        # Destination exists and is a folder:
        destIsFolder = os.path.isdir(self.dst.get())

        # True if The Source and Destination are valid
        allValid = sourceIsFolder and destIsFolder

        # True if both the source and destination are the same file
        bothEqu = self.src.get().strip() == self.dst.get().strip()

        # If both folders are valid, and are different, enable the button 'b'
        self.b.config(state = NORMAL if allValid and not(bothEqu) else DISABLED)

        return True;


    def getLastBUDate(self):
        if os.path.exists(self.dbfile): # Assume everything's OK
            with SQLite(self.dbfile) as db:
                db.cur.execute('SELECT value FROM intconfig WHERE item = "budate"')
                timeStamp = db.cur.fetchone()[0]
                #print (timeStamp)
                
        else:
            with SQLite(self.dbfile) as db: # Create the db & table with columns
                db.cur.execute("CREATE TABLE IF NOT EXISTS intconfig (" 
                    "item TEXT NOT NULL UNIQUE," 
                    "value INTEGER," 
                    "PRIMARY KEY(item));")
                db.cur.execute('INSERT INTO intconfig VALUES ("budate", 0)')
                db.conn.commit()
                db.cur.execute('SELECT value FROM intconfig WHERE item = "budate"')
                #print ("row count = ", db.cur.rowcount)
                timeStamp = db.cur.fetchone()[0]
        return timeStamp

    def setLastBUDate(self, timeStamp):
        with SQLite(self.dbfile) as db:
            db.cur.execute('UPDATE intconfig SET value = ? WHERE item = "budate"', (timeStamp,))
            db.conn.commit()
        
 
    def getModificationDate(self, filename):
        t = os.path.getmtime(filename)
        return datetime.datetime.fromtimestamp(t)


    def getCreationDate(self, filename):
        t = os.path.getctime(filename)
        return datetime.datetime.fromtimestamp(t)

    # Destructive Copy
    def dCopy(self, srcFile, dstFile, dstDir):
        if os.path.exists(dstFile):
            os.remove(dstFile)
        shutil.copy2(srcFile, dstDir)
        
    # The copyThem method for button 'b' does all the work of copying the .txt files:
    def copyThem(self):

        # Count all the .txt files that were copied
        txtcount = 0

        # Make it so this routine can write to the text box
        self.text.config(state = NORMAL)
        
        # Record the time the backup starts
        currbudate = datetime.datetime.now()
        # T24HoursAgo = now - datetime.timedelta(hours = 24)
        
        for file in os.listdir(self.src.get()):
            if file.endswith(".txt"):
                
                srcFile = os.path.join(self.src.get(), file)
                dstFile = os.path.join(self.dst.get(), file)
                modDate = self.getModificationDate(srcFile)
                mDateStr = modDate.strftime('%Y-%m-%d %H:%M:%S')
                creDate = self.getCreationDate(srcFile)
                cDateStr = creDate.strftime('%Y-%m-%d %H:%M:%S')

                # Copy if modified or created since the last backup
                if modDate > self.lastbudate:
                    # Copy the recently modified file
                    self.text.insert(END, srcFile + " last modified " + \
                        mDateStr + " so copying to " + self.dst.get() + ".\n")
                    self.dCopy(srcFile, dstFile, self.dst.get()) 
                    txtcount += 1
                elif creDate > self.lastbudate:
                    # Copy the recently created file
                    self.text.insert(END, srcFile + " was created " + \
                        cDateStr + " so copying to " + self.dst.get() + ".\n")
                    self.dCopy(srcFile, dstFile, self.dst.get())
                    txtcount += 1
                else:  
                    self.text.insert(END, srcFile + " was created " + \
                        cDateStr + " and last modified " + mDateStr + \
                        " so not copied...\n")

                # Be sure the bottom of the window text area is showing
                self.text.see(END)
                self.frame2.update_idletasks()

                # For testing delay slightly to make sure text is being
                # added as the copies are being performed, not all at the end.
                #time.sleep(0.2)
                    
        # print a summary
        self.text.insert(END, "\nNumber of *.txt files copied: " + str(txtcount) + "\n")
        self.text.insert(END, "Backup Complete through: " + currbudate.strftime('%Y-%m-%d %H:%M:%S') + "\n")

        # move the focus to make sure the last line written is displayed at the bottom of the window
        self.text.see(END)

        # Make the textbox read-only again
        self.text.config(state = DISABLED)

        # Update the last time backed up in both the dB and at the top of the form
        self.setLastBUDate(currbudate.timestamp())
        currbudateStr = currbudate.strftime('%Y-%m-%d %H:%M:%S')
        self.lbuDate.config(text = "Last Backed Up: " + currbudateStr)
        

##################################################################
# This will let you use the class either as a db = SQLite(dbfile)
# or in a with statement:
#
#    with SQLite(dbfile) as db:
#        # do stuff with db
# Adapted from code located at:
# http://stackoverflow.com/questions/38076220/python-mysqldb-connection-in-a-class
#
# The cool thing about this class is that SQLite objects will
# automatically close the dB connection at the end of a with
# statement, or when they go out of scope. Or, when the program
# ends.
##################################################################
class SQLite:

    def __init__(self, dbfile):
        self.dbfile = dbfile
        dsn = (self.dbfile,)
        self.conn = sqlite3.connect(*dsn)
        self.cur = self.conn.cursor()

    def __enter__(self):
        return SQLite(self.dbfile)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()


def main():            
    
    root = Tk()
    feedback = BigCopy(root)
    root.mainloop()
    
if __name__ == "__main__": main()
