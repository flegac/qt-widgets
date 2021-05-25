from dataclasses import dataclass
from typing import Tuple, List, TypeVar

T = TypeVar('T')


@dataclass
class BrowserConfig:
    index: int = 0
    item_per_line: int = 1
    item_per_page: int = 1
    tool_bar: bool = True
    transpose_grid: bool = False  # TODO: transpose orientation

    def range(self, index: int = None) -> Tuple[int, int]:
        if index is None:
            index = self.index
        start = index * self.item_per_page
        end = start + self.item_per_page
        return start, end

    def select(self, model: List[T], index: int):
        try:
            first, last = self.range(index)
            return model[first:last]
        except:
            return []
