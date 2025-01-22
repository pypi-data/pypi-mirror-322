import platform
from typing import Union, Optional
from hrenpack.listwork import split_list, intlist, floatlist, merging_dictionaries, if_dict_key, dict_keyf
from hrenpack.numwork import dec_to_hex, hex_to_dec


class stl(list):
    def __init__(self, source: Union[str, int, float, bool], *args, **kwargs) -> None:
        super().__init__()
        self.vstring = str(source)
        self.vlist = self.vstring.split(', ')
        self.save()
        self.__float__ = lambda: floatlist(self.vlist)
        self.__int__ = lambda: intlist(self.vlist)
        self.args, self.kwargs = args, kwargs
        self.not_empty = self.__bool__

    def __str__(self) -> str:
        return self.vstring

    def __list__(self) -> list:
        return self.vlist

    def __tuple__(self) -> tuple:
        return self.vtuple

    def save(self) -> None:
        self.vtuple = tuple(self.vlist)
        self.vstring = split_list(self.vlist)

    def split(self, isTuple: bool) -> Union[tuple, list]:
        return self.__tuple__() if isTuple else self.__list__()

    def append(self, value) -> None:
        self.vstring = f'{self.vstring}, {value}'
        self.vlist.append(value)
        self.save()

    def pop(self, index: int = -1) -> None:
        self.vlist.pop(index)
        self.save()

    def reverse(self) -> None:
        self.vlist.reverse()
        self.save()

    def remove(self, value) -> None:
        self.vlist.remove(value)
        self.save()

    def count(self, value) -> int:
        return self.vlist.count(value)

    def index(self, value, **kwargs) -> int:
        return self.vlist.index(value)

    def __len__(self) -> int:
        return len(self.vlist)

    def __bool__(self) -> bool:
        return bool(self.vlist)

    def __copy__(self):
        return stl(self.vstring)

    def __hash__(self):
        return hash(self.vstring)

    def __eq__(self, other) -> bool:
        return self.vstring == other.vstring

    def __ne__(self, other) -> bool:
        return self.vstring != other.vstring

    def clear(self):
        self.vlist.clear()
        self.save()

    def copy(self):
        return stl(self.vstring)

    def sort(self, *, key=None, reverse=False):
        self.vlist.sort(key=key, reverse=reverse)
        self.save()

    def __setitem__(self, key, value):
        self.vlist[key] = value
        self.save()

    def __getitem__(self, key):
        return self.vlist[key]

    def __delitem__(self, key):
        del self.vlist[key]
        self.save()

    def insert(self, __index, __object):
        self.vlist.insert(__index, __object)
        self.save()


class DictionaryWithExtendedFunctionality(dict):
    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__ = kwargs

    def merge(self, *dicts):
        self.__dict__ = merging_dictionaries(self.__dict__, *dicts)


class MatrixCore:
    def __init__(self, path_to_file: str = '</return/>'):
        self.path_to_file = path_to_file
        self.is_return = self.path_to_file == '</return/>'

    class RectMatrix:
        def __init__(self, width: int, height: int, default_value=0):
            self.matrix = list()
            self.width, self.height = width, height
            for y in range(height):
                yl = list()
                for x in range(width):
                    yl.append(default_value)
                self.matrix.append(yl)

        def __setitem__(self, x: int, y: int, value):
            self.matrix[y][x] = value

        def __getitem__(self, x: int, y: int):
            return self.matrix[y][x]

        def __str__(self, separator: str = ' ') -> str:
            def step1(argument):
                def step2(arg):
                    def step3(a):
                        pass

                    vs = arg.split()
                    return split_list(vs, separator)

                al = argument.split('\n')
                al.pop(0)

                return split_list(al, '\n')

            output = ''
            for yl in self.matrix:
                po = ''
                for xel in yl:
                    po = po + separator + str(xel)
                output = output + '\n' + po
            return step1(output)


class DataClass:
    __default_classname__: str = 'DataClass'

    def __init__(self, **kwargs):
        self.__classname__ = kwargs.get('__classname__', self.__default_classname__)
        if '__classname__' in kwargs.keys():
            del kwargs['__classname__']
        self.__kwargs__: dict = kwargs
        self.__methods__ = ('__dict__', '__setitem__', '__getitem__', '__delitem__', '__len__', '__bool__', '__copy__',
                            '__update__', '__str__', '__clear__', '__methods__')
        self.__update__(**kwargs)

    def __dict__(self):
        return self.__kwargs__

    def __setitem__(self, key, value):
        self.__kwargs__[key] = value

    def __getitem__(self, key):
        return self.__kwargs__[key]

    def __delitem__(self, key):
        del self.__kwargs__[key]

    def __len__(self):
        return len(self.__kwargs__)

    def __bool__(self):
        return bool(self.__kwargs__)

    def __copy__(self):
        return DataClass(**self.kwargs)

    def __update__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.__methods__:
                self.__kwargs__[key] = value
                setattr(self, key, value)
            else:
                raise ValueError(f"Имя {key} зарезервировано")

    # def __str__(self):
    #     classname = self.__classname__
    #     if classname == '</empty/>':
    #         string = ''
    #     else:
    #         string = classname + '('
    #     for key, value in self.__kwargs__.items():
    #         string += f'{key}={value}, '
    #     string = string[:-2]
    #     if classname != '</empty/>':
    #         string += ')'
    #     return string

    def __str__(self):
        string = self.__classname__ + '('
        for key, value in self.__kwargs__.items():
            string += f'{key}={value if type(value) is not str else f"'{value}'"}, '
        string = string[:-2]
        string += ')'
        return string

    def __clear__(self):
        self.__kwargs__.clear()

    def __ad_to_dt__(self):
        dicts = dict()
        for key, value in self.__kwargs__.items():
            if type(value) is dict:
                dicts[key] = PreEmptyDataClass(**value)
        self.__update__(**dicts)


class PreEmptyDataClass(DataClass):
    __default_classname__ = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.__classname__ != self.__default_classname__:
            self.__update__(__classname__=self.__classname__)


class EmptyDataClass(DataClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            del self.__classname__, self.__default_classname__
        except AttributeError:
            pass

    def __str__(self):
        string = ''
        for key, value in self.__kwargs__.items():
            string += f'{key}={value}, '
        string = string[:-2]
        return string


def dicts_to_dataclasses(cls):
    if issubclass(cls, DataClass):
        init = cls.__init__

        def new_init(self, **kwargs):
            init(self, **kwargs)
            self.__ad_to_dt__()

        cls.__init__ = new_init
    else:
        raise TypeError("Задекорированный класс должен наследоваться от класса DataClass")


if platform.system() == 'Windows':
    from tkinter import *

    class TkTemplate(Tk):
        def __init__(self, title: str, width: int, height: int, background: str = 'white', resizable: bool = False, **kwargs):
            super().__init__()
            self.title(title)
            self.resizable(resizable, resizable)
            self.geometry(f'{width}x{height}')
            self['bg'] = background
            if if_dict_key(kwargs, 'icon'):
                self.iconbitmap(kwargs['icon'])
            self.stylesheet = dict_keyf(kwargs, 'stylesheet', dict())
            self.__stylesheet__()
            self.widgets_init()

        def widgets_init(self):
            pass

        def __stylesheet__(self):
            self.stylesheet_class = DataClass(**self.stylesheet)
else:
    class TkTemplate:
        def __new__(cls, *args, **kwargs):
            raise OSError('This class is only supported on Windows')

        def __init__(self, *args, **kwargs):
            raise OSError('This class is only supported on Windows')


class Color:
    def __init__(self, red: int, green: int, blue: int) -> None:
        self.red, self.green, self.blue = red, green, blue
        self.hexCode = self.__hex__()

    def __hex__(self) -> str:
        return '#' + dec_to_hex(self.red) + dec_to_hex(self.green) + dec_to_hex(self.blue)

    def __dict__(self) -> dict:
        return {'red': self.red, 'green': self.green, 'blue': self.blue, 'hex': self.hexCode}

    def shuffle(self, hexCode: str) -> None:
        self.red = (self.red + hex_to_dec(hexCode[1:3])) // 2
        self.green = (self.green + hex_to_dec(hexCode[3:5])) // 2
        self.blue = (self.blue + hex_to_dec(hexCode[5:7])) // 2
        self.hexCode = self.__hex__()


class EmptyClass:
    """Обычный пустой класс"""


class range_plus:
    def __init__(self, *args, **kwargs):
        if kwargs:
            new_args = (kwargs.get('start', 0), kwargs['end'], kwargs.get('step', 1))
        elif args:
            args = list(args)
            largs = len(args)
            if largs == 1:
                new_args = (1, args[0] + 1, 1)
            else:
                args[1] += 1
                if largs == 2:
                    new_args = (args[0], args[1], 1)
                elif largs == 3:
                    new_args = args
                else:
                    raise ValueError("Максимум 3 аргумента")
        else:
            raise ValueError("Нужен хотя бы 1 аргумент")
        self.range = range(*new_args)

    def __iter__(self):
        return iter(self.range)

    def __str__(self):
        return str(self.range)


if __name__ == '__main__':
    color = Color(100, 100, 100)
    print(int('1010101010', 2))
