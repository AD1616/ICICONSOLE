# ICICONSOLE-GPT

## Overview

ICICONSOLE is designed to provide an efficient and powerful interface to Neo4j Knowledge Graph databases hosted on HPC resources, leveraging Tapis. 

This application is specialized for knowledge graph querying, and has some basic CYPHER commands built in. 

The difference between ICICONSOLE-GPT and ICICONSOLE is the integration of GPT-3.5 via the OpenAI API. Note that this means to access these features, an OpenAI API key is required; if you don't have one, you can use the rest of the ICICONSOLE features normally.

### Installation

Requires Python 3.10 or higher. You can clone this repository and manually install the requirements, or you can directly install the application from PyPi.

```shell 
pip install ICICONSOLE-GPT
```

```shell
python -m ICICONSOLE-GPT
```

**OR**

```shell 
git clone https://github.com/sdsc-hpc-training-org/hello_icicle_auth_clients.git
```

```shell
cd ICICONSOLE/ICICONSOLE_GPT/ICICONSOLE/
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
pip install openai
```

```shell
python __main__.py
```

### First time user guide

You will be asked to login with your TACC account. If you aren't sure if you have this, visit the TACC [portal](https://portal.tacc.utexas.edu/).

Next, you will see the Tapis Pods that you have been given permission to access. If you don't see any, please contact the owner of the Pod you wish to access. Type in the ID of the Pod that you want to access. 

Once you do this, you will be in a custom made console for interfacing with the Knowledge Graph, using the Cypher language. If you know Cypher, you can start typing in commands like 

```
MATCH(n) RETURN n LIMIT 10
```

If you are not familiar with Cypher, don't worry! This is meant for users who have never used Cypher before. Type in "help" to view some of the built in commands to start exploring the knowledge graph. These built in commands will grow more extensive as time goes on. 

The welcome message for the Knowledge Graph console contains helpful tips, like "new", "exit", "clear", and "help". 
