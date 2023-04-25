from typing import List
from dataclasses import dataclass
from abc import ABCMeta, abstractproperty

class StateBase(metaclass=ABCMeta):
    def __init__(self, _id: int, is_consuming: bool = True) -> None: 
        self._id = _id
        self.is_consuming = is_consuming
    
    @abstractproperty
    def is_accepting(self) -> bool:
        ...

    @abstractproperty
    def is_error(self) -> bool:
        ...


class AcceptingState(StateBase):
    @property
    def is_accepting(self) -> bool:
        return True

    @property
    def is_error(self) -> bool:
        return False

class ErrorState(StateBase):
    @property
    def is_accepting(self) -> bool:
        return False

    @property
    def is_error(self) -> bool:
        return True



# TODO change to frozen list
class TransitionTable(list):
    ...