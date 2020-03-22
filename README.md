# pysim

pysim is an event-driven python simulator. It was born for fun based on the OMNET++ concept. One of the advantages is that  the network definition is no more needed. Of course it actually missis all the statistic functionalities, but they will be available soon.

## Repo

The repository is organized in this way:
- _core_ contains all the essentail data structures for running the simulator (it should not be touched excpet if you want to improve it, in this case you are welcome);
- _examples_ contains some demo to show how the simulator works and some of its features;
- in the repo you can find the two _main_ programs related to the two examples.

Try these example just downloading the repo, entering the repo and issuing:
```
python3 echo_reply.py
```

## BaseModule module

The `BaseModule` is the base class that represents a module from which all the modules must be derived. It can be considered as an interface.
Indeed, if you want to create your own module, you can override three methods exposed by this interface:

- `initialize()` allows to begin the interaction. At least one of the modules registered to the system must send the first message. You can do this in this function.
- `handle_message(msg)` is called whenever the module receives a message.
- `finish()` is called at the destruction of the module and here you can destroy the module's data structures.

If you want to provide further data structures to your module you need to implement also its constructor which must invoke the base class constructor.

Moreover `BaseModule` provides some methods for sending messages:
- `send(msg, dest, delay)` is the standard method for sending a message `msg` to module with name `dest` with a delay equal to `delay` (default 0).
- `schedule_at(msg, delay)` allows a module to send the message to itself.

Here you can find how your module should be:
```python
from core.modules.baseModule import BaseModule
from core.message import Message

class SampleModule(BaseModule):
    def __init__(self, name):
        super(SampleModule, self).__init__(name)
        # here data structures can be defined, for instance
        self.queue = []

    def initialize(self):
        # initialize your data structures, for instance
        self.queue.append(object)

    def handle_message(self, msg):
        # consume the message
        print("New message received\ntext: {}\nfrom: {}".format(msg.text, msg.src))

    def finish(self):
        # destroy all data structures, for instance
        for o in self.queue:
            del o
```
