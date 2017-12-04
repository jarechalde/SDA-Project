# MAP REDUCE On the GDELTS GKG Dataset

This Projects objective is to use map-reduce in a hadoop cluster, for sentiment analysis, using the GDELTS dataset.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

After installing Hadoop in the machine, we need to add it to the path, in order to do this we will need to edit the ~/.bashrc file. After that, we will be ready to start transferring files to the Hadoop file system in order to start working with hadoop.
```
export PATH=$PATH:usr/local/hadoop/bin
```


End with an example of getting some data out of the system or using it for a little demo

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

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
