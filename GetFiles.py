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

print(dataurls[0])
urllib.urlretrieve(dataurls[0],"myfile.zip")
#We can add a progressbar later

for url in dataurls:
 #print(url)
 names = url.split("/")
 filename = names[4]
 year = filename[0:4]
 month = filename[4:6]
 day = filename[6:8]
 print(year,month,day)
  
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

