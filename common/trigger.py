

class Trigger:
    subscribers = set()

    def trigger(self, *args):
        for subscriber in self.subscribers:
            subscriber(*args)

    def listen(self, action):
        self.subscribers.add(action)
