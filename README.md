# pysim

pysim is an event-driven python simulator for interactions between modules. 
Everyone can implement new modules for new simulations.

Modules interacts among them through messages which are instances of class `Message`.

## Message class
You can create a new message by passing the _text_ to the constructor as follows:
```
message = Message("hello world")
```

## BaseModule module

The `BaseModule` module is the base class from which all the modules must be derived. New modules can use the method
`send()` to send messages to other modules.

For the `send()` method, the following parameters must be specified:
- _message_: instance of the class `Message`;
- _destination_: name of the destination module;
- _delay_: optional parameter that specifies when the message must be sent in relation with the simulation time.

## Implement new module

A new module must be derived by the base class `modules.BaseModule` and *must implement only* the following methods:
- `initialize()` is called by the `modules.BaseModule` constructor and must call send() function at least one time
in order to start the simulation.
- `handle_message(msg)` is called whenever a module receive a message. Since all messages are broadcast to all modules involved
in the simulation, you must remember to check the message destination to know if the message is addressed to a specific module.
