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
 for url in dataurls:
  names = url.split("/")
  filename = names[4]
  year = filename[0:4]
  month = filename[4:6]
  day = filename[6:8]
  #print(year,month,day)

  #print(filename)
 
  #Due to size limitations in Googles instances we will only use 2016 and 2017 data
  yearlist = ["2016"]
  if filtery == 1:
   if year not in yearlist:
    continue  	
 
  monthlist = ["01"] 
  if filterm == 1: 
   if month not in monthlist:
    continue

  daylist = ["01"]
  if filterd == 1:
   if day not in daylist:
    continue

  #Removing the temporary files before downloading our files
  try:
   os.system("rm -rf /usr/local/hadoop/tmp/Files")
  except:
   print("Directory doesn't exist")

  #Creating the file directories
  if not os.path.exists('/usr/local/hadoop/tmp/Files'):
   os.makedirs('/usr/local/hadoop/tmp/Files')

  if not os.path.exists('/usr/local/hadoop/tmp/Files/' + year):
   os.makedirs('/usr/local/hadoop/tmp/Files/' +  year)

  if not os.path.exists('/usr/local/hadoop/tmp/Files/'+year+"/"+month):
   os.makedirs("/usr/local/hadoop/tmp/Files/"+year+"/"+month)

  if not os.path.exists('/usr/local/hadoop/tmp/Files/'+year+"/"+month+"/"+day):
   os.makedirs("/usr/local/hadoop/tmp/Files/"+year+"/"+month+"/"+day)
 
  #Downloading each file in its corresponding directory
  urllib.urlretrieve(url,"/usr/local/hadoop/tmp/Files/"+year+"/"+month+"/"+day+"/"+filename)

  #Unzipping the file
  os.system("unzip "+"'/usr/local/hadoop/tmp/Files/"+year+"/"+month+"/"+day+"/"+filename+"'"+" -d"+" /usr/local/hadoop/tmp/Files/"+year+"/"+month+"/"+day+"/")

  #Deleting the zip file
  os.system("rm "+"'/usr/local/hadoop/tmp/Files/"+year+"/"+month+"/"+day+"/"+filename+"'")

  #Getting the name of the unzipped file
  fileunzip = filename.split(".")
  fileunzip = fileunzip[0]+".gkg.csv"
 
  #Reducing the file before transferring it to hadoop file system
  addressdata = "/usr/local/hadoop/tmp/Files/"+year+"/"+month+"/"+day+"/"+fileunzip
  addressdatar = "/usr/local/hadoop/tmp/Files/"+year+"/"+month+"/"+day+"/RED_"+fileunzip

  mydata = open(addressdata, 'r')
  mydatal = mydata.readlines()

  mydatar = open(addressdatar, 'a')
  for line in mydatal:
   data = line.split('\t')
   mydatar.write('{}\t{}'.format(data[10],data[15]))
  
  #Closing the files
  mydata.close()
  mydatar.close()
  

  #Copying the file into hadoop file system
  os.system("hdfs dfs -mkdir -p /home/hduser/Files/"+year+"/"+month+"/"+day)
  os.system("hdfs dfs -copyFromLocal "+"/usr/local/hadoop/tmp/Files/"+year+"/"+month+"/"+day+"/RED_"+fileunzip+" /home/hduser/Files/"+year+"/"+month+"/"+day+"/"+fileunzip)

  #Deleting the files from our local system after copying into hadoop file system 
  os.system("rm "+"'/usr/local/hadoop/tmp/Files/"+year+"/"+month+"/"+day+"/"+fileunzip+"'")
  os.system("rm "+"'/usr/local/hadoop/tmp/Files/"+year+"/"+month+"/"+day+"/RED_"+fileunzip+"'")

def mapreducejob():

 #Leave safe mode before running the mapreduce job
 os.system("/usr/local/hadoop/bin/hadoop dfsadmin -safemode leave")

 #Command for running the mapreduce job
 command = "hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.9.0.jar "
 command += "-file /home/hduser/Work/SDA-Project/MapHadoop.py "
 command += "-mapper /home/hduser/Work/SDA-Project/MapHadoop.py "
 command += "-file /home/hduser/Work/SDA-Project/ReducerHadoop.py "
 command += "-reducer /home/hduser/Work/SDA-Project/ReducerHadoop.py " 
 command += "-input /home/hduser/Files/2016/01/01/* "  

 #Skipping this for now 
 for i in range(1,30): 
  continue 
  j = str(i)   
 
  if i<10:
   command += "-input /home/hduser/Files/2016/01/0"+j+" " #This line will specify the input files for the mapreduce job
  else:
   command += "-input /home/hduser/Files/2016/01/"+j+" " 

 command += "-output /home/hduser/Hadoop/hadoop-output"

 #Running the  mapreduce job
 os.system(command)

 #Now lets copy the files from the hdfs into our local system
 os.system("hdfs dfs -get /home/hduser/Hadoop/hadoop-output/* /home/hduser/Work/SDA-Project/Results")

 #Removing the output from hdfs
 os.system("hdfs dfs -rm -r /home/hduser/Hadoop/hadoop-output/")


def cleanfiles():
 #Removing temporary files
 os.system("hdfs namenode -format")
 os.system("sudo rm -r /app/hadoop/tmp")
 os.system("sudo mkdir -p /app/hadoop/tmp")
 os.system("sudo chown hduser:hadoop /app/hadoop/tmp")
 os.system("sudo chmod 750 /app/hadoop/tmp")

def removefiles():
 os.system("hdfs dfs -rm -r /home/hduser/Files")

def closecluster():
 #Closing the cluster
 os.system("/usr/local/hadoop/sbin/stop-dfs.sh")
 os.system("/usr/local/hadoop/sbin/stop-yarn.sh")

startcluster()
#removefiles()
#getfiles(1,1,1)
mapreducejob()
#cleanfiles()
closecluster()

#We will get the files and then run the mapreduce job
