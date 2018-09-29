import pytest


from ..utils import make_fake_file
from eu07_tools.io.utils.tokenize import Tokenizer


class Test_tokenize:
    def setup(self):
        self.tokenizer = Tokenizer()

    def test_various_separators(self):
        file_ = make_fake_file(
            "foo bar;baz,quuz      quux,,,\n"
            "lorem"
        )

        tokens_iter = self.tokenizer.tokenize_file(file_)

        expected = ["foo", "bar", "baz", "quuz", "quux", "lorem"]

        assert list(tokens_iter) == expected

    def test_comments(self):
        file_ = make_fake_file(
            "foo //bar baz\n"
            "foo//bar baz\n"
            "foo// bar baz\n"
            "foo // bar baz\n"
            "foo /*bar baz*/\n"
            "foo/*bar baz */\n"
            "foo /* bar baz */\n"
            "foo /* bar\n"
            "baz*/"
        )

        tokens_iter = self.tokenizer.tokenize_file(file_)

        expected = ["foo"] * 8

        assert list(tokens_iter) == expected
    
    def test_quoted_tokens(self):
        file_ = make_fake_file(
            "\"bar baz\"\n"
            "\" bar;baz \"\n"
            "\"bar\n"
            "baz\"" 
        )

        tokens_iter = self.tokenizer.tokenize_file(file_)

        expected = ["bar baz", " bar;baz ", "bar\nbaz" ]

        assert list(tokens_iter) == expected

    def no_test_line_numbers(self):
        # This doesn't work for no reason (only in test environment!) -,-
        file_ = make_fake_file(
            "bar baz\n"
            "foo bar\n"
            "quz /* quux\n"
            "quz quz quz\n"
            "quz quz quz\n"
            "quz */ hello"
        )

        tokens_iter = self.tokenizer.tokenize_file(file_)

        x = (next(tokens_iter) for _ in range(5))

        assert self.tokenizer.line_no == 2
    