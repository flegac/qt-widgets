from dataclasses import dataclass
from typing import Tuple, List, TypeVar, Optional

T = TypeVar('T')


@dataclass
class Item:
    width: Optional[int] = None


@dataclass
class Page:
    index: int = 0
    size: int = 100

    def range(self, index: int = None) -> Tuple[int, int]:
        if index is None:
            index = self.index
        start = index * self.size
        end = start + self.size
        return start, end

    def select(self, model: List[T], index: int):
        first, last = self.range(index)
        return model[first:last]


@dataclass
class BrowserConfig:
    item: Item = Item()
    page: Page = Page()
