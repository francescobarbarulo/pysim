# pysim

`pysim` is an event-driven python simulator. It was born for fun based on the OMNET++ concept. One of the advantages is that the network definition is no more needed (forget about NED files) and the _pythonic way of programming_ can be exploited.

## Table of contents
- [Requirements](#requirements)
- [Modules](#modules)
    - [BaseModule](#basemodule)
- [Messages](#messages)
- [Signals and Statistics](#signals-and-statistics)
- [Generating random variates](#generating-random-variates)
- [Timeliness](#timeliness)
- [Logging](#logging)
- [Build your project](#build-your-project)
- [Experiments](#experiments)
    - [Configure your experiments](#configure-your-experiments)
- [Running the examples](#running-the-examples)

## Requirements

`pysim` requires Python 3.6 or better

## Modules

Modules represent the actors that interact in the simulation environment. At the moment, two type of modules are provided, from which you can create your own one: `BaseModule` and `MobileModule`.

### BaseModule

The `BaseModule` is the base class that represents a module from which all the modules must be derived. It can be considered as an interface.
Indeed, if you want to create your own module, you can override three methods exposed by this interface:

- `initialize()` can be exploited for sending the first messaged.
- `handle_message(msg)` is called whenever the module receives a message.
- `finish()` is called at the destruction of the module and here you can destroy the module's data structures.

If you want to provide further data structures to your module you need to implement also its constructor which must invoke the base class constructor.

Moreover `BaseModule` provides some methods for sending messages:
- `send(msg, dest, delay)` is the standard method for sending a message `msg` to module with name `dest` with a delay equal to `delay` (default 0).
- `schedule_at(msg, delay)` allows a module to send the message to itself.


## Messages

Modules interacts each other by means of messages. `Message` is a data structure that keeps:
- _text_ of the message;
- _src_ represents the sender of the message;
- _dest_ represent the receiver of the message.

Furthermore it offers the method `is_self_message()` to let you know if the message has been scheduled through the `schedule_at` function.

The `Message` class can be derived in order to create your custom messages.
Be careful to not override methods of the `Message` base class: `get_text()`, `get_source()`, `get_dest()`.


## Signals and Statistics

Signals are useful for exposing statistical properties of the model. Signals are identified by a _name_ and are emitted by modules.

In order to emit a signal you need to register it first in the constructor of the associated module. At the registration you need to assign the name, which must be unique in the module, and the type of statistic you want to collect (only mean available at this moment) like in the following example:

```python
self.register_signal("response_time", "mean")
```

In order to emit a signal you can call the function specifying the _name_ of the signal and the _value_ as follows:

```python
self.emit("response_time", 1.23456789)
```

If the _warm_up_period_ is set, signals emitted in its range are not considered in the statistic computation.

At the end of the simulation, all the statistics associated to the registered signals are stored in the `experiment_dir` in a `.csv` file named _module_name-signal_name.csv_.

## Generating random variates

pysim gives the possibility to obtain streams of non-uniformly distributed random numbers from various distributions.
The simulation library supports the following distributions:

Distribution | Description
--- | ---
intuniform(a, b) | uniform distribution in the range \[a,b)
exponential(mean) | exponential distribution with the given mean
lognormal(mean, variance) | normal distribution with the given mean and variance

## Timeliness
Take in mind that values of **all** variables representing _time_ are treated as **seconds**.

## Logging

pysim provides a built-in _log_ function which acts accordingly to the simulation debug mode. It can be invoked directly by the modules by:
```python
self.log("log text")
```

The logging outcome is in the form:
```bash
INFO - pysim - [sim_time][module_name] your log text
```

## Build your project

If you want to build a project based on pysim, you can refer to the [examples](#running-the-examples).

The module class should look like the following:

```python
# project/modules.py

from pysim.modules.baseModule import BaseModule
from pysim.core.message import Message


class MyModule(BaseModule):
    def __init__(self, name) -> None:
        super(MyModule, self).__init__(name)
        # here data structures can be defined, for instance
        self.queue = []

    def initialize(self):
        # if you want the module to start you need to schedule a message
        # so that it will trigger the handle_message function
        msg = Message(msg="hello")
        self.schedule_at(msg=msg, delay=0)

    def handle_message(self, msg: Message) -> None:
        # consume the message
        self.log(text="Message '{}' received from {}".format(msg.get_text(), msg.get_source()))
        self.queue.append(msg)

    def finish(self):
        # destroy all used data structures
        self.queue.clear()

```

If you want to define some member variables in your class module, like in this case, you need to define a constructor which **must** take the module name as argument.

For creating a new simulation script you need to create a new file, for instance `project.py`, in the main directory.
In that file, you need to import the `Simulator` object which provides you two main functions:

- `register_module(create_module, name, quantity)` registers your module creating a number of instances accordingly to the _quantity_ value (default 1). Note that when the quantity is more than 1, the created modules will be named adding a `-{value}` to their original name.
Thus, if your module is named _my_module_ and you need 3 of it, they will be named as _my_module-0_, _my_module-1_ and _my_module-2_.
- `run()` starts the simulator.

The _main_ should look like the following:

```python
# project/main.py

from pysim.core.experiment import ex
from pysim.core.simulator import Simulator

# import your own modules, for instance
from modules import MyModule


@ex.automain
def main():
    # create a new simulator
    sim = Simulator()

    # register your module
    sim.register_module(create_module=MyModule, name="my_module")

    # run the simulator
    sim.run()

```

Finally, let's launch the simulation by issuing:
```
python project/main.py
```

The outcome should look like:
```
INFO - pysim - [0][my_module] Message 'hello' received from my_module
```

## Experiments

pysim uses [Sacred](https://sacred.readthedocs.io/en/stable/) for reproducing computational experiments.
pysim configurable parameters are listed in the following table:

Parameter | Description | Default value
--- | --- | ---
_seed_ | seed for the pysim _Pseudo Random Number Generator (PRNG)_ | random (generated by Sacred)
_sim_time_limit_ | simulation duration | 10
_warm_up_period_ | warm up period | 0
_experiment_dir_ | path to the directory in which statistic results are stored | 'results/'
_debug_ | enable or disable console logs | True

You can set all this parameter by:
```bash
python project/main.py with seed=0 sim_time_limit=20 warm_up_period=5 debug=False
```

Of course, the simulation will stop even if it has not reached the `sim_time_limit` in the case no more events are scheduled.

### Configure your experiments

If you need to configure some parameters, pysim exposes an `Experiment` instance you can use by importing it both in _modules.py_ and _main.py_ by:

```python
from pysim.core.experiment import ex
```

Some guidelines:

1. Define a configuration before the _main_ function just defining a simple function decorated by the `@ex.config` which containes the _key-value_ experiment parameters. They can be of any type.

```python
# project/main.py

...
@ex.config
def config():
    param1 = 1234
    param2 = "1234"
    param3 = True
...
```

2. Decorate the _main_ function with `@ex.automain`.
If you need to use some configuration parameters just pass them as arguments:

```python
# project/main.py

...
@ex.automain
def main(param1, param2, param3):
    ...
```

3. If you need to configure some parameters used by your module, just decorate its constructor with `@ex.capture` passing the parameters as arguments:

```python
# project/modules.py

...
@ex.capture
def __init__(self, param1, param2, param3):
    ...
```

## Running the examples

`pysim` comes with a number of examples illustrating how it works and which are its main features. 

If you are curious, you can browse these examples here: https://github.com/francescobarbarulo/pysim/tree/main/examples.

## Collaborate
Feel free to fork it and submit your changes, you are welcome!
