#!/usr/bin/env python

#import pyspark
import os,logging
#from pyspark.sql.functions import *
import sys

#Starting the logger
logging.basicConfig(filename="Mapper.log", level=logging.INFO)

for line in sys.stdin:

 line = line.split("\t")

 #Initializing the list that will contain lat,long, and emotion
 listlatlongem = []
  
 try:
  #Locations
  loc = line[1]
 
  #Emotions for this locations
  emot = line[2]

 except:
  logging.info("Input error")
  continue

 #If there are no locations in this row, we are not interested into this row, so we skip it:
 if loc==None:
  logging.info("NO LOCATION DATA")
  continue

 #If there are locations in this row, we continue saving the place
 #Locations in the same row are separated by ;
 locations = loc.split(";")

 #We get the emotion for this locations
 #Emotions are separated by a simple comma
 emotions = emot.split(",")

 try:
  emotion = emotions[0]
 except:
  continue
  logging.info("No emotions data")

 #Now for every location in locations we will save it
 #Locatioon 0 was empty for some reason so we start in 1 instead
 for i in range(1,len(locations)):
  location = locations[i]

  #Locations are divided by #, and the latitude and longitude are in the 5th and 6th position respectivelu
  locatt = location.split("#")
  try:
   lat = locatt[5]
   long = locatt[6]
  except:
   logging.info("No location data")

  #If we cannot convert the float due to a erroneous lat or long we skip this iteration
  try:
   latlongemot = (float(lat),float(long),float(emotion))
  except:
   logging.error("MISSING DATA")
   continue

  print("%f\t%f\t%f" % (latlongemot[0],latlongemot[1],latlongemot[2]))
