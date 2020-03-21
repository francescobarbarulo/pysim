"""
    *** Broadcast example ***
"""

from examples.Broadcast.broadcastModule import BroadcastModule
from examples.Broadcast.receiverModule import ReceiverModule
from core.simulator import Simulator


def main():
    sim = Simulator()

    sim.add_module(BroadcastModule("broadcast"))
    for i in range(5):
        sim.add_module(ReceiverModule("receiver-" + str(i)))

    sim.run()


if __name__ == '__main__':
    main()

