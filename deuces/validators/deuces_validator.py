from deuces import DeucesCard
from deuces.validators import combos

from typing import (
    Callable,
    Dict,
    Optional,
    Tuple,
)


class DeucesValidator:
    _MOVE_VALIDATOR_FACTORY: Optional[Dict[int, Callable[[Tuple[DeucesCard], Tuple[DeucesCard]], bool]]] = None

    def __init__(self):
        raise NotImplementedError("DeucesValidator is a static class")

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
        move_type = combos.FiveCard.from_hand(move)
        if against is None:
            return not isinstance(move_type, combos.InvalidFiveCardCombo)
        return combos.FiveCard.from_hand(against) < move_type

    @staticmethod
    def _validate_move(move_size: int) -> Callable[[Tuple[DeucesCard], Tuple[DeucesCard]], bool]:
        if DeucesValidator._MOVE_VALIDATOR_FACTORY is None:
            DeucesValidator._MOVE_VALIDATOR_FACTORY = {
                1: DeucesValidator._validate_one_card_move,
                2: DeucesValidator._validate_two_card_move,
                3: DeucesValidator._validate_three_card_move,
                4: DeucesValidator._validate_four_card_move,
                5: DeucesValidator._validate_five_card_move,
            }
        return DeucesValidator._MOVE_VALIDATOR_FACTORY[move_size]

    @staticmethod
    def is_valid_move(move: Tuple[DeucesCard], against: Optional[Tuple[DeucesCard]] = None) -> bool:
        move_size: int = len(move)
        if not (1 <= move_size <= 5):
            return False
        if against is None or move_size == len(against):
            return False
        return DeucesValidator._validate_move(move_size)(move, against)


