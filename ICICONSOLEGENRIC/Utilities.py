import signal
import json
import pkg_resources

# This class handles exiting the console application at any time.
class GracefulExiter():
    def __init__(self):
        self.state = False
        signal.signal(signal.SIGINT, self.change_state)

    def change_state(self, signum, frame):
        print("\nPress Ctrl+C again to exit.")
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.state = True

    def exit(self):
        return self.state
    
def timeout_handler(signum, frame):
    raise TimeoutError("Timeout occurred.")

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

# Loads help for cypher commands
def helpCypher():
    json_path = pkg_resources.resource_filename(__name__, 'helpCypher.json')
    print("\n")
    with open(json_path) as f:
        help_data = json.load(f)
    for key, value in help_data.items():
        print(key + ' : ' + value + '\n')

timeout = 20