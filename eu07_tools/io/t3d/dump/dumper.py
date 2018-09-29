from typing import Any, Dict

from .common import TYPES_TO_KEYS
from maszyna_utils.io.utils import (
    float_sequence_to_string, float_to_string, bool_to_string
)


class T3DDumper:
    """
    Context manager for serializing T3D entries (submodels, includes).

    Usage:
    with T3DDumper('model.t3d') as dumper:
        context = {
            'Parent': 'none',
            'Type': 'Mesh',
            'Name': 'example',
            etc...
        }

        dumper.dump(context)
    """
    def __init__(self, file_path: str):
        self._file_path = file_path

    def __enter__(self):
        self._file = open(self._file_path, 'w')
        return self

    def __exit__(self, *args):
        self._file.close()

# -- Public Interface --

    def dump_submodel(self, context: Dict[str, Any]):
        """ Dump submodel with given context parameters """
        self._context = context

        self._write_separator()
        self._write_from_context('Parent')
        self._write_from_context('Type')
        self._write_from_context('Name')
        self._write_from_context('Anim')

        if self._context['Type'] == 'Mesh':
            self._write_from_context('Ambient')
            self._write_from_context('Diffuse')
            self._write_from_context('Specular')
            self._write_from_context('SelfIllum')
            self._write_from_context('Wire')
            self._write_from_context('WireSize')
            self._write_from_context('Opacity')
            self._write_from_context('Map')

        elif self._context['Type'] == 'FreeSpotLight':
            self._write_from_context('Diffuse')
            self._write_from_context('SelfIllum')
            self._write_from_context('NearAttenStart')
            self._write_from_context('NearAttenEnd')
            self._write_from_context('UseNearAtten')
            self._write_from_context('FarAttenDecayType')
            self._write_from_context('FarDecayRadius')
            self._write_from_context('FalloffAngle')
            self._write_from_context('HotspotAngle')

        elif self._context['Type'] == 'Stars':
            self._write_from_context('Diffuse')
            self._write_from_context('SelfIllum')

        self._write_from_context('MaxDistance')
        self._write_from_context('MinDistance')
        self._write_from_context('Transform')

        if 'vertex_groups' in self._context:
            self._write_from_context('NumVerts')
            self._write_vertex_groups()
        else:
            self._file.write('\r\n')

    def dump_include(self, file_path: str):
        """ Write 'include' command with provided file_path """
        self._file.write(
            'include {file_path} end\r\n'.format(
                file_path=file_path,
            )
        )

# -- Internals --

    def _write_separator(self):
        self._file.write(
            '//' + ('-' * 81) + '\r\n'
        )

    def _write_from_context(self, key: str):
        value = self._context[key]

        if key in TYPES_TO_KEYS['FLOAT']:
            value = float_to_string(value)

        elif key in TYPES_TO_KEYS['RGB']:
            value = float_sequence_to_string(value)

        elif key in TYPES_TO_KEYS['BOOL']:
            value = bool_to_string(value)

        elif key in TYPES_TO_KEYS['MATRIX']:
            # Matrix should be on the next line
            value = '\r\n\t' + '\r\n\t'.join(
                float_sequence_to_string(row) for row in value
            )

        elif key in TYPES_TO_KEYS['UNION']:
            try:
                value = bool_to_string(value)
            except ValueError:
                value = float_to_string(value)

        self._file.write(
            f'{key}: {value}\r\n'
        )

    def _write_vertex_groups(self):
        for vert_group in self._context['vertex_groups']:
            smooth = str(vert_group[0]) + '\r\n'

            verts = vert_group[1:]
            verts_str = '\r\n'.join(
                float_sequence_to_string(vert) for vert in verts
            )

            self._file.write(
                smooth + verts_str + '\r\n\r\n'
            )
