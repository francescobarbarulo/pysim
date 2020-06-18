import random


def intuniform(a, b):
    return random.randint(a, b-1)


def exponential(lambd):
    return random.expovariate(1 / lambd)


def lognormal(mu, sigma):
    return random.lognormvariate(mu, sigma)
