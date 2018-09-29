from typing import Dict, Iterable, Iterator, Pattern
from io import TextIOWrapper, BufferedReader, BytesIO
import re
import math


def _get_stream_size(stream: TextIOWrapper) -> int:
    stream.seek(0, 2)
    stream_size = stream.tell()
    stream.seek(0)
    return stream_size


_DEFAULT_SEPARATORS = [" ", "\t", ";", ","]


class Tokenizer:

    class DelimitationData:
        def __init__(self, opening: str, closing: str, return_: bool=False, keep_delimiters: bool=True):
            self.opening = opening
            self.closing = closing
            self.re_opening = re.compile(re.escape(opening))
            self.re_closing = re.compile(re.escape(closing))
            self.return_ = return_
            self.keep_delimiters = keep_delimiters

    def __init__(self, return_comments=False, separators=_DEFAULT_SEPARATORS):
        self.line_no: int = 0

        self._file: TextIOWrapper = None
        self._stream_size: int = 0
        self._readed_stream_size: int = 0

        sep_pat = r"".join(re.escape(sep) for sep in separators)
        self._re_separators: Pattern = re.compile(r"[" + sep_pat + r"]+")
        self._re_opening_delimiters: Pattern = re.compile(r"//|/\*|\"")

        # TODO: Delimiters registration
        self._delimiters_map: Dict[str, self.DelimitationData] = {
            "//": self.DelimitationData("//", "\n", return_=return_comments),
            "/*": self.DelimitationData("/*", "*/", return_=return_comments),
            "\"": self.DelimitationData("\"", "\"", return_=True, keep_delimiters=False)
        }
        
    # public:
    def tokenize_file(self, stream: TextIOWrapper, ignore_comments=True):
        self.line_no = 1
        self._stream = stream
        self._stream_size = _get_stream_size(self._stream)
        # HACK: In default, input file stream converts all crlf/cr to lf. 
        # It causes that the desirable result of len(line) (where line ends with crlf) is less by 1.
        # So we need to disable this behaviour to provide correct progress calculation.
        # In this case newline conversion is performed explicitly for each line with string.replace().
        self._stream.reconfigure(newline="")

        return self._get_tokens_generator()

    def tokenize_string(self, string: str) -> Iterator[str]:
        return self.tokenize_file(TextIOWrapper(BufferedReader(BytesIO(string.encode()))))
        
    @property
    def progress(self) -> int:
        return round((self._readed_stream_size / self._stream_size) * 100, ndigits=2)
                
    # internal:
    def _get_tokens_generator(self):
        # TODO: CQS destroyed here, should be fixed
        for self.line_no, line in enumerate(self._stream, start=1):
            line_size = len(line)
            line = line.replace("\r\n", "\n").replace("\r", "\n")
            yield from self._tokenize_string(line)
            self._readed_stream_size += line_size

    def _tokenize_string(self, string: str) -> Iterator[str]:
        delimiter_match = re.search(self._re_opening_delimiters, string)

        if delimiter_match:
            yield from self._handle_delimited_tokens(delimiter_match.group(0), string)
        else:
            string = string.rstrip("\n")
            for token in re.split(self._re_separators, string):

                if token != "":
                    yield token
            

    def _handle_delimited_tokens(self, opening: str, string: str) -> Iterator[str]:
        delim_data = self._delimiters_map[opening]

        non_delimited_part, string = re.split(delim_data.re_opening, string, maxsplit=1)

        yield from self._tokenize_string(non_delimited_part)

        try:
            line = string  # Cache line to gain speed while looking for closing delimiter
            while delim_data.closing not in line:
                line = next(self._stream)
                self.line_no + 1
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