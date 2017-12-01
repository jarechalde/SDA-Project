import pyspark
import os
from pyspark.sql.functions import *
import csv

#Loading the packages befores creating the context
#os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages com.databricks:spark-xml:0.4.1 pyspark-shell'

#Initializing the spark context
#sc = pyspark.SparkContext.getOrCreate()
#sc.setLogLevel("OFF")

#Initialize the SQL context
#sql = pyspark.SQLContext(sc)

#Lets load a sample of the data
#mydata = sql.read.format("csv").options(delimiter="\t").load("./Files/2016/01/01/20160101160000.gkg.csv")

mydata = csv.reader("./Files/2016/01/01/20160101160000.gkg.csv", delimiter='\t')

#Renaming the columns
mydata = mydata.toDF("GKGRECORDID",
          "V2.1 DATE",
          "V2SOURCECOLLECTIONIDENTIFIER",
          "V2SOURCECOMMONNAME",
          "V2DOCUMENTIDENTIFIER",
          "V1COUNTS",
          "V2.1COUNTS",
          "V1THEMES",
          "V2ENHANCEDTHEMES",
          "V1LOCATIONS",
          "V2ENHANCEDLOCATIONS",
          "V1PERSONS",
          "V2ENHANCEDPERSONS",
          "V1ORGANIZATIONS",
          "V2ENHANCEDORGANIZATIONS",
          "V1.5TONE",
          "V2.1ENHANCEDDATES",
          "V2GCAM",
          "V2.1SHARINGIMAGE",
          "V2.1RELATEDIMAGES",
          "V2.1SOCIALIMAGEEMBEDS",
          "V2.1SOCIALVIDEOEMBEDS",
          "V2.1QUOTATIONS",
          "V2.1ALLNAMES",
          "V2.1AMOUNTS",
          "V2.1TRANSLATIONINFO",
          "V2EXTRASXML")

#Number of rows we have
nrows = mydata.count()
print("Number of rows: ",nrows)

#Collect data so we can treat it as a list
mydata = mydata.collect()

#Initializing the list that will contain lat,long, and emotion
listlatlongem = []

for i in range(1,nrows):
 #Locations
 loc = mydata[i]["V2ENHANCEDLOCATIONS"]
 
 #Emotions for this locations
 emot = mydata[i]["V1.5TONE"]

 #If there are no locations in this row, we are not interested into this row, so we skip it:
 if loc==None:
  #print("NO LOCATION DATA")
  continue

 #If there are locations in this row, we continue saving the place
 #Locations in the same row are separated by ;
 locations = loc.split(";")

 #We get the emotion for this locations
 #Emotions are separated by a simple comma
 emotions = emot.split(",")
 emotion = emotions[0]

 #Now for every location in locations we will save it
 for location in locations:
  
  #Locations are divided by #, and the latitude and longitude are in the 5th and 6th position respectivelu
  locatt = location.split("#")
  lat = locatt[5]
  long = locatt[6]

  #If we cannot convert the float due to a erroneous lat or long we skip this iteration
  try:
   latlongemot = (float(lat),float(long),float(emotion))
  except:
   #print("ERROR: MISSING DATA")
   #print(lat,long,emotion)
   continue

  #print("%f\t%f\t%f" % (latlongemot[0],latlongemot[1],latlongemot[2]))
