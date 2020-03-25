"""
    *** Simple example ***
    This simulation implements an echo-reply interaction between two modules.
"""

from examples.EchoReply.echoModule import EchoModule
from examples.EchoReply.replyModule import ReplyModule
from pysim.simulator import Simulator


def main():
    sim = Simulator()

    sim.register_module(EchoModule("echo"))
    sim.register_module(ReplyModule("reply"))

    sim.run()


if __name__ == '__main__':
    main()

