import struct

class BinaryWriter:
    def __init__(self, file):
        self._file = file

    # TODO: Ensure if it is correct way to pad
    def write_bytes(self, bytes_):
        self._file.write(bytes_)

    def write_int(self, value):
        binary = struct.pack("i", value)
        self._file.write(binary)

    def write_float(self, value):
        binary = struct.pack("f", value)
        self._file.write(binary)

    def write_floats(self, values):
        binary = struct.pack(f"{len(values)}f", *values)
        self._file.write(binary)

    def write_string(self, value):
        binary = struct.pack(f"{len(value)}s", value.encode("utf-8"))
        self._file.write(binary)
