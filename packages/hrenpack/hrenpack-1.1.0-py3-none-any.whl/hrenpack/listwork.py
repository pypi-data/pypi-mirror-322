import re
from typing import Union, Literal, Optional
from hrenpack.boolwork import Fand

tuplist = Union[tuple, list]
tdl = Union[tuple, dict, list]


def IS_TUPLE(input: Union[tuple, list], is_tuple: bool) -> Union[tuple, list]:
    return tuple(input) if is_tuple else list(input)


def antizero(wnull):
    if wnull < 10:
        output = '0' + str(wnull)
    else:
        output = str(wnull)
    return output


def listsearch(list, search):
    for i in range(len(list)):
        if list[i] == search:
            index = i
            break
        else:
            index = False
    return index


def antienter(list):
    o = ''
    for i in range(len(list)):
        o = o + list[i]
    output = o.split('\n')
    return output


def antienter_plus(list):
    o = ''
    for i in range(len(list)):
        o = o + list[i]
    output = o.split('\n')
    el0 = output[0].split('\ufeff')
    pel = el0[-1]
    output[0] = pel
    output.pop()
    return output


def intlist(input: list) -> list:
    for i in range(len(input)):
        input[i] = int(input[i])
    return input


def floatlist(input: tuplist) -> list:
    input = list(input)
    for i in range(len(input)):
        input[i] = float(input[i])
    return input


def list_add(input: list, index: int, data) -> list:
    forcikl = len(input) + 1
    output = list()
    for i in range(forcikl):
        if i < index:
            output.append(input[i])
        elif i == index:
            output.append(data)
        elif i > index:
            m = i - 1
            output.append(input[m])
    return output


def str_to_list_one(string: str) -> list:
    output = list()
    for letter in string:
        output.append(letter)
    return output


def in_number_series(ot: int, to: int, num: int) -> bool:
    number_series = list()
    for i in range(ot, to):
        number_series.append(i)
    return num in number_series


def in_numbers(ot: int, to: int, nums: Union[tuple, dict, list]) -> dict:
    is_dict = dict()
    for num in nums:
        is_dict[num] = in_number_series(ot, to, num)
    return is_dict


def dict_to_list(input: dict, is_tuple: bool):
    output = list()
    for key in input:
        value = input[key]
        output.append(value)
    return IS_TUPLE(output, is_tuple)


def multi_pop(input: list, *indexes: int):
    for i in range(len(indexes)):
        index = indexes[i] - i
        try:
            if index == len(input) - 1:
                input.pop()
            else:
                input.pop(index)
        except IndexError:
            pass
    return input


def if_dict_key(dct: dict, key):
    try:
        dct[key]
    except KeyError:
        return False
    else:
        return True


def split_list(input: Union[tuple, list], separator: str = ', '):
    output = ''
    for el in input:
        if output == '':
            output = str(el)
        else:
            output = f'{output}{separator}{el}'
    return output


def merging_dictionaries(*dicts: dict) -> dict:
    output = dict()
    for d in dicts:
        output = {**output, **d}
    return output


# -1 - pd to d
# 0 - выполнять в любом случае
# 1 - d to pd
def pseudo_dictionary(input: tdl, not_edit_type: Literal[-1, 0, 1] = 0) -> tdl:
    if type(input) is dict and not_edit_type in (0, 1):
        output = list()
        for key, value in input.items():
            output.append((key, value))
    elif type(input) in (list, tuple) and not_edit_type in (-1, 0):
        output = dict()
        for el in input:
            key, value = el
            output[key] = value
    else:
        output = input
    return output


def variable_in_tuple(variable, *values):
    return variable in values


def pop(input: list, index: int = -1):
    input.pop(index)
    return input


split_list_enter = lambda input: split_list(input, '\n')
split_list_space = lambda input: split_list(input, ' ')
split_list_tab = lambda input: split_list(input, '\t')
dict_key_null = lambda dct, key: dct[key] if key in dct else None
dict_key_false = lambda dct, key: dct[key] if key in dct else False
dict_key_tf = lambda dct, key, true, false: true if key in dct else false
dict_keyf = lambda dct, key, false: dct[key] if key in dct else false
key_in_dict = lambda dct, key: dict_key_tf(dct, key, True, False)


def ab_reverse(a, b, condition: bool, is_tuple: bool = True) -> tuplist:
    output = [a, b]
    if condition:
        output.reverse()
    return tuple(output) if is_tuple else output


def ab_not_reverse(a, b, condition: bool, is_tuple: bool = True) -> tuplist:
    output = ab_reverse(a, b, condition, is_tuple)
    output.reverse()
    return output


def multi_reverse(condition, *args, is_tuple: bool = True) -> tuplist:
    args = list(args)
    if condition:
        args.reverse()
    return tuple(args) if is_tuple else args


def multi_not_reverse(condition, *args, is_tuple: bool = True) -> tuplist:
    output = multi_reverse(condition, *args, is_tuple=is_tuple)
    output.reverse()
    return output


def dict_keys_values(keys: tuplist, values: tuplist) -> dict:
    return dict(zip(keys, values))


def dkv_dict(source: dict, keys: tuplist, values: tuplist) -> dict:
    return merging_dictionaries(source, dict_keys_values(keys, values))


def remove_all(input: list, value, is_tuple: bool = False):
    count = input.count(value)
    for i in range(count):
        input.remove(value)
    return IS_TUPLE(input, is_tuple)


def remove_multi(input: list, *values, _remove_all: bool = False, is_tuple: bool = False):
    if _remove_all:
        for value in values:
            input = remove_all(input, value)
    else:
        for value in values:
            input.remove(value)
    return IS_TUPLE(input, is_tuple)


def list_to_list(input: list, index: Optional[int] = None, element=None, is_tuple: bool = True) -> tuplist:
    if index is not None and element is not None:
        raise TypeError("Оба аргумента не равняются None")
    elif index is None:
        index = input.index(element)
    in2 = input[index:-1]
    in2.pop(0)
    in2.append(input[-1])
    return IS_TUPLE((input[0:index], in2), is_tuple)


def list_tuple_to_str(input) -> str:
    try:
        if input is None:
            output = '()'
        elif isinstance(input, list) or Fand(isinstance(input, tuple), len(input) > 1):
            output = str(input)
        elif isinstance(input, tuple) and len(input) == 1:
            output = f'({input[0]})'
        else:
            output = f'({input})'
    except TypeError:
        output = f'({input})'
    finally:
        return output


def split_quotes(text: str, is_tuple: bool = False) -> tuplist:
    pattern = r"""
            (?:
                "(?:[^"\\]|\\.)*"
                |
                '(?:[^'\\]|\\.)*'
                |
                \S+              
            )
        """
    tokens = re.findall(pattern, text, re.VERBOSE)
    return IS_TUPLE(tokens, is_tuple)


def get_values_by_keys(input: dict, *keys, is_tuple: bool = False) -> tuplist:
    output = list()
    for key in keys:
        output.append(input[key])
    return IS_TUPLE(output, is_tuple)


def del_keys(input: dict, *keys) -> None:
    for key in keys:
        del input[key]


def dict_index(input: dict, value):
    for k, v in input.items():
        if v == value:
            return k
    else:
        raise ValueError(f"Словарь {input} не содержит значения {value}")


def strlist(input: tuplist, is_tuple: bool = False):
    input = list(input)
    for i in range(len(input)):
        input[i] = str(input[i])
    return IS_TUPLE(input, is_tuple)
