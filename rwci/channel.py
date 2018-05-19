import time

class Channel:
    def __init__(self, name):
        self.name = name
        self.message = []
        self.timestamp = time.time()
