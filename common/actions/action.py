

class Action:
    subscribers = []
    def __call__(self):
        [sub(self) for sub in self.subscribers]
