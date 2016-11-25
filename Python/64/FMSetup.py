#!/usr/bin/python2
##########################################
# A Test settup program
#
# This program sets up the souce folder
# for testing the Copy by date script.
#
# Be sure to have 50+ text files in
# the source directory, so you have
# plenty of files both less than
# 24 hours old, and greater than 24
# hours old.
#
##########################################

import os, shutil, sys, datetime, time, win32file, win32con

def setModificationDate(file, date):
    # Set last modified time and accessed time to rtime
    utime = time.mktime(date.timetuple()) # change the date to a timestamp int
    os.utime(fullFileName, (utime, utime)) # modify the times

def setCreationDate(file, date):
    # This only works in WIN32
    handle = win32file.CreateFile(file,
                               win32con.GENERIC_WRITE,
                               0, None, win32con.OPEN_EXISTING, 0, None)
    win32file.SetFileTime(handle, date, None, None)
    

# make the 2 folder names
desktopFolder = os.path.join(os.path.expanduser("~"), "Desktop")
src = desktopFolder+"\\Folder A"

# set recent time to 45 minutes ago:
now = datetime.datetime.now()
rtime = now- datetime.timedelta(minutes=45)

# Go through the text files in the source file and change their
# last-modified dates

fileCount = 0
for file in os.listdir(src):
    if file.endswith(".txt"):

        fullFileName = os.path.join(src, file)

        if fileCount % 2 == 0: # Count Odd, make creation date more than 24 hours old
            creDelta = datetime.timedelta(hours=-24)
        else:
            if (now - rtime) < datetime.timedelta(hours=24): # creDate before mod date
                creDelta = datetime.timedelta(minutes=10)
            else:
                creDelta = datetime.timedelta(hours = 24)
                
        # Set last modified time and accessed time to rtime
        setModificationDate(fullFileName, rtime)

        setCreationDate(fullFileName, rtime + creDelta) 
        
        # Subtract 60 minutes from rtime
        # (So some of the files were last modified less than 24
        # hours old, and some were modified more than 24)
        rtime -= datetime.timedelta(minutes=60)
        fileCount += 1
        




