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
# FUTURE ENHANCEMENTS:
# 1) Change the button's color as it copies
# 2) Enable the y-scroll bar, and turn off
#    text wrap in the text box, so the user
#    can copy out cleaner looking text.
# 3) Remove the 0.2 second delay. It's there
#    to make sure lines are written to the
#    screen as soon as they are added to
#    the text object. Otherwise, text
#    isn't written until all the files
#    are copied. 
# 5) Pretty up the UI. Style it up, instead
#    of using the default sizes.
#
##############################################

from tkinter import *
from tkinter import ttk
import os, shutil, time, datetime

class BigCopy:

    def __init__(self, root):
    
        root.title('The Big Text File Copy')
        root.resizable(False, False)

        # Create the top Frame area to hold the selectors
        # for the 2 folders, along with the copy button
        self.frame1 = Frame(root, bd=2, relief=SUNKEN)
        self.frame1.pack(side=TOP)

        # Entry for the source Folder
        self.src = StringVar()
        self.slabel = ttk.Label(self.frame1, text = "Enter the text file source folder:")
        self.sfolder = ttk.Entry(self.frame1, width = 60, textvariable = self.src)#, validate="all", validatecommand = self.validate)
        self.src.trace("w", self.validate)
        self.sbrowseBut = ttk.Button(self.frame1, text = "Browse...", command = self.sourceFolder)
        self.slabel.grid(row = 0, column = 1, sticky = W)
        self.sfolder.grid(row = 0, column = 2, columnspan = 5)
        self.sbrowseBut.grid(row = 0, column = 7, sticky = E)

        # Entry for the destination Folder
        self.dst = StringVar()
        self.dlabel = ttk.Label(self.frame1, text = "Enter the text file destination folder:")
        self.dfolder = ttk.Entry(self.frame1, width = 60, textvariable = self.dst)#, validate=ALL, validatecommand = self.validate)
        self.dst.trace("w", self.validate)
        self.dbrowseBut = ttk.Button(self.frame1, text = "Browse...", command = self.destFolder)
        self.dlabel.grid(row = 1, column = 1, sticky = W)
        self.dfolder.grid(row = 1, column = 2, columnspan = 5)
        self.dbrowseBut.grid(row = 1, column = 7, sticky = E)

        # Define the Copy button
        self.b = Button(self.frame1, text="Copy", command=self.copyThem, state=DISABLED)
        self.b.grid(row = 2, column = 4, sticky = S)

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
    def sourceFolder(self):
        folder = filedialog.askdirectory()
        self.sfolder.delete(0,END)
        self.sfolder.insert(0, folder)
        self.validate()

    # The Text File Dest. Folder Picker Method
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
        
    # The copyThem method for button 'b' does all the work of copying the files:
    def copyThem(self):

        # Count all the .txt files that were copied
        txtcount = 0

        # Make it so this routine can write to the text box
        self.text.config(state = NORMAL)

        # Find what the time was 24 hours ago
        T24HoursAgo = datetime.datetime.now() - datetime.timedelta(hours = 24)
        
        for file in os.listdir(self.src.get()):
            if file.endswith(".txt"):
                
                srcFile = os.path.join(self.src.get(), file)
                dstFile = os.path.join(self.dst.get(), file)
                modDate = self.getModificationDate(srcFile)
                mDateStr = modDate.strftime('%Y-%m-%d %H:%M:%S')
                creDate = self.getCreationDate(srcFile)
                cDateStr = creDate.strftime('%Y-%m-%d %H:%M:%S')

                # Copy if modified or created in the last 24 hours
                if modDate > T24HoursAgo:
                    # Copy the recently modified file
                    self.text.insert(END, srcFile + " last modified " + \
                        mDateStr + " so copying to " + self.dst.get() + ".\n")
                    self.dCopy(srcFile, dstFile, self.dst.get()) 
                    txtcount += 1
                elif creDate > T24HoursAgo:
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
                time.sleep(0.2)
                    
        # print a summary
        self.text.insert(END, "\nNumber of *.txt files copied: " + str(txtcount) + "\n")

        # move the focus to make sure the last line written is showing at the bottom of the window
        self.text.see(END)

        # Make the textbox read-only again
        self.text.config(state = DISABLED)

def main():            
    
    root = Tk()
    feedback = BigCopy(root)
    root.mainloop()
    
if __name__ == "__main__": main()
