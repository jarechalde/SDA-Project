#First we start spark
import pyspark
import os
from pyspark.sql.functions import *

#Loading the packages befores creating the context
#os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages com.databricks:spark-xml:0.4.1 pyspark-shell'

#Initializing the spark context
sc = pyspark.SparkContext.getOrCreate()

#Initialize the SQL context
sql = pyspark.SQLContext(sc)

#Lets load a sample of the data
mydata = sql.read.format("csv").options(delimiter="\t").load("Files/2016/01/01/20160101160000.gkg.csv")

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

#Initializing the location list
loclists = []
allpersons = []

#Change the limit to nrows later
for i in range(1,nrows):
    #Locations
    loc = mydata[i]["V2ENHANCEDLOCATIONS"]

    #Tone goes from -100 (extremely negative) to +100 (extremely positive)
    emot = mydata[i]["V1.5TONE"]

    #Person names in the news
    persons = mydata[i]["V2ENHANCEDPERSONS"]

    #We will focus on locations, so if we dont have a location, we will skip the loop
    if loc==None:
        print("NO LOCATION DATA")
        continue

    #If the locations exist, we continue saving the place
    locations = loc.split(";")

    #Emotion tone indicators are separated by a comma
    emotions = emot.split(',')
    latlist = []

    #Person names are separated by semicolon

    #If there are no person names, we will indicate it
    if persons==None:
        persons = "No Persons"

    persons = persons.split(';')
    perslist = []
    for person in persons:
        #We get rid of the reference
        person = person.split(',')
        person = person[0]
        perslist.append(person)

    #Getting only the unique names in the person list
    perslist = list(set(perslist))

    for location in locations:
        locatt = location.split("#")
        lat = locatt[5]
        long = locatt[6]
        #If we cannot convert to float we skip to the next loop execution
        try:
            latlong = (float(lat),float(long))
        except:
            continue
        latlist.append(latlong,emotions[0])

    #We should save in the third part of the list the number of times same location appeared to set a circle size in the map

    #Adding the locartion
    loclists.append(latlist)

    #We add the emotion of this event to the emotions array
    emotlist.append(emotions[0])

    #Add the persons of this event to the persons array
    allpersons.append(perslist)
