from singleton_injector import injector


@injector
class Car:
    def __init__(self):
        print("Instantiating Car class on definition")


@injector
class Brand:
    def __init__(self, car: Car, car2: Car):
        print("Injected Car parameters are the same: %s" % (car is car2))
