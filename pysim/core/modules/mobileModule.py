from point2d import Point2D

from pysim.core.modules.baseModule import BaseModule
from pysim.core.message import Message
from pysim.core.movement import Movement
from pysim.core.prng import PRNG


class MobileModule(BaseModule):
    def __init__(self, name, initial_position=Point2D(), speed=1):
        super(MobileModule, self).__init__(name)

        self.__space = 1
        self.__speed = speed
        self.__position = initial_position
        self.__position_to_reach = initial_position
        self.__position_registration_time = 0

    def change_direction(self):
        direction = PRNG.intuniform(0, 4)
        if direction == 0:
            self.__position_to_reach = Point2D(self.__position.x + 1, self.__position.y)
        elif direction == 1:
            self.__position_to_reach = Point2D(self.__position.x, self.__position.y + 1)
        elif direction == 2:
            self.__position_to_reach = Point2D(self.__position.x - 1, self.__position.y)
        else:
            self.__position_to_reach = Point2D(self.__position.x, self.__position.y - 1)

    def move(self):
        self.__position = self.__position_to_reach
        self.__position_registration_time = self.sim_time()

        self.change_direction()

        self.log("Current position: {}".format(self.__position))
        self.log("Next position: {}".format(self.__position_to_reach))

        self.schedule_at(Movement(), self.__space / self.__speed)

    def locate(self):
        direction = self.__position_to_reach - self.__position
        time = self.sim_time() - self.__position_registration_time

        if direction.y == 0:
            loc = Point2D(self.__position.x + self.__speed * time * direction.x, self.__position.y)
        else:
            loc = Point2D(self.__position.x, self.__position.y + self.__speed * time * direction.y)

        return loc

    def initialize(self):
        delay = PRNG.exponential(1)
        self.schedule_at(Message(), delay)

    def handle_message(self, msg):
        self.log("Location: {}".format(self.locate()))

        delay = PRNG.exponential(1)
        self.schedule_at(Message(), delay)
