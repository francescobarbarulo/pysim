# pysim

pysim is an event-driven python simulator. It was born for fun based on the OMNET++ concept. One of the advantages is that  the network definition is no more needed. Of course it actually misses all the statistic functionalities, but they will be available soon.

## Repo

The repository is organized in this way:
- _core_ contains all the essential data structures for running the simulator (it should not be touched except if you want to improve it, in this case you are welcome);
- _examples_ contains some demo to show how the simulator works and some of its features;
- in the repo you can find the two _main_ programs related to the two examples.

Try these example just downloading the repo, entering the repo and issuing:
```
python3 echo_reply.py
```

## Configuration

In order to start the simulation, the configuration file `pysim.ini` must be placed in the main directory and it should contain at least two parameters as follows:
```ini
# pysim.ini

[DEFAULT]
sim_time_limit = 10
repeat = 1
```

- `sim_time_limit` specifies the duration of the simulation.
- `repeat` specifies the number of repetitions.

## BaseModule module

The `BaseModule` is the base class that represents a module from which all the modules must be derived. It can be considered as an interface.
Indeed, if you want to create your own module, you can override three methods exposed by this interface:

- `initialize()` sets the module for new simulations.
- `handle_message(msg)` is called whenever the module receives a message.
- `finish()` is called at the destruction of the module and here you can destroy the module's data structures.

If you want to provide further data structures to your module you need to implement also its constructor which must invoke the base class constructor.
In this case, it is **mandatory** to initialize the data structures not only in the constructor but also in the `initialize()` function.

Moreover `BaseModule` provides some methods for sending messages:
- `send(msg, dest, delay)` is the standard method for sending a message `msg` to module with name `dest` with a delay equal to `delay` (default 0).
- `schedule_at(msg, delay)` allows a module to send the message to itself.

### Build your own module

Your own module should look like the following:
```python
# examples/Sample/sampleModule.py

from core.modules.baseModule import BaseModule
from core.message import Message


class SampleModule(BaseModule):
    def __init__(self, name):
        # the call to the base class constructor must be the first
        super(SampleModule, self).__init__(name)
        # here data structures can be defined, for instance
        self.queue = []

    def initialize(self):
        # initialize your data structures also here!
        self.queue = []
        # if you want the module to start you need to schedule a message
        # so that it will trigger the handle_message function
        msg = Message()
        self.schedule_at(msg, delay=0)

    def handle_message(self, msg):
        # consume the message
        print("New message received\ntext: {}\nfrom: {}".format(msg.get_text(), msg.get_source()))

    def finish(self):
        # destroy all used data structures
        pass

```

For creating a new simulation script you need to create a new file, for instance `sample.py`, in the main directory.

```python
# sample.py

from core.simulator import Simulator

# import your own modules, for instance
from examples.Sample.sampleModule import SampleModule


def main():
    # create a new simulator
    sim = Simulator()

    # register your module
    sim.register_module(SampleModule("sample"))

    # run the simulator
    sim.run()


if __name__ == '__main__':
    main()
```

Finally, let's launch the simulation by issuing:
```
python3 sample.py
```

The outcome should look like:
```
New simulation is started at 22-03-2020 11:10:30:380067
New message received
text: hello
from: sample
Simulation finished at 22-03-2020 11:10:30:380232
```

## Messages

Modules interacts each other by means of messages. `Message` is a data structure that keeps:
- _text_ of the message;
- _src_ represents the sender of the message;
- _dest_ represent the receiver of the message.

Furthermore it offers the method `is_self_message()` to let you know if the message has been scheduled through the `schedule_at` function.

The `Message` class can be derived in order to create your custom messages. Be careful to not override methods of the base class.

## Collaborate
You are welcome for improving the pysim!
