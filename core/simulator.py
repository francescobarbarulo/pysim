class Simulator(object):
    def __init__(self):
        self.modules = []
        self.sim_time = 0
        self.events = []

    def add_module(self, m):
        self.modules.append(m)

    def notify_all(self, e):
        print("notify_all")
        new_events = []

        for module in self.modules:
            module_events = module.notify(e)
            new_events += module_events

        return new_events

    def run(self):
        for module in self.modules:
            self.events += module.load()

        while self.events:
            self.forward()

    def forward(self):
        print("forward")
        next_event = self.events.pop(0)
        self.sim_time = next_event.time
        new_events = self.notify_all(next_event)

        del next_event

        self.events += new_events
