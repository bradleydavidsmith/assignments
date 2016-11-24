#!/usr/bin/python2
import os, shutil, sys, datetime

# make the 2 folder names
desktopFolder = os.path.join(os.path.expanduser("~"), "Desktop")
src = desktopFolder+"\\Folder A"
dst = desktopFolder+"\\Folder B"

# Make sure the 2 folders exist
if not os.path.isdir(src):
    print "Folder", src, "doesn't exist"
    sys.exit()

if not os.path.isdir(dst):
    # Create the destination folder
    os.mkdir(dst)


# Move all the files that have been modified in the
# last 24 hours. 
T24HoursAgo = datetime.datetime.now() - datetime.timedelta(hours = 24)
txtcount = 0

for file in os.listdir(src):
    if file.endswith(".txt"):


        fullFileName = os.path.join(src, file)
        modTS = os.path.getmtime(fullFileName)
        modDate = datetime.datetime.fromtimestamp(modTS)
        mDateStr = modDate.strftime('%Y-%m-%d %H:%M:%S')

        # Copy if modified in the last 24 hours
        if modDate > T24HoursAgo:   
            print file, "last modified", mDateStr, \
            "So copying to", dst
            shutil.copy2(fullFileName, dst)
            txtcount += 1
        else:
            print file, "last modified", mDateStr, \
            "So not copied..."
            
print
print "Number of *.txt files copied:", txtcount

