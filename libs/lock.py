"""

 Created by plough on 2019/7/5.
"""

class SimpleLock:

    def __init__(self):
        self.locked = False


    def unlock(self):
        if self.locked:
            self.locked = False

    def is_locked(self):
        return self.locked

    def lock(self):
        self.locked = True