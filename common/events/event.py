

class Event:
    def __init__(self):
        self.handlers = set()

    def on_trigger(self, handler):
        self.handlers.add(handler)

    def trigger(self):
        for handler in self.handlers:
            handler()
