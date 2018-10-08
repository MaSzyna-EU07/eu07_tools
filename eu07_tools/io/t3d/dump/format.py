from typing import Iterable, Union, Sequence

_FLOAT_PRECISION = 5


def format_sequence(seq: Iterable[object]) -> str:
    return " ".join(format_number(v) for v in seq)


def format_number(num: Union[float, int]) -> str:
    formatted = str(round(num, _FLOAT_PRECISION))
    if formatted != "0":
        formatted = formatted.rstrip("0").rstrip(".")

    return formatted


def format_matrix(matrix: Iterable[float]) -> str:
    return (
        f"\n" + 
        f"\t{format_sequence(matrix[:4])}\n"
        f"\t{format_sequence(matrix[4:8])}\n"
        f"\t{format_sequence(matrix[8:12])}\n"
        f"\t{format_sequence(matrix[12:])}"
    )


def format_geometry_unit(unit: Sequence[Union[int, Iterable[float]]]) -> str:
    return (
        str(unit[0]) + "\n" +
        "\n".join(
            format_sequence(vertex)
            for vertex in unit[1:]
        ) + "\n\n"
    )


def format_bool(value: bool) -> str:
    return "true" if value else "false"

