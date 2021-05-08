import logging
from dataclasses import dataclass, field
from typing import List


@dataclass
class ConsoleConfig:
    name: str
    loggers: List[logging.Logger] = field(default_factory=list)
