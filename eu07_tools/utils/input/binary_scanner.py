import struct

class BinaryScanner:
    def __init__(self, file):
        self._file = file
        self._calc_file_size()
        
# public:
    @property
    def is_empty(self):
        return self._file_size == self._file.tell()

    def read_bytes(self, size):
        return self._file.read(size)

    def read_int(self):
        bytes_ = self._file.read(4)
        return struct.unpack("i", bytes_)[0]

    def read_float(self):
        bytes_ = self._file.read(4)
        return struct.unpack("f", bytes_)[0]

    def read_str(self, size):
        bytes_ = self._file.read(size)
        fmt = f"{size}s"
        return struct.unpack(fmt, bytes_)[0].decode("utf-8")

# internal:
    def _calc_file_size(self):
        self._file.seek(0, 2)
        self._file_size = self._file.tell()
        self._file.seek(0, 0)