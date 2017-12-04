from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

mydata = open("part-00000","r")
mydata = mydata.readlines()

print(len(mydata))

#m = Basemap(llcrnrlon=-10.5,llcrnrlat=49.5,urcrnrlon=3.5,urcrnrlat=59.5,
#            resolution='i',projection='cass',lon_0=-4.36,lat_0=54.7)

m = Basemap()

m.drawcoastlines()
m.fillcontinents(color='coral',lake_color='aqua')

# draw parallels and meridians.
m.drawparallels(np.arange(-40,61.,2.))
m.drawmeridians(np.arange(-20.,21.,2.))
m.drawmapboundary(fill_color='aqua')

for i in range(0,100):
 data = mydata[i]
 data = data.split("\t")
 lon = data[0]
 lat = data[1]
 print(lon)
 x,y = m(lon,lat)
 m.plot(x,y,'bo',markersize=24)

plt.title("Cassini Projection")
plt.savefig("Mymap.jpg")
