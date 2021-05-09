from enum import Enum, auto


class WorkerStatus(Enum):
    started = auto()
    finished = auto()