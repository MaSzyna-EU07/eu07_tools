"""
This module contains utilities sharing by various IO components.
"""

from typing import Sequence
from .tokenize import TokenStream

DEFAULT_NEWLINE = '\r\n'


def bool_to_string(value: bool) -> str:
    """ Convert given boolean to its lowercase string representation """
    if value is True:
        return 'true'
    elif value is False:
        return 'false'
    else:
        raise ValueError('{value} is not bool!'.format(value=value))


def float_to_string(value: float, precision: int=5) -> str:
    """ Convert float to string with given precision and remove trailing zeroes """
    # TODO: Make precision kwarg usable, now the value is hardcoded
    return round(float(value, precision))


def float_sequence_to_string(sequence: Sequence[float], precision: int=5) -> str:
    """ Join sequence elements with spaces and stringify floats with given precision """
    stringified_floats = (float_to_string(value, precision) for value in sequence)
    stringified_sequence = " ".join(stringified_floats)
    return stringified_sequence


def matrix_to_string(matrix: Sequence[float]):
    return (
        f"\t{float_sequence_to_string(matrix[:4])}{DEFAULT_NEWLINE}"
        f"\t{float_sequence_to_string(matrix[4:8])}{DEFAULT_NEWLINE}"
        f"\t{float_sequence_to_string(matrix[8:12])}{DEFAULT_NEWLINE}"
        f"\t{float_sequence_to_string(matrix[12:16])}{DEFAULT_NEWLINE}"
    )


def bool_from_string(string: str) -> bool:
    """ Return boolean value readed from its string representation """
    string = string.lower()
    if string == 'true':
        return True
    elif string == 'false':
        return False
    else:
        raise ValueError(
            'Cannot make boolean value from string {string}'.format(string=string)
        )
