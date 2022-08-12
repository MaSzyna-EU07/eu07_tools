DEFAULT_SEPARATORS = [" ", "\t", ";", ","]

class TextScanner:
    @classmethod
    def from_file(cls, file, tokenizer=None):
        return cls(file, tokenizer)

    def __init__(self, file, tokenizer=None):
        self._tokenizer = tokenizer
        if not self._tokenizer:
            self._tokenizer = Tokenizer()
        self._tokenizer.tokenize_file(file)
        self._back_tokens = []

    def read_string(self):
        if self._back_tokens:
            return self._back_tokens.pop(0)
        return self._tokenizer.get_token()

    def read_float(self):
        return float(self.read_string())

    def read_int(self):
        return int(self.read_string())

    def read_strings(self, amount):
        return [self.read_string() for _ in range(amount)]

    def read_floats(self, amount):
        return [self.read_float() for _ in range(amount)]

    def read_ints(self, amount):
        return [self.read_int() for _ in range(amount)]

    def read_strings_before(self, endmark):
        tokens = []
        
        while True:
            token = self.read_string()

            if (token == endmark or token == ""):
                return tokens

            tokens.append(token)

        return tokens


    def read_ints_before(self, endmark):
        return [int(x) for x in self.read_strings_before(endmark)]

    def read_floats_before(self, endmark):
        return [float(x) for x in self.read_strings_before(endmark)]

    def put_back(self, token):
        self._back_tokens.append(str(token))

    @property
    def line_number(self):
        return self._tokenizer.line_no

    @property
    def filename(self):
        return self._tokenizer.filename



# Ugly legacy code written long time ago, might be refactored later,
# it must work because all inputs rely on this tokenizer
from io import TextIOWrapper, BufferedReader, BytesIO, TextIOBase
import re
import math


def get_stream_size(stream: TextIOBase):
    stream.seek(0, 2)
    stream_size = stream.tell()
    stream.seek(0)
    return stream_size


class Tokenizer:

    class DelimitationData:
        def __init__(self, opening, closing, return_=False, keep_delimiters=True):
            self.opening = opening
            self.closing = closing
            self.re_opening = re.compile(re.escape(opening))
            self.re_closing = re.compile(re.escape(closing))
            self.return_ = return_
            self.keep_delimiters = keep_delimiters

    def __init__(self, return_comments=False, separators=DEFAULT_SEPARATORS, parameters=None):
        self.line_no = 0
        self._parameters = parameters

        self._stream_size = 0
        self._readed_stream_size = 0

        sep_pat = r"".join(re.escape(sep) for sep in separators)
        self._re_separators = re.compile(r"[" + sep_pat + r"]+")
        self._re_opening_delimiters = re.compile(r"//|/\*|\"")

        self._tokens_iterator = None

        # TODO: Delimiters registration
        self._delimiters_map  = {
            "//": self.DelimitationData("//", "\n", return_=return_comments),
            "/*": self.DelimitationData("/*", "*/", return_=return_comments),
            "\"": self.DelimitationData("\"", "\"", return_=True, keep_delimiters=False)
        }
        
    # public:
    def get_token(self):
        try:
            return next(self._tokens_iterator)
        except StopIteration:
            return ""

    def get_tokens(self, amount):
        return (self.get_token() for _ in range(amount))

    def __iter__(self):
        return self._tokens_iterator

    def tokenize_file(self, stream, ignore_comments=True):
        self.line_no = 1
        self._stream = stream
        self._stream_size = get_stream_size(self._stream)
        # HACK: In default, input file stream converts all crlf/cr to lf. 
        # It causes that the desirable result of len(line) (where line ends with crlf) is less by 1.
        # So we need to disable this behaviour to provide correct progress calculation.
        # In this case newline conversion is performed explicitly for each line with string.replace().
        self._stream.reconfigure(newline="")

        self._tokens_iterator = self._get_tokens_generator()

    def tokenize_string(self, string):
        return self.tokenize_file(TextIOWrapper(BufferedReader(BytesIO(string.encode()))))

    @property
    def progress(self):
        return round((self._readed_stream_size / self._stream_size) * 100, ndigits=2)

    @property
    def filename(self):
        return self._stream.name
                
    # internal:
    def _get_tokens_generator(self):
        # TODO: CQS destroyed here, should be fixed
        for self.line_no, line in enumerate(self._stream, start=1):
            line_size = len(line)
            line = line.replace("\r\n", "\n").replace("\r", "\n")
            yield from self._tokenize_string(line)
            self._readed_stream_size += line_size

    def _tokenize_string(self, string):
        delimiter_match = re.search(self._re_opening_delimiters, string)

        if delimiter_match:
            yield from self._handle_delimited_tokens(delimiter_match.group(0), string)
        else:
            string = string.rstrip("\n")
            for token in re.split(self._re_separators, string):

                if token != "":
                    yield token
            

    def _handle_delimited_tokens(self, opening, string):
        delim_data = self._delimiters_map[opening]

        non_delimited_part, string = re.split(delim_data.re_opening, string, maxsplit=1)

        yield from self._tokenize_string(non_delimited_part)

        try:
            line = string  # Cache line to gain speed while looking for closing delimiter
            while delim_data.closing not in line:
                line = next(self._stream)
                self.line_no += 1
                string += line
                
        except StopIteration:
            pass
        else:
            delimitation, non_delimited_part = re.split(delim_data.re_closing, string, maxsplit=1)
        
            if delim_data.return_:
                if delim_data.keep_delimiters:
                    delimitation = delim_data.opening + delimitation + delim_data.closing
                    print(delimitation)
                yield delimitation

            yield from self._tokenize_string(non_delimited_part)