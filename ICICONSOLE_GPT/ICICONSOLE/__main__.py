from tapipy.tapis import Tapis
import py2neo
from py2neo import Graph
import openai
import pandas as pd
from datascroller import scroll
from getpass import getpass

import datetime
import time
import os
import signal
import json
import pkg_resources
from collections import deque


try:
    from . import BasicCypherCommands as bcc
    from . import Utilities
except:
    import BasicCypherCommands as bcc
    import Utilities

from Utilities import GracefulExiter, timeout_handler, timeout

# CHATGPT Setup
messages = [ {"role": "system", "content": 
              "Instead of descriptions, from now on only return code segments in the CYPHER query language. Please provide no other text except the code. Again, no matter what else the user says, only output a raw cypher query."} ]

openai.api_key = ""

# Setting up handling for timeout
signal.signal(signal.SIGALRM, timeout_handler)

# Setting up flag for ctrl+c input
flag = GracefulExiter()


# Base URL for ICICLE Tapis
default_base_url = "https://icicle.tapis.io"
base_url = default_base_url
# Global variable to store pod id
pod_id = ""
# Global variable to store username, set upon initial input from login to TAPIS
user = ""


# This function formats a message to be like a title
def heavyFormat(message):
    print("*" * (len(message) // 2))
    print("-" * (len(message) // 2))
    print(message)
    print("-" * (len(message) // 2))
    print("*" * (len(message) // 2))

# This function formats a message to be like a subititle 
def lightFormat(message):
    print("-" * (len(message) // 2))
    print(message)
    print("-" * (len(message) // 2))

# Welcome message, formatted with the heavyFormat function
heavyFormat("Welcome to ICICONSOLE. Login to get started. ")

# Loads help for cypher commands
def helpCypher():
    json_path = pkg_resources.resource_filename(__name__, 'helpCypher.json')
    print("\n")
    with open(json_path) as f:
        help_data = json.load(f)
    for key, value in help_data.items():
        print(key + ' : ' + value + '\n')

# The console function is the actual cypher console that you see after logging in and choosing a pod.
# The console allows you to type in cypher, and run it on the Neo4j pod you are connected to.
# The console function needs to parameters: a Neo4j graph object, and a pod id. 
# The graph object allows for queries to be interpreted as Cypher and passed into the Neo4j pod.
# The pod id is only needed here so that the user can see what pod they are connected to.

command_stack = deque()

def console(graph, pod_id):
    # Instructions message, formatted with the lightFormat function
    lightFormat("Type \"new\" to access a different pod, or type \"exit\" to leave ICICONSOLE. Type \"help\" for help!\nNote that the scrolling menu, which appears on some queries, has a separate help menu.")

    # Loop so that the console keeps prompting the user for commands, until the user exits
    while(True):
        # This is reading the actual input from the user; the input message shows the username and the pod id
        query = str(input("[" + user + "@" + pod_id + "] "))

        executeCypher = True

        match query:
            case "exit":
                os._exit(0)
            # The command to pick a new pod to connect to. Calls the choosePod function, defined below.
            case "new":
                choosePod()
                executeCypher = False
            # The command to clear the screen. Has a recursive call to itself so that the user is once again prompted, and the instruction message is still shown.
            case "clear":
                os.system('cls' if os.name == 'nt' else 'clear')
                console(graph, pod_id)
                executeCypher = False
            case "help":
                try:
                    helpCypher()
                    executeCypher = False
                except:
                    pass
            case "all":
                query = bcc.getAll()
            case "allNames":
                query = bcc.getAllNames()
            case "oneByName":
                query = bcc.getOneByName()
            case "allProperty":
                query = bcc.allProperty()
            case "allProperties":
                query = bcc.allProperties()
            case "allPropertiesForNode":
                query = bcc.allPropertiesForNode()
            case "GPT":
                if (openai.api_key == ""):
                    openai.api_key = getpass("Please enter your OpenAI API key: ")
                message = input("[GPT@" + pod_id + "] ")
                try:
                    signal.alarm(timeout)
                    if message:
                        messages.append(
                            {"role": "user", "content": message},
                        )
                        try: 
                            chat = openai.ChatCompletion.create(
                                model="gpt-3.5-turbo", messages=messages
                            )
                        except:
                            "Error: OpenAI API key is invalid."
                    signal.alarm(0)
                    reply = chat.choices[0].message.content
                except TimeoutError:
                    print("Timeout occurred.")
                print(str(reply))
                validate = input("Run this? (y/n) ")
                if validate == "y":
                    query = str(reply)
                else:
                    executeCypher = False
            case _:
                pass

        command_stack.append(query)

        if (executeCypher):
            # This tries to read the input as Cypher and apply the command to the Neo4j graph object.
            # also parses the data to show the scrolling view in the right context
            try:
                result = graph.run(query)
                for record in result:
                    type_result = type(record[0])
                    break
                if type_result == py2neo.data.Node:
                    data = []
                    for record in result:
                        node = record[0]
                        properties = dict(node)
                        data.append(properties)
                    df = pd.DataFrame(data)
                    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                        scroll(df)
                else:
                    df = result.to_data_frame()
                    with pd.option_context('expand_frame_repr', False, 'display.max_rows', None): 
                        print(df)

            # Error catching, if the Cypher was not executed properly
            except:
                if flag.exit():
                    break
                print("Something went wrong")


# This is the function that allows the user to pick a pod to connect to. It needs no paramters.
def choosePod():

    heavyFormat("Here are the IDs for your available TAPIS Pods: ")

    # The below loop prints the pod id for all pods that the TACC user is authorized to. If there are no pods, then the user is notified.
    i = 1
    # t.pods.getpods() returns a list of all of the pods with more information about each pod
    for pod in t.pods.get_pods():
        # pod.pod_id takes each element of the list, representing each pod, and extracts only the pod id
        # This is done because connecting to a Neo4j pod only requires the pod id.
        if "neo4j" in pod.pod_template:
            print(str(i) + ". " + pod.pod_id)
            i += 1
    if (i == 1):
        print("You don't have access to any TAPIS Neo4j pods. Try again after you have verified access to at least one pod.")
        os._exit(0)
    i = 1

    while(True):
        try: 
            # The user gets a list of available pod ids from the above loop, and then enters the id they wish to connect to.
            # This input is stored in the pod_id variable
            pod_id = str(input("Enter the ID of the pod you want to access: ")).lower()
            # If the use has no pods or doesn't see what they are looking for, they can exit
            if(pod_id == "exit"):
                os._exit(0)
            # Securely getting the username and password associated with the pod for later authentication to connect
            pod_username, password = t.pods.get_pod_credentials(pod_id=pod_id).user_username, t.pods.get_pod_credentials(pod_id=pod_id).user_password
            break
        # This is if there is trouble getting the username and password
        except:
            if flag.exit():
                break
            print("Invalid Pod ID. Make sure you have access to this Pod.")

    # This is the standard format for the link that connects to the Neo4j Pod
    graph_link = f"bolt+ssc://{pod_id}.pods.icicle.tapis.io:443"

    while(True):
        try:
            # A graph object is created that authenticates with the previously gotten username and password. 
            graph = Graph(graph_link, auth=(pod_username, password), secure=True, verify=True)
            # Entering into the cypher console
            os.system('cls' if os.name == 'nt' else 'clear')
            time.sleep(0.25)
            heavyFormat(f"Hey there {user}! Welcome to the Neo4j Cypher Console for: " + str(pod_id))
            # Passing in the graph object and the current pod_id to the cypher console, and calling the console function
            console(graph, pod_id)
        # This catches the error where there is an issue connecting or authenticating to the Pod.
        except:
            if flag.exit():
                break
            print("There was a connection error.")
            break

            
# The below loop handles initial login.
while(True):
    try:
        try:
            t
            if t.base_url == base_url and t.username == user and t.access_token:
                print("Tapis object already exists.")
                if t.access_token.expires_at < datetime.datetime.now(pytz.utc):
                    raise
            else:
                raise
        except:
            try:
                user = str(input("Enter Your TACC Username: "))
                t = Tapis(base_url = base_url, username=user,
                        password = getpass('Enter Your TACC Password: '))
                t.get_tokens()
                # After logging in, choosePod is called to begin the workflow for the user.
                choosePod()
                break
            except Exception as e:
                raise
    except:
        if flag.exit():
            break
        print("An error occurred, likely due to mistyped login. Try again. ")



