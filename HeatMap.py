from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

#Number of bins for our plot

mydata = open("/home/javier/Work/SDA-Project/Results/part-00000","r")
mydata = mydata.readlines()

#We will use a Cylindrical projection with a low resolution
map = Basemap(projection ='cyl', resolution = 'i', area_thresh = 10000)

x = []
y = []
c = []
d = []

#Figure
for i in range(0,len(mydata)):
 data = mydata[i]
 data = data.split("\t")
 print(data[0],data[1],data[2])
 lat,lon = map(float(data[0]),float(data[1]))
 x.append(lon)
 y.append(lat)
 c.append(float(data[2]))
 d.append(float(data[3]))

#Transforming into numpy array our lists
x = np.array(x)
y = np.array(y)
c = np.array(c)
d = np.array(d)

fig = plt.figure()
fig.suptitle("News Analysis 01/01/2016", fontsize = 20)

###First Plot###

#Adding hexbin map
ax = fig.add_subplot(211)
map.hexbin(x,y, C = c)

#Adding bar at the bottom
colbar = map.colorbar(location = 'right')
colbar.set_label('Tone')

#Drawing state and coast lines
map.drawcountries(linewidth=0.5, linestyle='solid', color='k')
map.drawcoastlines(linewidth = 1)

#Plot title
plt.title("Tone of the News")

###Second Plot###

#Adding hexbin for number times that location was referenced in the news
ax = fig.add_subplot(212)
map.hexbin(x,y, C = d)

#Adding color bar at the bottom
colbar2 = map.colorbar(location= 'right')
colbar2.set_label('Number of references')

#Drawing state lines and coast lines
map.drawcountries(linewidth=0.5, linestyle='solid', color='k')
map.drawcoastlines(linewidth = 1)

#Plot title
plt.title("Number of references in the News")

#Showing the plot
plt.show()
plt.savefig("Mymap.jpg")
