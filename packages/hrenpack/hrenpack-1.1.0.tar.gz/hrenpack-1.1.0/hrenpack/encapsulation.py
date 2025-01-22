import functools, abc, inspect


class IncapsulationError(Exception):
    pass


def count_inheritance_levels(cls):
    # Получаем все классы в порядке разрешения методов
    mro = cls.__mro__
    # Считаем, сколько раз base_class есть в цепочке MRO
    count = 0
    for c in mro:
        if c is object:
            count += 1
    return count - 2


def check_method_in_parent(cls, name):
    bases = cls.__bases__
    print(bases)
    for base in bases:
        if hasattr(base, name):
            print(base.__name__)
            return True
    return False


def abstractmethod(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if AbstractClass in self.__class__.__bases__:
            return abc.abstractmethod(func(self, *args, **kwargs))


class AbstractClass:
    def __new__(cls):
        if cls is AbstractClass or AbstractClass in cls.__bases__:
            raise TypeError("Это абстрактный класс, его можно только наследовать")


def abstractclass(cls):
    class _Class(cls, AbstractClass):
        pass
    return _Class


class ClassMethodMeta(type):
    """Не работает"""
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)

        for attr_name, attr_value in attrs.items():
            if callable(attr_value):
                if '__' in attr_name:
                    continue
                setattr(new_class, attr_name, classmethod(attr_value))

        return new_class


class StaticClass(metaclass=ClassMethodMeta):
    """Не работает"""
    def __new__(cls):
        raise TypeError("Это статический класс, он не может создавать объекты")


def staticclass(cls):
    """Не работает"""
    class _Class(StaticClass, cls):
        pass
    return _Class


def inner_function():
    frame = inspect.currentframe()  # Получаем текущий стек вызовов
    local_vars = frame.f_back.f_locals
    del frame
    return local_vars


def protectedmethod(method):
    def wrapper(*args, **kwargs):
        stack = inspect.stack()
        for frame in stack:
            caller = frame.frame
            if caller.f_locals.get('self') is args[0]:
                return method(*args, **kwargs)
        raise IncapsulationError("Это защищенный метод")
    return wrapper


def privatemethod(method):
    """Пока что работает только как защищенный метод"""
    return protectedmethod(method)
