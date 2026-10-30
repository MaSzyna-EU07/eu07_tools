import re

# a parameter of an included file, (p1), (p2) ...
PARAMETER_PATTERN = re.compile(r"\(p(\d+)\)", re.IGNORECASE)


def has_parameters(token):
    """ Whether the token holds a parameter of an included file, (pN) """
    return PARAMETER_PATTERN.search(token) is not None


def substitute_parameters(token, parameters):
    """ The token with its parameters (pN) replaced by the values the include gives them, as the simulator does: a
    parameter the include doesn't give becomes "none". Without any parameters the token stays as it is """
    if not parameters:
        return token

    def replace(match):
        index = int(match.group(1))
        return str(parameters[index - 1]) if 1 <= index <= len(parameters) else "none"

    return PARAMETER_PATTERN.sub(replace, token)
