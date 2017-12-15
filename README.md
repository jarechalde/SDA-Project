# MAP REDUCE On the GDELTS GKG Dataset

The goal of this project is to run map-reduce on GDELT's Global Knowledge Graph data in a cluster set up in Google Cloud Platform. We will start by setting up the cluster, the we will download the files and transfer them to HDFS, and once the files are replicated in all the DataNodes, we will run MapReduce 2.0 or YARN over our data, using a Mapper and a Reducer function implemented in this project too. Our last step will be to plot the results using Matplotlib's Basemap Toolkit.

# Data used in this project
The data used in this project is available as a list of links to the files [here](http://data.gdeltproject.org/gdeltv2/masterfilelist.txt), our main script will download this files on our instance automatically and select the urls that we will use to download the data.

In this project, as we mentioned before, we will only use GDELT's GKG data. This data has been stored in GDELT's last format 2.1 from January 2015 until this very moment, in intervals of 15 minutes.

More information about how this data is stored is available [here](http://data.gdeltproject.org/documentation/GDELT-Global_Knowledge_Graph_Codebook-V2.1.pdf).

# Getting Started

First we will start by setting up the hadoop cluster, for this project we will create 4 instances, and configure them as it follows.

We will create on Google Cloud Platform 4 instances that will serve as master and slave nodes for our project. We created 4 instances each one of them having 1 vCore and 4 GB of RAM, and 500GB of disk each one, due to the limitation of 2TB inside a project. Ths instances will be running Ubuntu 16.04 LTS

## 1. Installing java [ALL]

First we will need to install java.

```
[1] sudo apt-get update
[2] sudo apt-get upgrade
[3] sudo apt-get install default-jre
[4] sudo apt-get install default-jdk
```

To check if Java was installed correctly we can run this command
```
[1] java -version
```
And the java version should show up in case it was successfully installed.

## 2. Installing unzip [MASTER]

Our main script will be using unzip to unzip all the incoming files, so we will need to install the unzip package on the master node. This can be done by executing this simple command.

```
[1] sudo apt-get install unzip
```

## 3. Creating Hadoop users [ALL]

Then we continue by adding a user for Hadoop in the users group, and giving this user superuser permissions, this should be done in all instances too. You can choose any password you like, it won’t affect any part of this process.

```
[1] sudo addgroup hadoop
[2] sudo adduser –-ingroup hadoop hduser
[3] sudo usermod -aG sudo hduser
```

Then we should login into the created username in all the instances.

```
[1] su – hduser
```

## 4. Giving access to the slave nodes to the master node [MASTER]

The master node should be able to access all the other nodes in the cluster without a ssh key, to run the map-reduce job, so we need to create a public key by running the first command. After running the second command, we will get the key string. The way Google instances get the ssh keys is different than in any other service. Google instances get the ssh key values from Google Cloud Platform whenever they are started, so we will need to copy the key string obtained by executing the second command to Metadata > SSH Keys on the Google Cloud Platform Computer Engine menu. Then when we connect to any of the instances, Google Cloud Platform will pass this keys to the instance and add it to the authorized keys list. If this setup was done in another service, the key value should be added manually to the authorized keys list in the other instances manually.

```
[1] ssh-keygen -t rsa -P ""
[2] cat $HOME/.ssh/id_rsa.pub
```
## 5. Configuring IP addresses of slaves and masters and disabling ipv6 [ALL]

Then we will need to add the IP addresses of the all the instances to the hosts file in all instances. We can open this file by running this command.

```
[1] sudo nano /etc/hosts
```

Then we will need to add the following lines to the file. The IP we need to use is the Internal IP that is shown in the Google Compute Engine Dashboard.

```
[IP of Master] master
[IP of slave1] slave1
[IP of slave2] slave2
...
[IP of slaveN] slaveN
```

Then we will need to disable ipv6 by adding this lines to /etc/sysct1.conf. 

```
# disable ipv6
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
```

## 6. Checking connection to the slaves [MASTER]

Now we can check if we can connect to the slave and master nodes from the master node. To check this, we must run the following commands and answer yes whenever they ask us if we want to continue connecting.

```
[1] ssh master
[2] ssh slave1
[3] ssh slave2
...
[N] ssh slaveN
```

## 7. Installing and configuring Hadoop [ALL]

Now we will proceed to install Hadoop. First, we will go to the local folder, then we will download Hadoop, then we will extract it and move it to the Hadoop folder. To get the URL, go to Hadoops Releases webpage and get the last released binary file download address, in this case 2.9.0.

```
[1] cd /usr/local
[2] wget [download_url]
[3] sudo tar xzf [file name]
[4] sudo mv [extracted folder name] hadoop
[5] sudo chown – R hduser:hadoop hadoop
```

Now we need to add Hadoop home and java home to the path

```
[1] sudo nano $HOME/.bashrc
```
Add the following lines at the end of the file.

```
export HADOOP_HOME =/usr/local/hadoop
export JAVA_HOME = /usr/lib/jvm/default-java
```

Then we configure the Hadoop environment variables.

```
[1] sudo nano /usr/local/hadoop/etc/hadoop-env.sh
```

Edit the JAVA_HOME value in the file with the java directory.

```
export JAVA_HOME = /usr/lib/jvm/default-java
```

Create a temporary folder so hadoop can store its files while we download them and transfer them to Hadoop File Hystem.
```
[1] sudo mkdir -p /app/hadoop/tmp
[2] sudo chown hduser:hadoop /app/hadoop/tmp
[3] sudo chmod 750 /app/hadoop/tmp
```
## 8. Configuring master and slaves [MASTER]

Configure the masters' and slaves' files.
Masters file.
```
[1] sudo nano /usr/local/hadoop/etc/hadoop/masters
```
Add the following line.
```
master
```
Slaves file.
```
[1] sudo nano /usr/local/hadoop/etc/hadoop/slaves
```
Add the following lines.
```
master //Yes, in this project the master node will be a slave node too
slave1
...
slaveN
```
## 9. Configuring HDFS and YARN [ALL]

Configure the site xml file in all machines
```
[1] sudo nano /usr/local/hadoop/etc/hadoop/core-site.xml
```
Add the following lines in between configuration.
```
<property>
  <name>hadoop.tmp.dir</name>
  <value>/app/hadoop/tmp</value>
</property>
<property>
  <name>fs.defaultFS</name>
  <value>hdfs://master:54310</value>
</property>
```

Configure mapred-site.xml
```
[1] sudo nano /usr/local/hadoop/etc/hadoop/mapred-site.xml
```
Add the following lines in between configuration.
```
<property>
  <name>mapreduce.framework.name</name>
  <value>yarn</value>
</property>
```

Configure hfs-site.xml. Inside value put the number of slaves, in this case 4, as the master node is also a Data Node.
```
[1] sudo nano /usr/local/hadoop/etc/hadoop/hdfs-site.xml
```
Add the following lines in between configuration.
```
<property>
  <name>dfs.replication</name>
  <value>4</value>
</property>
```
Configure yarn-site.xml.
```
[1] sudo nano /usr/local/hadoop/etc/hadoop/yarn-site.xml
```
Add the following lines in between configuration.
```
<property>
  <name>yarn.nodemanager.aux-services</name>
  <value>mapreduce_shuffle</value>
</property>
<property>
  <name>yarn.resourcemanager.hostname</name>
  <value>master</value>
</property>
```
## 10. Formatting the file system [ALL]

Finally we need to configure the file system:

```
[1] hdfs namenode -format
```

# Running Map-Reduce over our dataset

Once the cluster is set up and running, we will start downloading our data and running MapReduce over our dataset. Before doing anything, we should check if the cluster was correctly setup. To check if we successfully set up the cluster we will start by running this commands in the master node.
```
[1] \usr\local\hadoop\sbin\start-dfs.sh
[2] \usr\local\hadoop\sbin\start-yarn.sh
```

These commands will start the Hadoop File System, and the resource manager. Once the startup process ends, we can check if our nodes are ready to replicate the data we download and to work on the MapReduce job by running the following command on the master node and the slave nodes.
```
jps
```

In the master node we should get something like this/
```
[process num] SecondaryNameNode
[process num] NameNode
[process num] NodeManager
[process num] Jps
[process num] FsShell
[process num] DataNode
[process num] ResourceManager
```

In the slave nodes, we should get something like this instead.
```
[process num] DataNode
[process num] NodeManager
[process num] Jps
```

If everything is working as expected we can proceed to download the files and run the MapReduce job. First we will stop the NodeManager, and the DataNodes by running the following command.
```
[1] \usr\local\hadoop\sbin\stop-dfs.sh
[2] \usr\local\hadoop\sbin\stop-yarn.sh
```

Our MapReduce process will be running a custom Mapper and Reduced that we implemented, so before running the MapReduce job, we must make sure that all our nodes have access to these scripts. The script tho run the MapReduce job is configured in a way that points to the Mapper and Reducer scripts in this Github project. So we should run this commands in all our instances.
```
[1] su - hduser
[2] cd /home/hduser
[3] mkdir Work
[4] cd Work
[5] git clone "this repo url"
```

Then we need to make sure that the scripts can be executed by the nodes, so we need to go into _SDA_Project_ folder that will appear after we clone this repository, and run the following commands on all our nodes.
```
[1] chmod +x MapHadoop.py
[2] chmod +x ReducerHadoop.py
```

Once all this steps have been completed we can procede to run our main script _Main.py_, which will take care of a few things that we will explain now.

## 1. Starting the HDFS and the Resource Manager
First our script will start Hadoop File System and the Resource manager that will take care of distributing the MapReduce job over the worker nodes.

## 2. Getting the files
After HDFS and the resource manager are ready, our script will continue by downloading all the files that we specify, this can be done by filtering by month,day and/or year the different files that are listed in the _masterfiles.txt_ file. Our script will take care of downloading in the master node every file, unzip it, get rid of the data that we don't need from this file to save space, transfer it to HDFS and delete it from the local file system on the master node.

## 3. Running the MapReduce job
Once all the files specified are downladed, the script will procede to run the MapReduce job on all our slave nodes, remember that our master node is also a slave node in this project. This will be done by submitting one command from the script that will indicate which will be the Mapper and Reducer scripts used for this job, and the list of files that will be implied in this job and the outpuit folder.

## 4. Stopping HDFS and the Resource Manager
Whenever the MapReduce job is done, and the results are retrieved from HDFS to the local machine, the script will take care of stopping HDFS and the Resource Manager.

# Results

To show our results, the Python script developed will use Matplotlib's Basemap Toolkit as we mentioned at the beginning of this document. It will also use Numpy to manipulate our data. So the first step of this last part will be to install all the modules that we will need for this script to run.
```
[1] sudo apt-get install python-matplotlib
[2] sudo apt-get install python-mpltoolkits.basemap
[3] sudo apt-get install python-numpy //This may be unnecesary, as when we install matplotlib, the numpy package is installed too
```

Another way of installing this tool may be using Python's pip instead.
```
[1] sudo apt-get install python-pip
```

And then run the following commands.
```
[1] pip install matplotlib
[2] pip install numpy
```

Once we have installed Matplotlib, Numpy, and Basemap, we will procede to plot our results. To plot the results, we will need to run the _HeatMap.py_ script. Notice that depending on the data that we want to plot, we need to change the line that loads the file from out _Results_ folder that contains the results of running the MapReduce over our dataset.

```
mydata = open("/Path/to/Results/part-00000","r")
```

After updating this line to open the results file, we can finally run our script.

```
python HeatMap.py
```

And a window will open showing the results:

![picture](https://raw.githubusercontent.com/jarechalde/SDA-Project/master/Mymap.jpg)"Results"
