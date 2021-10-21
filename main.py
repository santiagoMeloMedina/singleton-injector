from typing import Any, Callable, Dict, List, Set
import inspect


class Singleton:
    def __init__(self):
        self.instances = {}

    def __call__(self, _class):
        def wrapper(*args, **kwargs):
            if _class not in self.instances:
                self.instances[_class] = _class(*args, **kwargs)
            return self.instances[_class]

        return wrapper


class Injector:
    def __init__(self, singleton: Singleton):
        self.singleton = singleton
        self._classes: Dict[str, Callable] = {}

    def __call__(self, class_wrapper: Callable):
        return class_wrapper

    def get_method_parameter_classes(self, _method: Callable) -> Dict[str, Callable]:
        parameters = inspect.getfullargspec(_method).annotations
        for name in parameters:
            _class = parameters[name]
            parameters[name] = self._classes[_class.__name__]()
        return parameters

    def __inject(self, _class: Callable, wrapper: Callable):
        parameter_classes = self.get_method_parameter_classes(_class.__init__)
        wrapper(**parameter_classes)

    def single(self, _class: Callable):
        class_wrapper = self.singleton(_class)
        self._classes[_class.__name__] = class_wrapper
        self.__inject(_class, self._classes[_class.__name__])
        return _class


singleton = Singleton()
injector = Injector(singleton)


@injector.single
class Car:
    def __init__(self):
        print("Im a car")


@injector.single
class Brand:
    def __init__(self, car: Car, car2: Car):
        print(car is car2)
