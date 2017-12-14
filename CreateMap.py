from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

mydata = open("/home/hduser/Work/SDA-Project/Results/part-00000","r")
mydata = mydata.readlines()

print(len(mydata))

#m = Basemap(llcrnrlon=-10.5,llcrnrlat=49.5,urcrnrlon=3.5,urcrnrlat=59.5,
#            resolution='i',projection='cass',lon_0=-4.36,lat_0=54.7)

map = Basemap(projection='ortho', lat_0=0, lon_0=0)

#m.drawcoastlines()
map.fillcontinents(color='coral',lake_color='aqua')

# draw parallels and meridians.
#m.drawparallels(np.arange(-40,61.,2.))
#m.drawmeridians(np.arange(-20.,21.,2.))
map.drawmapboundary(fill_color='aqua')

for i in range(0,len(mydata)):
 data = mydata[i]
 data = data.split("\t")
 print(data[0],data[1])
 lon = float(data[0])
 lat = float(data[1])
 x,y = map(lon,lat)
 map.plot(x,y,marker = 'D', color = 'm')

plt.show()
plt.savefig("Mymap.jpg")
