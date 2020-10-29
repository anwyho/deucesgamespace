from abc import ABC
from typing import (
    Callable,
    Dict,
    Optional,
    Tuple,
)

import deuces.validation as validation
from deuces import DeucesCard

MoveValidator = Callable[[Tuple[DeucesCard], Optional[Tuple[DeucesCard]]], bool]


class LogicalValidator(validation.BaseValidator, ABC):
    _MOVE_VALIDATOR_FACTORY: Optional[Dict[int, MoveValidator]] = None

    @staticmethod
    def is_valid_move(move: Tuple[DeucesCard], against: Optional[Tuple[DeucesCard]] = None) -> bool:
        move_size: int = len(move)
        if not (1 <= move_size <= 5):
            return False
        if against is not None and move_size != len(against):
            return False
        return LogicalValidator._move_validator_factory(move_size)(move, against)

    @staticmethod
    def _move_validator_factory(move_size: int) -> Dict[int, MoveValidator]:
        if LogicalValidator._MOVE_VALIDATOR_FACTORY is None:
            LogicalValidator._MOVE_VALIDATOR_FACTORY = {
                1: LogicalValidator._validate_one_card_move,
                2: LogicalValidator._validate_two_card_move,
                3: LogicalValidator._validate_three_card_move,
                4: LogicalValidator._validate_four_card_move,
                5: LogicalValidator._validate_five_card_move,
            }
        return LogicalValidator._MOVE_VALIDATOR_FACTORY[move_size]

    @staticmethod
    def _validate_one_card_move(move: Tuple[DeucesCard], against: Optional[Tuple[DeucesCard]] = None) -> bool:
        if against is None:
            return True
        return against[0] < move[0]

    @staticmethod
    def _validate_two_card_move(move: Tuple[DeucesCard], against: Optional[Tuple[DeucesCard]] = None) -> bool:
        if against is None:
            return move[0].rank == move[1].rank
        return (
            move[0].rank == move[1].rank and
            max(c.value for c in against) < max(c.value for c in move)
        )

    @staticmethod
    def _validate_three_card_move(move: Tuple[DeucesCard], against: Optional[Tuple[DeucesCard]] = None) -> bool:
        if against is None:
            return move[0].rank == move[1].rank == move[2].rank
        return (
            move[0].rank == move[1].rank == move[2].rank and
            against[0].rank < move[0].rank
        )

    @staticmethod
    def _validate_four_card_move(move: Tuple[DeucesCard], against: Optional[Tuple[DeucesCard]] = None) -> bool:
        if against is None:
            return move[0].rank == move[1].rank == move[2].rank == move[3].rank
        return (
            move[0].rank == move[1].rank == move[2].rank == move[3].rank and
            against[0].rank < move[0].rank
        )

    @staticmethod
    def _validate_five_card_move(move: Tuple[DeucesCard], against: Optional[Tuple[DeucesCard]] = None) -> bool:
        move_type = validation.combos.FiveCard.from_hand(move)
        if against is None:
            return not isinstance(move_type, validation.combos.InvalidFiveCardCombo)
        return validation.combos.FiveCard.from_hand(against) < move_type
