import urllib2
import urllib
import os

files  = urllib2.urlopen('http://data.gdeltproject.org/gdeltv2/masterfilelist.txt')
web = files.read()

#Creating a file with the urls
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
  if "gkg" not in file:
   continue
  gkgurls.write(file)
 except:
  print("ERROR")

#Closing the file of gkg urls
gkgurls.close()

#Now we load the urls and download all the data
dataurls = open("gkgfiles.txt","r")
dataurls = dataurls.readlines()

#We can add a progressbar later

#Starting hadoop cluster
os.system("/usr/local/hadoop/sbin/start-dfs.sh")
os.system("/usr/local/hadoop/sbin/start-yarn.sh")
#Leaving safe mpode
os.system("/usr/local/hadoop/bin/hadoop dfsadmin -safemode leave")


def getfiles():

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
  if year not in yearlist:
   #print("Passing")
   continue  	
 
  monthlist = ["01"]
  if month not in monthlist:
   #print("Passing")
   continue

  daylist = ["01"]
  if day not in daylist:
   #print("Passing")
   continue

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
 
  #Downloading file in the corresponding directory
  urllib.urlretrieve(url,"/usr/local/hadoop/tmp/Files/"+year+"/"+month+"/"+day+"/"+filename)

  #Unzipping the file
  os.system("unzip "+"'/usr/local/hadoop/tmp/Files/"+year+"/"+month+"/"+day+"/"+filename+"'"+" -d"+" /usr/local/hadoop/tmp/Files/"+year+"/"+month+"/"+day+"/")

  #Deleting the zip file
  os.system("rm "+"'/usr/local/hadoop/tmp/Files/"+year+"/"+month+"/"+day+"/"+filename+"'")

  #Getting the name of the unzipped file
  fileunzip = filename.split(".")
  fileunzip = fileunzip[0]+".gkg.csv"
 
  #Copying the file into hadoop file system
  os.system("hdfs dfs -mkdir -p /home/hduser/Files/"+year+"/"+month+"/"+day)
  os.system("hdfs dfs -copyFromLocal "+"/usr/local/hadoop/tmp/Files/"+year+"/"+month+"/"+day+"/"+fileunzip+" /home/hduser/Files/"+year+"/"+month+"/"+day+"/"+fileunzip)

  #Deleting the file after copying into hadoop file system 
  os.system("rm "+"'/usr/local/hadoop/tmp/Files/"+year+"/"+month+"/"+day+"/"+fileunzip+"'")


#getfiles()

def mapreducejob():

 #Leave safe mode before running the mapreduce jib
 os.system("/usr/local/hadoop/bin/hadoop dfsadmin -safemode leave")

 command = "hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.9.0.jar "
 command += "-file /home/hduser/Work/SDA-Project/MapHadoop.py "
 command += "-mapper /home/hduser/Work/SDA-Project/MapHadoop.py "
 command += "-file /home/hduser/Work/SDA-Project/ReducerHadoop.py "
 command += "-reducer /home/hduser/Work/SDA-Project/ReducerHadoop.py " 
 command += "-input /home/hduser/Files/2016/01/01/* "
 command += "-output /home/hduser/Hadoop/hadoop-output"

 #Getting files
 #getfiles()

 os.system(command)

 #Now lets copy the files from the hdfs into our local system
 os.system("hdfs dfs -get /home/hduser/Hadoop/hadoop-output/* /home/hduser/Results")

 #Removing the results from hdfs
 os.system("hdfs dfs -rm -r /home/hduser/Hadoop/hadoop-output/")

 #Removing temporaty filed
 os.system("sudo rm -r /app/hadoop/tmp")
 os.system("sudo mkdir -p /app/hadoop/tmp")
 os.system("sudo chown hduser:hadoop /app/hadoop/tmp")
 os.system("sudo chmod 750 /app/hadoop/tmp")


#Closing the clsuter
#os.system("/usr/local/hadoop/sbin/stop-dfs.sh")
#os.system("/usr/local/hadoop/sbin/stop-yarn.sh")
