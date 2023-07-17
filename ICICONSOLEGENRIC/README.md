# ICICONSOLE


## Overview

ICICONSOLE is designed to provide an efficient and powerful interface to Neo4j Knowledge Graph databases hosted on HPC resources, leveraging Tapis. 

This application is specialized for knowledge graph querying, and has some basic CYPHER commands built in. 

### Installation

Requires Python 3.10 or higher. You can clone this repository and manually install the requirements, or you can directly install the application from PyPi.

```shell 
pip install ICICONSOLE
```

```shell
python -m ICICONSOLE
```

**OR**

```shell 
git clone https://github.com/AD1616/ICICONSOLE.git
```

```shell
cd ICICONSOLE/ICICONSOLE_PROD/ICICONSOLE
```

```shell
pip install pandas
```

```shell
pip install py2neo
```

```shell
pip install tapipy
```

```shell
pip install datascroller
```

```shell
python ICICONSOLE.py
```

### First time user setup

You have two options as of now: connecting to a Neo4j database hosted on a Tapis Pod at the Texas Advanced Computing Center, or downloading Neo4j Desktop and connecting to a database that you are running locally. 

#### Tapis

When prompted to change authentication type from Tapis, enter "n". It will then present the default ICICLE base url for tapis, which you can modify by typing "y" to the prompt to change base url. 

You will then be asked to login with your TACC account. If you aren't sure if you have this, visit the TACC [portal](https://portal.tacc.utexas.edu/).

Once you enter your username and password to ICICONSOLE, you will see the Tapis Pods that you have been given permission to access. If you don't see any, please contact the owner of the Pod you wish to access. Type in the ID of the Pod that you want to access. 

#### Local
If you are running a Neo4j database locally, you will need to download Neo4j Desktop. You can download it [here](https://neo4j.com/download/).

Next, you have to run a local dbms. This should be running by default on bolt port 7687, which is what ICICONSOLE will try to connect to. 

In ICICONSOLE, when prompted to change authentication type from Tapis, enter "y". Then type "local". 

Next, enter any username and graph name; this is just for personalization in the application and not needed for authentication. 

The graph password, however, is important. This is the password that you set within Neo4j Desktop for your local database.


### First time usage guide

Once you access either a Tapis Pod or your local database, you will be in a custom made console for interfacing with your Knowledge Graph, using the Cypher language. If you know Cypher, you can start typing in commands like 

```
MATCH(n) RETURN n LIMIT 10
```

If you are not familiar with Cypher, don't worry! This is meant for users who have never used Cypher before. Type in "help" to view some of the built in commands to start exploring the knowledge graph. These commands are very limited however; you can query more creatively and extensively using the power of GPT. Type in the "GPT" command for this. Note that you will need an OpenAI key, which you can get [here](https://beta.openai.com/). Then, you can simply type in a query in natural language and get the Cypher code for it.

The welcome message for the Knowledge Graph console contains helpful tips, like "new", "exit", "clear", and "help". 

