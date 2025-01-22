from typing import Union, Literal

stb = Union[str, bool]
tdl = Union[tuple, list, dict]


def booltest(bull: stb) -> None:
    if bull == 'True' or bull == 'False' or bull is True or bull is False:
        pass
    else:
        raise TypeError("Данная функция может работать только с булевыми значениями")


def str_to_bool(input: stb) -> bool:
    if input is True or input is False:
        return input
    elif input == 'True' or input == 'true' or int(input) == 1:
        return True
    elif input == 'False' or input == 'false' or int(input) == 0:
        return False
    else:
        raise TypeError("Данная функция может работать только с булевыми значениями")


def bool_list_count(input: tdl) -> dict:
    def TF(bull: bool, dict_tf: dict):
        if bull:
            dict_tf[True] += 1
        else:
            dict_tf[False] += 1

    TrueFalse = {True: 0, False: 0}
    if type(input) is dict:
        for key in input:
            value = input[key]
            booltest(value)
            TF(value, TrueFalse)
    else:
        for b in input:
            booltest(b)
            TF(b, TrueFalse)
    return TrueFalse


def Fand(*questions: bool):
    output = True
    for b in questions:
        if not b:
            output = False
            break
    return output


def For(*questions: bool):
    output = False
    for b in questions:
        if b:
            output = True
            break
    return output


def switch_For(variable, *values):
    return variable in values


def str_to_bool_soft(input: stb, return_false: bool = False):
    try:
        return str_to_bool(input)
    except TypeError:
        return False if return_false else input


def for_in(variable, mode: Literal['in', '==', 'is'], *values) -> bool:
    output = False
    if mode == 'in':
        for value in values:
            if value in variable:
                output = True
                break
    elif mode == 'is':
        for value in values:
            if value is variable:
                output = True
                break
    else:
        for value in values:
            if value == variable:
                output = True
                break
    return output
