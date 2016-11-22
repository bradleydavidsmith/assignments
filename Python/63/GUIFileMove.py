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
# 1) Clean up the code
# 2) Make it an object
# 3) When things don't work, find ways to
#    correct it, don't just disable the
#    button.
#
##############################################

from Tkinter import *
import ttk, os, shutil, time

root = Tk()
root.title('The Big Text File Copy')

# The callback routine for button 'b' does all the work:
def callback():
    # Move and count all the .txt files
    txtcount = 0
    text.config(state = NORMAL)
    for file in os.listdir(src):
        if file.endswith(".txt"):
            fullFileName = os.path.join(src, file)
            
            #print "Moving", fullFileName, "to", dst
            text.insert(END, "Moving" + fullFileName + " to " + dst + "\n")
            text.see(END)
            
            # So text would be inserted as it is written,
            # Insead of all at the end:
            root.update_idletasks()
            time.sleep(0.2)

            shutil.move(fullFileName, dst)
            txtcount += 1

    #print
    #print "Number of *.txt files moved:", txtcount
    text.insert(END, "\nNumber of *.txt files moved: " + str(txtcount) + "\n")
    text.see(END)
    text.config(state = DISABLED)
    # Finished, disable the app
    b.config(state = DISABLED)

# Define the button
b = Button(root, text="Copy", command=callback)
b.pack()

# Create the frame to hold the text box and scroll bar
frame = Frame(root, bd=2, relief=SUNKEN)

frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

#xscrollbar = Scrollbar(frame, orient=HORIZONTAL)
#xscrollbar.grid(row=1, column=0, sticky=E+W)

yscrollbar = Scrollbar(frame)
yscrollbar.grid(row=0, column=1, sticky=N+S)

text = Text(frame, wrap=WORD, bd=0,
#            xscrollcommand=xscrollbar.set) ,
            yscrollcommand=yscrollbar.set)

# Test Code:
#text.config(state = NORMAL)
#text.insert(END, test)
#text.config(state = DISABLED)

text.grid(row=0, column=0, sticky=N+S+E+W)

#xscrollbar.config(command=text.xview)
yscrollbar.config(command=text.yview)

frame.pack()

## INITIAL CHECKS BEFORE THE mainloop()

# make the 2 folder names
src = ".\Folder A"
dst = ".\Folder B"

# Make sure the 2 folders exist
if not os.path.isdir(src):
    text.config(state = NORMAL)
    text.insert(END, "Folder " + src + " doesn't exist.")
    text.config(state = DISABLED)
    # Disable the app
    b.config(state = DISABLED)


if not os.path.isdir(dst):
    # Create the destination folder
    os.mkdir(dst)

mainloop()
