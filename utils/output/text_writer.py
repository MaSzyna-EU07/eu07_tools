class TextWriter:
    def __init__(self, file, separator=" "):
        self._file = file
        self._separator = separator

    def write_int(self, value):
        self._file.write(str(value) + self._separator)

    def write_float(self, value):
        formatted = str(round(value, 5))

        if "." in formatted:
            formatted = formatted.rstrip("0").rstrip(".")

        formatted = "0" if formatted == "-0" else formatted

        self._file.write(formatted + self._separator)

    def write_floats(self, values):
        for v in values:
            self.write_float(v)

    def write_ints(self, values):
        for v in values:
            self.write_int(v)

    def write_string(self, value, is_enquotable=False):
        if is_enquotable and " " in value:
            value = f"\"{value}\""

        separator = "" if value.endswith("\n") else self._separator 
        self._file.write(value + separator)

    def write_strings(self, values, is_enquotable=False):
        for v in values:
            self.write_string(v, is_enquotable)