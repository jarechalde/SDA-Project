from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math
from matplotlib import colors

#Number of bins for our plot

mydata = open("/home/javier/Work/SDA-Project/Results/results1/part-00000","r")
mydata = mydata.readlines()

#We will use a Cylindrical projection with a intermediate resolution, and we will only show lakes with
#an area greater than 10000m^2
map = Basemap(projection ='cyl', resolution = 'i', area_thresh = 10000)

x = []
y = []
c = []
d = []

#Figure
for i in range(0,len(mydata)):
 data = mydata[i]
 data = data.split("\t")

 #First lets work with the tone
 tone = float(data[2])
 
 #Usually the tone stays in between -10 and 10 values, so if the tone is smaller or greater than
 #this amount we will set it to either one of those
 
 if tone<-10:
  tone = -10

 if tone>10:
  tone = 10

 count = float(data[3])
 lat,lon = map(float(data[0]),float(data[1]))
 x.append(lon)
 y.append(lat)
 c.append(tone)
 d.append(count)

#Transforming into numpy array our lists
x = np.array(x)
y = np.array(y)
c = np.array(c)
d = np.array(d)

fig = plt.figure()
fig.suptitle("News Tone and Number of References", fontsize = 20)

###First Plot###

#Adding hexbin map
ax = fig.add_subplot(211)
map.hexbin(x,y, C = c, vmax = 10, vmin = -10)

#Adding bar at the bottom
colbar = map.colorbar(location = 'right')
colbar.set_label('Tone')

#Drawing state and coast lines
map.drawcountries(linewidth=0.5, linestyle='solid', color='k')
map.drawcoastlines(linewidth = 1)

#Plot title
plt.title("TONE")

###Second Plot###

#Heatmap for the second plot
cmap = colors.ListedColormap(['#ffcccc','#ff8080','#ff3333','#cc0000','#4d0000'])
bounds=[1, 10, 100, 1000, 1000]
norm = colors.BoundaryNorm(bounds, cmap.N)

#Adding hexbin for number times that location was referenced in the news
ax = fig.add_subplot(212)
map.hexbin(x,y, C = d, cmap = cmap, norm = norm)

#Adding color bar at the bottom
colbar2 = map.colorbar(location= 'right')
colbar2.set_label('Number of references')

#Drawing state lines and coast lines
map.drawcountries(linewidth=0.5, linestyle='solid', color='k')
map.drawcoastlines(linewidth = 1)

#Plot title
plt.title("REFERENCES")

#Showing the plot
plt.show()
