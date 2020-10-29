from abc import ABC, abstractmethod
from typing import (
    Optional,
    Tuple,
)

from deuces import DeucesCard


class BaseValidator(ABC):
    def __init__(self):
        raise NotImplementedError(f"{self.__class__.__name__} is an abstract class")

    @staticmethod
    @abstractmethod
    def is_valid_move(move: Tuple[DeucesCard], against: Optional[Tuple[DeucesCard]] = None) -> bool:
        NotImplementedError("is_valid_move must be implemented by a subclass")


