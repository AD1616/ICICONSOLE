import signal

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

timeout = 20