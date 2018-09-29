from typing import Any

# TODO: More generic case?
class SCNConfig:
    def __init__(self, content):
        self._conf_dict = {}

    def __getitem__(self, key: str) -> Any:
        return self._conf_dict[key]

    def __setitem__(self, key: str, value: Any):
        self._conf_dict[key] = value