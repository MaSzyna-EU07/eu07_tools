from typing import Iterator, List
import os
from dataclasses import dataclass

class SearcherConfig:
    def __init__(self, root, lookup_paths, extensions):
        self.root: str = root
        self.lookup_paths: List[str] = lookup_paths
        self.extensions: List[str] = extensions



class FileSearcher:
    def __init__(self, config=None):
        self.config = config


    def find_existing_paths(self, relpath: str) -> Iterator[str]:
        relpath = os.path.splitext(relpath)[0]
        relpath = os.path.normpath(relpath.replace('\\', '/')).lstrip('/').lower()

        for lookup_path in self.strategy.lookup_paths:
            file_path = os.path.join(lookup_path, relpath)

            for extension in self.strategy.extensions:
                full_path = ".".join((file_path, extension))

                if os.path.exists(full_path):
                    yield full_path

        return None




