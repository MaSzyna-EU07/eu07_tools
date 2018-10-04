from typing import Iterable, Union, Sequence

_FLOAT_PRECISION = 5


def format_sequence(seq: Iterable[object]) -> str:
    return " ".join(format_float(v) for v in seq)


def format_number(num: Union[float, int]) -> str:
    return str(round(num, FLOAT_PRECISION))


def format_matrix(matrix: Iterable[float]) -> str:
    return (
        "{newline}" + 
        "\t" + format_sequence(matrix[:4]) + "{newline}" +
        "\t" + format_sequence(matrix[4:8]) + "{newline}" +
        "\t" + format_sequence(matrix[8:12]) + "{newline}" +
        "\t" + format_sequence(matrix[12:])
    )


def format_geometry_unit(unit: Sequence[Union[int, Iterable[float]]]) -> str:
    return (
        str(unit[0]) + "{newline}" +
        "{newline}".join(
            format_sequence(vertex)
            for vertex in unit[1:]
        )
    )


def format_bool(value: bool) -> str:
    return "true" if value else "false"

