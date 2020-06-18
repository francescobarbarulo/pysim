from point2d import Point2D

from pysim.core.modules.baseModule import BaseModule
from pysim.core.message import Message
from pysim.core.movement import Movement
import pysim.core.PRNG as PRNG


class MobileModule(BaseModule):
    def __init__(self, name, initial_position=Point2D(), speed=1):
        super(MobileModule, self).__init__(name)

        self._space = 1
        self._speed = speed
        self._position = initial_position
        self._position_to_reach = initial_position
        self._position_registration_time = 0

    def change_direction(self):
        direction = PRNG.intuniform(0, 4)
        if direction == 0:
            self._position_to_reach = Point2D(self._position.x + 1, self._position.y)
        elif direction == 1:
            self._position_to_reach = Point2D(self._position.x, self._position.y + 1)
        elif direction == 2:
            self._position_to_reach = Point2D(self._position.x - 1, self._position.y)
        else:
            self._position_to_reach = Point2D(self._position.x, self._position.y - 1)

    def move(self):
        self._position = self._position_to_reach
        self._position_registration_time = self.sim_time()

        self.change_direction()

        self.log("Current position: {}".format(self._position))
        self.log("Next position: {}".format(self._position_to_reach))

        self.schedule_at(Movement(), self._space / self._speed)

    def locate(self):
        direction = self._position_to_reach - self._position
        time = self.sim_time() - self._position_registration_time

        if direction.y == 0:
            loc = Point2D(self._position.x + self._speed * time * direction.x, self._position.y)
        else:
            loc = Point2D(self._position.x, self._position.y + self._speed * time * direction.y)

        return loc

    def initialize(self):
        delay = PRNG.exponential(1)
        self.schedule_at(Message(), delay)

    def handle_message(self, msg):
        self.log("Location: {}".format(self.locate()))

        delay = PRNG.exponential(1)
        self.schedule_at(Message(), delay)
