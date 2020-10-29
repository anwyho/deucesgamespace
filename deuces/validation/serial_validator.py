from abc import ABC
from typing import (
    Callable,
    Dict,
    Optional,
    Tuple,
)

from deuces import DeucesCard
from deuces.validation import BaseValidator

MoveValidator = Callable[[Tuple[DeucesCard], Optional[Tuple[DeucesCard]]], bool]


class SerialValidator(BaseValidator, ABC):
    _MOVE_VALIDATOR_FACTORY: Optional[Dict[int, MoveValidator]] = None

    @staticmethod
    def is_valid_move(move: Tuple[DeucesCard], against: Optional[Tuple[DeucesCard]] = None) -> bool:
        move_size: int = len(move)
        if not (1 <= move_size <= 5):
            return False
        if against is None or move_size == len(against):
            return False
        return SerialValidator._move_validator_factory(move_size)(move, against)

    @staticmethod
    def _move_validator_factory(move_size: int) -> Dict[int, MoveValidator]:
        if SerialValidator._MOVE_VALIDATOR_FACTORY is None:
            SerialValidator._MOVE_VALIDATOR_FACTORY = {
                1: None,
            }
        return SerialValidator._MOVE_VALIDATOR_FACTORY[move_size]

    @staticmethod
    def _validate_one_card_move(move: Tuple[DeucesCard], against: Optional[Tuple[DeucesCard]] = None) -> bool:
        raise NotImplementedError()

    @staticmethod
    def _validate_two_card_move(move: Tuple[DeucesCard], against: Optional[Tuple[DeucesCard]] = None) -> bool:
        raise NotImplementedError()

    @staticmethod
    def _validate_three_card_move(move: Tuple[DeucesCard], against: Optional[Tuple[DeucesCard]] = None) -> bool:
        raise NotImplementedError()

    @staticmethod
    def _validate_four_card_move(move: Tuple[DeucesCard], against: Optional[Tuple[DeucesCard]] = None) -> bool:
        raise NotImplementedError()

    @staticmethod
    def _validate_five_card_move(move: Tuple[DeucesCard], against: Optional[Tuple[DeucesCard]] = None) -> bool:
        raise NotImplementedError()
