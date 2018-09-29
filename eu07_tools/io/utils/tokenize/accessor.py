from typing import Iterable, Iterator


class TokensAccessor:
    def __init__(self, tokens: Iterable[str]):
        self._tokens_iterator = iter(tokens)

    def get_token(self) -> str:
        try:
            return next(self._tokens_iterator)
        except StopIteration:
            return ""

    def get_tokens(self, amount: int) -> Iterator[str]:
        return (self.get_token() for _ in range(amount))

    def get_tokens_before(self, endmark: str) -> Iterator[str]:
        for token in self._tokens_iterator:
            if token == endmark:
                break

            yield token

        return iter([])
    
    def __iter__(self):
        return self._tokens_iterator