# ICICONSOLE-GPT

## Overview

ICICONSOLE is designed to provide an efficient and powerful interface to Neo4j Knowledge Graph databases hosted on HPC resources, leveraging Tapis. 

This application is specialized for knowledge graph querying, and has some basic CYPHER commands built in. 

The difference between ICICONSOLE-GPT and ICICONSOLE is the integration of GPT-3.5 via the OpenAI API. Note that this means to access these features, an OpenAI API key is required; if you don't have one, you can use the rest of the ICICONSOLE features normally.

### Installation

Requires Python 3.10 or higher. You can clone this repository and manually install the requirements, or you can directly install the application from PyPi.

```shell 
pip install ICICONSOLEGPT
```

```shell
python -m ICICONSOLEGPT
```

**OR**

```shell 
git clone https://github.com/AD1616/ICICONSOLE.git
```

```shell
cd ICICONSOLE/ICICONSOLEGPT/ICICONSOLE/
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

The key feature of this is that in addition to the built in commands with ICICONSOLE, this application also has the ability to use GPT-3.5 to generate Cypher queries. To do this, use the "GPT" command once in the console, and then enter a query in natural language. 

The welcome message for the Knowledge Graph console contains helpful tips, like "new", "exit", "clear", and "help". 
