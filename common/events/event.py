

class Event:
    def __init__(self):
        self.handlers = []

    def on_trigger(self, handler):
        self.handlers.append(handler)

    def trigger(self):
        for handler in self.handlers:
            handler()
