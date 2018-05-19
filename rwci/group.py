import shortuuid
import time

class Group:
    def __init__(self, members):
        self.members = members
        self.id = shortuuid.ShortUUID().random(length=7)
        self.messages = []
        self.timestamp = time.time()
