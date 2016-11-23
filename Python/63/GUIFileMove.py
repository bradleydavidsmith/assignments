##############################################
# Title: Copy *.txt Files
#
# Written for: Python 2.7.9
#
# Purpose: To copy all the *.txt files
# from 'Folder A' to 'Folder B' at
# the press of a button.
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
# 4) When things don't work, find ways to
#    correct it, don't just disable the
#    button.
# 5) Pretty up the UI. Style it up, instead
#    of using the default sizes.
#
##############################################

from Tkinter import *
import ttk, os, shutil, time

class BigCopy:

    def __init__(self, root):
    
        root.title('The Big Text File Copy')

        # Define the button
        self.b = Button(root, text="Copy", command=self.copyThem)
        self.b.pack()

        # Create the frame to hold the text box and scroll bar
        self.frame = Frame(root, bd=2, relief=SUNKEN)

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        #self.xscrollbar = Scrollbar(self.frame, orient=HORIZONTAL)
        #self.xscrollbar.grid(row=1, column=0, sticky=E+W)

        self.yscrollbar = Scrollbar(self.frame)
        self.yscrollbar.grid(row=0, column=1, sticky=N+S)

        self.text = Text(self.frame, wrap=WORD, bd=0,
        #            xscrollcommand=self.xscrollbar.set) ,
                    yscrollcommand=self.yscrollbar.set,
                    state = DISABLED)


        # Test Code:
        #self.text.config(state = NORMAL)
        #self.text.insert(END, test)
        #self.text.config(state = DISABLED)

        self.text.grid(row=0, column=0, sticky=N+S+E+W)

        #xscrollbar.config(command=self.text.xview)
        self.yscrollbar.config(command=self.text.yview)

        self.frame.pack()

        ## INITIAL CHECKS BEFORE THE mainloop()

        # make the 2 folder names
        self.desktopFolder = os.path.join(os.path.expanduser("~"), "Desktop")
        self.src = self.desktopFolder + "\\Folder A"
        self.dst = self.desktopFolder + "\\Folder B"

        # Make sure the 2 folders exist
        if not os.path.isdir(self.src):
            self.text.config(state = NORMAL)
            self.text.insert(END, "Folder '" + self.src + "' doesn't exist.")
            self.text.config(state = DISABLED)
            # Disable the app
            self.b.config(state = DISABLED)


        if not os.path.isdir(self.dst):
            # Create the destination folder
            os.mkdir(self.dst)

    # The copyThen method for button 'b' does all the work of copying the files:
    def copyThem(self):
        #print "in copyThem"
        # Move and count all the .txt files
        txtcount = 0

        # Make it so you can write to the text box
        self.text.config(state = NORMAL)
        
        for file in os.listdir(self.src):
            if file.endswith(".txt"):
                fullFileName = os.path.join(self.src, file)
                
                #print "Moving", fullFileName, "to", dst
                self.text.insert(END, "Moving '" + fullFileName + "' to '" + self.dst + "'.\n")
                self.text.see(END)
                
                # Call this so text would be displayed as it is written,
                # Insead of all at the end:
                self.frame.update_idletasks()
                time.sleep(0.2)

                # move the file
                shutil.move(fullFileName, self.dst)
                txtcount += 1

        #print
        #print "Number of *.txt files moved:", txtcount
        self.text.insert(END, "\nNumber of *.txt files moved: " + str(txtcount) + "\n")
        self.text.see(END)

        # Make the textbox read-only again
        self.text.config(state = DISABLED)
        
        # Finished, disable the app by disabling the button
        self.b.config(state = DISABLED)

def main():            
    
    root = Tk()
    feedback = BigCopy(root)
    root.mainloop()
    
if __name__ == "__main__": main()
