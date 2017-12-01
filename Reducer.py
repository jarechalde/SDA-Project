#!/usr/bin/env python

from operator import itemgetter
import sys

current_lat = None
current_long = None
current_emotion = 0
lat,long = None

#Input comes from STDIN
for line in sys.stdin:
 
 #Removing whitespace
 line = line.strip()

 lat,long,emot = line.split('\t')

 #This section of the code works because Hadoop sorts map output
 if current_lat==lat and current_long==long:
  current_emotion+=emot
 else:
  if current_lat and current_long:
   #Writing the results to STDOUT
   print("%f\t%f\t%f" % (current_lat,current_long,emot))
   current_lat = lat
   current_long = long
   current_emot = emot

 #Printing the last coordinates
 if current_lat==lat and current_long==long:
  print("%f\t%f\t%f" % (current_lat,current_long,emot))


