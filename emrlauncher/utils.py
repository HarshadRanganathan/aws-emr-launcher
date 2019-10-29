import re
import collections
from copy import deepcopy


def substitute_placeholders_with_values(data, input_vars):
    """
    substitute_placeholders_with_values: replaces placeholders with values from global props
    :param data:
    :type data: str
    :param input_vars: Input variables which serve as parameters for the configuration files
    :type input_vars: dict
    :return: str
    """
    val = deepcopy(data)
    placeholders = re.findall(r'\${([A-Z_]*)}', val, re.MULTILINE)
    if len(placeholders) == 0:
        return val
    else:
        for placeholder in placeholders:
            if placeholder in input_vars:
                val = val.replace("${{{0}}}".format(placeholder), input_vars.get(placeholder))
        return val


def dict_merge(dct, merge_dct):
    """
    dict_merge: merges dictionary keys
    :param dct: dict onto which the merge is executed
    :type dct: dict
    :param merge_dct: dict to be merged
    :type merge_dct: dict
    :return: new dict with the merges
    """
    dct = deepcopy(dct)
    for k, v in merge_dct.items():
        if isinstance(dct.get(k), dict) and isinstance(v, collections.Mapping):
            dct[k] = dict_merge(dct[k], v)
        else:
            dct[k] = v
    return dct
