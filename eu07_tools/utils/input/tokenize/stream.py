from __future__ import annotations
from typing import Iterator, Pattern
from io import TextIOWrapper

from .tokenizer import Tokenizer
from .accessor import TokensAccessor


class TextScanner:
    """ This class provides API for extracting tokens from text data. """
    _tokenizer = Tokenizer()

    def __init__(self, accessor: TokensAccessor):
        self._accessor = accessor

    @classmethod
    def from_file(cls, stream: TextIOWrapper, read_comments: bool=False) -> TextScanner:
        """ Return new TokenStream instance with tokens readed from given file-like object. """
        tokens_iter = cls._tokenizer.tokenize_file(stream, read_comments)
        accessor = TokensAccessor(tokens_iter)
        return cls(accessor)
    
    def read_string(self):
        return self._accessor.get_token()

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

    def get_token(self) -> str:
        """ Return next token. 
        If there are no tokens in stream, an empty string will be returned.
        """
        return self._accessor.get_token()

    def get_tokens(self, amount: int) -> Iterator[str]:
        """ Return given amount of tokens. 
        If given amount is greater than total amount of tokens in stream, redundant tokens will be empty. 
        """
        return self._accessor.get_tokens(amount)

    def get_tokens_before(self, endmark: str) -> Iterator[str]:
        """ Return all tokens occuring before given endmark. 
        If endmark token not exists, this function will return all tokens until end of stream.
        """
        return self._accessor.get_tokens_before(endmark)

    @property
    def progress(self) -> int:
        """ Return approximated percentage progress of stream reading. """
        return self._tokenizer.progress

    @property
    def current_line_number(self) -> int:
        """ Return number of current processed line """
        return self._tokenizer.line_no

    def __iter__(self):
        return iter(self._accessor)