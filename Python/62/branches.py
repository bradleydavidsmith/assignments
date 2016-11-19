##############################################
# Title: Branch locations
#
# Written for: Python 2.7.9
#
#
# Purpose: To find the local time of the
#     Portland, NYC and London branches
#     and determine if they are open or closed.
#
#
# Author: Brad Smith
#
# NOTE: The assignment said to take the
#       Time of Portland HQ, and change
#       it to the timezone of both
#       NYC and London. However, the
#       documentation for the ptzy module
#       notes issues with using
#       local time and recommends
#       using UTC, and converting from
#       UTC to the local time zone.
#       http://pytz.sourceforge.net/#problems-with-localtime
#
#
# NOTE2: Used pytz.normalize in place of
#        datetime.astimezone because
#        pytz.normalize automatically
#        accounts for Daylight Savings Time.
#
#
# METHOD and MODULES USED:
# Used the pygeocode module to take a street
# address string, like 'Portland, OR' and
# return it's latitude and longitude.
#
# Used the tzwhere module to take the
# latitude and longitude from above and
# return the time zone string.
#
# Used pytz to take the timezone string
# and localize UTC to the local time.
# pytz.normalize() accounts for daylight
# savings time.
#
# FUTURE ENHANCEMENTS:
# 1) Instead of hard-coding the business
# locations, open the company database and
# retrieve the street address, opening time
# and closing time for the company locations.
#
# 2) Create a wrapper object for the location
# routines. The object will initialize with
# a location, or even and street address string
# like 'Portland, OR' or London, England and
# and have methods like:
#
# coordinates (returns latitude/longitude)
# current local time
# if it's in daylight savings time
# The time zone
# The time zone string
#
# Also comparison methods:
# is_north (if location A is north of location B)
# in_same_time_zone
# distance between
# etc.
#
##############################################

import datetime
import pytz
from datetime import datetime, timedelta
from pygeocoder import Geocoder
from tzwhere import tzwhere

# List of office locations:
locList = ['Portland, OR', 'New York, NY', 'London, England']

# Set the local office opening and closing times
opening = '9:00 AM'
closing = '9:00 PM'
fmt = '%I:%M %p'

o = datetime.strptime(opening, fmt)
c = datetime.strptime(closing, fmt)

# Determines if a time(now) is between 2 times (start and end)
def in_between(now, start, end):
    if start <= end:
        return start <= now < end
    else:
        return start <= now or now < end

# Not used here, but could be useful in the future
# usage is_dst("America/Los_Angeles")
def is_dst(zonename):
    tz = pytz.timezone(zonename)
    now = pytz.utc.localize(datetime.utcnow())
    return now.astimezone(tz).dst() != timedelta(0)

# Current universal time (will localize to local time zone below)
utc_dt = pytz.utc.localize(datetime.utcnow())

# Start the report
print "Offices are open between", opening, "and", closing, "local time."
print

for loc in locList:
    # Find the longitude and latitude of the office location:
    try:
        longLat = Geocoder.geocode(loc).coordinates
    except:
        # The above statement can fail because:
        # 1. The Location name (loc) is misspelled
        # 2. The internet connection is not available
        # 3. The API that the Geocoder is relying on is not working
        print "Could not find Longitude/Latitude for", loc
        continue

    # Find the Time Zone string for the longitude and latitude.
    # The Time Zone string is used by pytz
    try:
        timeZone = tzwhere.tzwhere().tzNameAt(*longLat)
    except:
        # The above statement can fail because:
        # 1. The internet connection is not available
        # 2. The API that the tzwhere is relying on is not working
        print "Could not find Time Zone for", loc, "at longitude/latitude:", longLat
        continue        

    # Set the local time zone
    l_tz = pytz.timezone(timeZone)

    # Set the local time (normalize() accounts for daylight savings time)
    l_time = l_tz.normalize(utc_dt)

    # Is the local office open?
    isOpen = "open" if in_between(l_time.time(), o.time(), c.time()) else "closed"

    # Report location status
    print "The current time in", loc, "is", l_time.strftime(fmt), "and this office is currently", isOpen + "."

