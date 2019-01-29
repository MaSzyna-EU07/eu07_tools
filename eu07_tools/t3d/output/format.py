_FLOAT_PRECISION = 5


def format_sequence(seq):
    return " ".join(format_number(v) for v in seq)


def format_number(num):
    formatted = str(round(num, _FLOAT_PRECISION))
    if formatted != "0":
        formatted = formatted.rstrip("0").rstrip(".")

    return formatted


def format_matrix(matrix):
    return (
        f"\n" + 
        f"\t{format_sequence(matrix[:4])}\n"
        f"\t{format_sequence(matrix[4:8])}\n"
        f"\t{format_sequence(matrix[8:12])}\n"
        f"\t{format_sequence(matrix[12:])}"
    )


def format_geometry_unit(unit):
    return (
        str(unit[0]) + "\n" +
        "\n".join(
            format_sequence(vertex)
            for vertex in unit[1:]
        ) + "\n\n"
    )


def format_bool(value):
    return "true" if value else "false"


def format_submodel_name(value):
    if " " in value:
        value = f"\"{value}\""

    return value