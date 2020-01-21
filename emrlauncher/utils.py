import re
import collections
from copy import deepcopy
from typing import Dict


def substitute_placeholders_with_values(data: str, input_vars: Dict[str, str]):
    """
    substitute_placeholders_with_values: replaces placeholders with values from global props
    :param data:
    :type data: str
    :param input_vars: Input variables which serve as parameters for the configuration files
    :type input_vars: dict
    :return: str
    """
    val = deepcopy(data)
    placeholders = re.findall(r"\${([A-Z_0-9]*)}", val, re.MULTILINE)
    if len(placeholders) == 0:
        return val
    else:
        for placeholder in placeholders:
            if placeholder in input_vars:
                val = val.replace(
                    "${{{0}}}".format(placeholder), input_vars.get(placeholder)
                )
        return val


def dict_merge(dct: dict, merge_dct: dict) -> dict:
    """
    dict_merge: merges dictionary keys
    :param dct: dict onto which the merge is executed
    :type dct: dict
    :param merge_dct: dict to be merged
    :type merge_dct: dict
    :return: new dict with the merges
    """
    dct = deepcopy(dct)
    for key, value in merge_dct.items():
        if isinstance(dct.get(key), dict) and isinstance(value, collections.Mapping):
            dct[key] = dict_merge(dct[key], value)
        else:
            dct[key] = value
    return dct
