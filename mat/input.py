from .structures import create_material, MATMaterial, MATTextureValue
from .common import VARIANT_KEYS, FLOAT_KEYS, STRING_KEYS, INT_KEYS
from eu07_tools.utils import TextScanner, TexturePath


def load(file):
    scanner = TextScanner.from_file(file)
    return _load_material(scanner)


def _load_material(scanner):
    mat = MATMaterial()

    while True:
        token = scanner.read_string()
        key = token.rstrip(":")

        if not token:
            break
        elif key == "{":
            continue
        elif key == "}":
            break

        elif "texture" in key:
            token = scanner.read_string()

            if token == "[":
                value = MATTextureValue.from_list([
                    TexturePath(p) for p in
                    scanner.read_strings_before("]")
                ])

            else:
                value = MATTextureValue.from_path(TexturePath(token))

        elif key in VARIANT_KEYS:
            value = _load_material(scanner)

        elif key in STRING_KEYS:
            value = scanner.read_string()

        elif key in FLOAT_KEYS:
            value = scanner.read_float()

        elif key in INT_KEYS:
            value = scanner.read_int()

        elif key == "size":
            value = scanner.read_floats(2)

        elif key.startswith("param"):
            values = []
            while 1:
                token = scanner.read_string()
                try:
                    pv = float(token)
                except ValueError:
                    scanner.put_back(token)
                    break
                else:
                    values.append(pv)

            value = values

        mat[key] = value

    return mat