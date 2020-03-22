import random


class PRNG(object):

    @staticmethod
    def intuniform(a, b):
        return random.randint(a, b)

    @staticmethod
    def exponential(lambd):
        return random.expovariate(1 / lambd)

    @staticmethod
    def lognormal(mu, sigma):
        return random.lognormvariate(mu, sigma)