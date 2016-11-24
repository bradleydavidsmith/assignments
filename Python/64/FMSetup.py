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

import os, shutil, sys, datetime, time


# make the 2 folder names
desktopFolder = os.path.join(os.path.expanduser("~"), "Desktop")
src = desktopFolder+"\\Folder A"


# set recent time to 30 minutes ago:
rtime = datetime.datetime.now()- datetime.timedelta(minutes=30)

# Go through the text files in the source file and change their
# last-modified dates
for file in os.listdir(src):
    if file.endswith(".txt"):
        fullFileName = os.path.join(src, file)

        # Set last modified time and accessed time to rtime
        utime = time.mktime(rtime.timetuple()) # change the date to an int
        os.utime(fullFileName, (utime, utime)) # modify the times

        # Subtract 60 minutes from rtime
        # (So some of the files are less than 24
        # hours old, and some are more than 24)
        rtime -= datetime.timedelta(minutes=60)
        




