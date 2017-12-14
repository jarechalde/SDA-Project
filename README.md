# MAP REDUCE On the GDELTS GKG Dataset

This Projects objective is run use map-reduce in a hadoop cluster, for sentiment analysis, using the GDELTS dataset.

# Data used in this project
The data used in this project is available as a list of links to the files [here](http://data.gdeltproject.org/gdeltv2/masterfilelist.txt), but our main script will download it on our instance automatically and select the urls that we will use.

## Getting Started

First we will start by setting up the hadoop cluster, for this project we will create 4 instances, and configure them as it follows.

We will create on Google Cloud Platform 4 instances that will serve as master and slave nodes for our project. We created 4 instances each one of them having 1 vCore and 4 GB of RAM, and 500GB of disk each one, due to the limitation of 2TB inside a project. Ths instances will be running Ubuntu 16.04 LTS

### [ALL] 1. Installing java

First we will need to install java.

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install default-jre
sudo apt-get install default-jdk
```

To check if Java was installed correctly we can run this command
```
java -version
```
And the java version should show up in case it was successfully installed.

### [MASTER] 2. Installing unzip 

Our main file will be using unzip to unzip all the incoming files, so we will need to install the unzip package on the master node. This can be done by executing this simple command.

```
sudo apt-get install unzip
```

### [ALL] 3. Creating Hadoop users

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

### [MASTER] 4. Giving access to the slave nodes to the master node

The master node should be able to access all the other nodes in the cluster without a ssh key, to run the map-reduce job, so we need to create a public key by running the first command. After running the second command, we will get the key string. The way Google instances get the ssh keys is different than in any other service. Google instances get the ssh key values from Google Cloud Platform whenever they are started, so we will need to copy the key string obtained by executing the second command to Metadata > SSH Keys on the Google Cloud Platform Computer Engine menu. Then when we connect to any of the instances, Google Cloud Platform will pass this keys to the instance and add it to the authorized keys list. If this setup was done in another service, the key value should be added manually to the authorized keys list in the other instances manually.

```
[1] ssh-keygen -t rsa -P ""
[2] cat $HOME/.ssh/id_rsa.pub
```
[ALL] Then we will need to add the IP addresses of the all the instances to the hosts file in all instances. We can open this file by running this command.
sudo nano /etc/hosts
[ALL] Then we will need to add the following lines to the file. The IP we need to use is the Internal IP that is shown in the Google Compute Engine Dashboard.
[IP of Master] master
[IP of slave1] slave1
[IP of slave2] slave2
...
[IP of slaveN] slaveN

[ALL] Then we will need to disable ipv6 by adding this lines to /etc/sysct1.conf. 
# disable ipv6
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1

[MASTER] Now we can check if we can connect to the slave and master nodes from the master node. To check this, we must run the following commands and answer yes whenever they ask us if we want to continue connecting.
ssh master
ssh slave1
ssh slave2
...
ssh slaveN


[ALL] Now we will proceed to install Hadoop. First, we will go to the local folder, then we will download Hadoop, then we will extract it and move it to the Hadoop folder. To get the URL, go to Hadoops Releases webpage and get the last released binary file download address, in this case 2.9.0.

cd /usr/local
wget [download_url]
sudo tar xzf [file name]
sudo mv [extracted folder name] hadoop
sudo chown – R hduser:hadoop hadoop

[ALL] Now we need to add Hadoop home and java home to the path
sudo nano $HOME/.bashrc
Add the following lines at the end of the file.
export HADOOP_HOME =/usr/local/hadoop
export JAVA_HOME = /usr/lib/jvm/default-java

[ALL] Then we configure the Hadoop environment variables.
sudo nano /usr/local/hadoop/etc/hadoop-env.sh
Edit the JAVA_HOME value in the file with the java directory.
export JAVA_HOME = /usr/lib/jvm/default-java

[ALL] Create a temporary folder so hadoop can store its files while we download them and transfer them to Hadoop File Hystem.
sudo mkdir -p /app/hadoop/tmp
sudo chown hduser:hadoop /app/hadoop/tmp
sudo chmod 750 /app/hadoop/tmp

[MASTER] Configure the masters’ and slaves’ files.
Masters file.
sudo nano /usr/local/hadoop/etc/hadoop/masters
Add the following line.
master

Slaves file.
sudo nano /usr/local/hadoop/etc/hadoop/slaves
Add the following lines.
master
slave1
...
slaveN

[ALL] Configure the site xml file in all machines
sudo nano /usr/local/hadoop/etc/hadoop/core-site.xml
Add the following lines.
<property>
<name>hadoop.tmp.dir</name>
<value>/app/hadoop/tmp</value>
</property>
<property>
<name>fs.defaultFS</name>
<value>hdfs://master:54310</value>
</property>

[ALL] Configure mapred-site.xml
sudo nano /usr/local/hadoop/etc/hadoop/mapred-site.xml
Add the following lines.
<property>
<name>mapreduce.framework.name</name>
<value>yarn</value>
</property>

[ALL] Configure hfs-site.xml inside value put the number of slaves, in this case 4, as the master node is also a Data Node.
sudo nano /usr/local/hadoop/etc/hadoop/hdfs-site.xml
Add the following lines.
<property>
  <name>dfs.replication</name>
  <value>4</value>
</property>

[ALL] Configure yarn-site.xml.
sudo nano /usr/local/hadoop/etc/hadoop/yarn-site.xml
Add the following lines.
<property>
<name>yarn.nodemanager.aux-services</name>
<value>mapreduce_shuffle</value>
</property>
<property>
<name>yarn.resourcemanager.hostname</name>
<value>master</value>
</property>

[MASTER] Finally we need to configure the file system:
bin/hadoop namenode -format


## Running the tests

###1. First Map-Reducer 

After creating the Python Mapper and Reducer functions, we ran some tests to see if they were behaving properly. For this tests, we didn't use hdfs.

```
find . -name \*2016010112*\ -print | /home/jarechalde/Project/SDA-PROJECT/Map3.py | sort -k1,1 -k2,1 | /home/jarechalde/Project/SDA-Project/Reducer.py
```
This test, sends the mapper file a list of CSV files, the mapper takes this files and extracts all the coordinates found in this file, after that we sort the coordinates in ascending order, first the longitude and then the latitude. In the end, we send this list to the reducer function, which takes this list as an input and reduces them, counting the number of times each location appeared, and calculating the average of the sentiments for each unique location.

Explain how to run the automated tests for this system

###2. Testing the map reducer on Hadoop

Now we will test Map Reduce on Hadoop, for that we will first need to transfer our data files to hadoop file system. We will test this first copying only one days data.

```
hdfs dfs -copyFromLocal ~/Path-to-local-Files/Files/2016/01/01 ~/Path-to-some-other-folder/
```

To check if the files were copied successfully we run this command.

```
hdfs dfs -ls
```

We have to find the hadoop streaming jar next, which maybe located in different folders depending on the hadoop version. To find it we run this command.

```
sudo find / -name "hadiio-streaming*.jar"
```

In my case the file was located in this folder.

```
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.9.0.jar
```

Then we execute this command for the map-reduce

```
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.9.0.jar -file /home/jarechalde/Project/SDA-Project/Map3.py -mapper /home/jarechalde/Project/SDA-Project/Map3.py -file /home/jarecha
lde/Project/SDA-Project/Reducer.py -reducer /home/jarechalde/Project/SDA-Project/Reducer.py -input /home/jarechalde/Hadoop/01/* -output /home/jarechalde/Hadoop/hadoop-output
le /home/jarechalde/Project/SDA-Project/Reducer.py -reducer /home/jarechalde/Project/SDA-Project/Reducer.py -input 
```


And the files should be showing there.
