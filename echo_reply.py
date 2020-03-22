"""
    *** Simple example ***
    This simulation implements an echo-reply interaction between two examples.
"""

from examples.EchoReply.echoModule import EchoModule
from examples.EchoReply.replyModule import ReplyModule
from core.simulator import Simulator


def main():
    sim = Simulator()
    ''' 
        Add examples here:
        - in a single statement like in the example;
        - in more statements:
            sim.register(SimpleModule("s1"))
            sim.register(SimpleModule("s2"))
    
    '''
    sim.register(EchoModule("echo"), ReplyModule("reply"))

    sim.run()


if __name__ == '__main__':
    main()

