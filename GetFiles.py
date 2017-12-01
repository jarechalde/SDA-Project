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

for url in dataurls:
 names = url.split("/")
 filename = names[4]
 year = filename[0:4]
 month = filename[4:6]
 day = filename[6:8]
 #print(year,month,day)

 #print(filename)
 
 #Due to size limitations in Googles instances we will only use 2016 and 2017 data
 yearlist = ["2016","2017"]
 if year not in yearlist:
  print("Passing")
  continue  	
 
 #Creating the file directories
 if not os.path.exists('Files'):
  os.makedirs('Files')

 if not os.path.exists('Files/' + year):
  os.makedirs('Files/' +  year)

 if not os.path.exists('Files/'+year+"/"+month):
  os.makedirs("Files/"+year+"/"+month)

 if not os.path.exists('Files/'+year+"/"+month+"/"+day):
  os.makedirs("Files/"+year+"/"+month+"/"+day)
 
 #Downloading file in the corresponding directory
 urllib.urlretrieve(url,"Files/"+year+"/"+month+"/"+day+"/"+filename)

 #Unzipping the file
 os.system("unzip "+"'Files/"+year+"/"+month+"/"+day+"/"+filename+"'"+" -d"+" Files/"+year+"/"+month+"/"+day+"/")

 #Deleting the zip file
 os.system("rm "+"'Files/"+year+"/"+month+"/"+day+"/"+filename+"'")

