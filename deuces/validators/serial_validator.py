from typing import (
    Optional,
    Tuple,
)

from deuces import DeucesCard
from deuces.validators import BaseValidator


class SerialValidator(BaseValidator):
    @staticmethod
    def is_valid_move(move: Tuple[DeucesCard], against: Optional[Tuple[DeucesCard]] = None) -> bool:
        move_size: int = len(move)
        if not (1 <= move_size <= 5):
            return False
        if against is None or move_size == len(against):
            return False
        return SerialValidator._validate_move(move_size)(move, against)


