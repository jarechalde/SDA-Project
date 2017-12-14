#We will get the files and then run the mapreduce jobimport urllib2
import urllib2
import urllib
import os
import csv

#First we get the file that contains all the urls for the files that we are going to use in this project
files  = urllib2.urlopen('http://data.gdeltproject.org/gdeltv2/masterfilelist.txt')
web = files.read()

#Creating a file to save the urls
myfile = open("myfiles.txt","w")
myfile.write(web)
myfile.close()

#Open the file in read mode
urls = open("myfiles.txt","r")
urlslist = urls.readlines()
urls.close()

#Open a file to save gkg urls
gkgurls = open("gkgfiles.txt","w")

for url in urlslist:
 url = url.split(" ")
 try:
  file = url[2]
  #If the file name doesnt contain gkg, we wont save it into the gkg urls file
  if "gkg" not in file:
   continue
  gkgurls.write(file)
 except:
  print("ERROR, url not found")

#Closing the file of gkg urls
gkgurls.close()

#Now we load the urls and download all the data
dataurls = open("gkgfiles.txt","r")
dataurls = dataurls.readlines()

def startcluster():
 #Starting hadoop cluster
 os.system("/usr/local/hadoop/sbin/start-dfs.sh")
 os.system("/usr/local/hadoop/sbin/start-yarn.sh")

#Leaving safe mode
#os.system("/usr/local/hadoop/bin/hadoop dfsadmin -safemode leave")

#Function for getting the files
def getfiles(filtery,filterm,filterd):
 
 #For each url in the gkg urls we will get the filename, year, month and day
 for i in range(1,2):
  url = dataurls[i]
  names = url.split("/")
  filename = names[4]
  year = filename[0:4]
  month = filename[4:6]
  day = filename[6:8]
  #print(year,month,day)

  print(url)
 
  print("Downloading Files")

  #Downloading each file in its corresponding directory
  urllib.urlretrieve(url,"/home/jarechalde/Work/SDA-Project/"+filename)

  #Unzipping the file

  #Getting the name of the unzipped file
  fileunzip = filename.split(".")
  fileunzip = fileunzip[0]+".gkg.csv"

  os.system("unzip "+"'/home/jarechalde/Work/SDA-Project/"+filename+"'"+" -d"+" /home/jarechalde/Work/SDA-Project/")


  fileaddress = "/home/jarechalde/Work/SDA-Project/"+fileunzip
  print(fileaddress)

  fileaddress = "/home/jarechalde/Work/SDA-Project/"+fileunzip

  filered = "/home/jarechalde/Work/SDA-Project/red"+fileunzip

  mydata = open(fileaddress,'r')
  mydatal = mydata.readlines()
  
  myrdata = open(filered,'w')

  print(fileunzip)

  for line in mydatal:
   line = line.split("\t")
   myrdata.write(line[10] + "\t" +line[15] + "\n")
   
  myrdata.close()
  mydata.close()

getfiles(1,1,1)
#mapreducejob()
#closecluster()
#cleanfiles()
#removefiles()

#We will get the files and then run the mapreduce job
