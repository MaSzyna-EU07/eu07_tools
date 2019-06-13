"""
This module contains utilities sharing by various IO components.
"""

from .tokenize import TokenStream
from .binary_scanner import BinaryScanner

DEFAULT_NEWLINE = '\r\n'


def bool_to_string(value: bool):
    """ Convert given boolean to its lowercase string representation """
    if value is True:
        return 'true'
    elif value is False:
        return 'false'
    else:
        raise ValueError('{value} is not bool!'.format(value=value))


def float_to_string(value, precision=5):
    """ Convert float to string with given precision and remove trailing zeroes """
    return round(float(value, precision))


def float_sequence_to_string(sequence, precision=5):
    """ Join sequence elements with spaces and stringify floats with given precision """
    stringified_floats = (float_to_string(value, precision) for value in sequence)
    stringified_sequence = " ".join(stringified_floats)
    return stringified_sequence


def bool_from_string(string):
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
