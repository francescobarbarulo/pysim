import random


def intuniform(a, b):
    return random.randint(a, b-1)


def exponential(mean):
    return random.expovariate(1 / mean)


def lognormal(mean, stdev):
    return random.lognormvariate(mean, stdev)
