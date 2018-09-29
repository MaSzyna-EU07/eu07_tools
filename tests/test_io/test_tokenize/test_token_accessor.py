import pytest
from pytest import raises

from eu07_tools.io.utils.tokenize import TokensAccessor


class Test_get_token:
    def test_when_stream_has_tokens(self):
        stream = TokensAccessor(
            iter(["foo", "bar", "baz"])
        )

        assert stream.get_token() == "foo"
        assert stream.get_token() == "bar"
        assert stream.get_token() == "baz"

    def test_when_stream_is_exhausted(self):
        stream = TokensAccessor(iter([]))

        assert stream.get_token() == ""


class Test_get_tokens:
    def test_when_stream_has_tokens(self):
        stream = TokensAccessor(
            iter(["foo", "bar", "baz"])
        )

        assert list(stream.get_tokens(3)) == ["foo", "bar", "baz"]

    def test_when_stream_is_exhausted(self):
        stream = TokensAccessor(iter([]))

        assert list(stream.get_tokens(3)) == ["", "", ""]

    def test_when_stream_gets_exhausted_during_call(self):
        stream = TokensAccessor(
            iter(["foo", "bar", "baz"])
        )

        assert list(stream.get_tokens(5)) == ["foo", "bar", "baz", "", ""]


class Test_get_tokens_before:
    def test_when_stream_has_tokens(self):
        stream = TokensAccessor(
            iter(["foo", "bar", "baz", "quz", "quux"])
        )

        assert list(stream.get_tokens_before("quz")) == ["foo", "bar", "baz"]

    def test_when_stream_is_exhausted(self):
        stream = TokensAccessor(iter([]))

        assert list(stream.get_tokens_before("quz")) == [] 

    def test_when_stream_gets_exhausted_during_call(self):
        stream = TokensAccessor(
            iter(["foo", "bar", "baz"])
        )

        assert list(stream.get_tokens_before("quz")) == ["foo", "bar", "baz"]

       