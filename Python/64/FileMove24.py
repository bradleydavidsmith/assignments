#################################################################
#
# File Copy
#
# DESCRIPTION:
#    Copies all the files from a directory to another if
#    the file was modified in the last 24 hours
#
# WRITTEN FOR: Python 2.7.9
#
# WRITTEN BY: Brad Smith
#
# FUTURE ENHANCEMENTS:
#    1) This program's purpose is to do a backup of the directory.
#       Instead of counting on it being run every 24 hours, have
#       the program keep a database of backed up files, and only
#       back up files that changed in the last 24 hours.
#
#    2) Have the program back up the entire directory structure
#       instead of just a single directory
##################################################################


#!/usr/bin/python2
import os, shutil, sys, datetime

def getModificationDate(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

def getCreationDate(filename):
    t = os.path.getctime(filename)
    return datetime.datetime.fromtimestamp(t)

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
        modDate = getModificationDate(fullFileName)
        mDateStr = modDate.strftime('%Y-%m-%d %H:%M:%S')
        creDate = getCreationDate(fullFileName)
        cDateStr = creDate.strftime('%Y-%m-%d %H:%M:%S')

        # Copy if modified or created in the last 24 hours
        if modDate > T24HoursAgo:   
            print file, "last modified", mDateStr, \
            "so copying to", dst
            shutil.copy2(fullFileName, dst)
            txtcount += 1
        elif creDate > T24HoursAgo:   
            print file, "was created", cDateStr, \
            "so copying to", dst
            shutil.copy2(fullFileName, dst)
            txtcount += 1
        else:
            print file, "was created", cDateStr, "and last modified", mDateStr, \
            "so not copied..."
            
print
print "Number of *.txt files copied:", txtcount

