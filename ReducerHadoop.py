#!/usr/bin/env python

from operator import itemgetter
import sys

current_lat = None
current_long = None
current_emotion = 0
lat = None
long = None
current_count = 1

#Input comes from STDIN
for line in sys.stdin:

 #Removing whitespace
 line = line.strip()

 lat,long,emot = line.split('\t')

 #Converting to numbers
 try:
  lat = float(lat) 
  long = float(long)
  emot = float(emot)

 #If we cannot convert them skip to the next iteration
 except:
  continue

 #print(lat,long,emot)

 #This section of the code works because Hadoop sorts map output
 if current_lat==lat and current_long==long:
  current_emot+=emot
  current_count=current_count+1
 else:
  if current_lat and current_long:
   #Writing the results to STDOUT
   #Calculating the mean first
   current_emot = current_emot/current_count
   print("%f\t%f\t%f\t%i" % (current_lat,current_long,current_emot,current_count))
 
  #Updating the values  
  current_lat = lat
  current_long = long
  current_emot = emot
  current_count = 1

#Printing the last coordinates
if current_lat==lat and current_long==long:
 print("%f\t%f\t%f" % (current_lat,current_long,current_emot,current_count))
