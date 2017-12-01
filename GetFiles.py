import urllib2
import urllib

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
