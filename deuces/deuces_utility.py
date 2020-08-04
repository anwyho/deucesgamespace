from .cardgame import Card
from .cardgame.card import Suit
# from .cardgame import Deck

from typing import (
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
)


class DeucesCard(Card):
    RANK_ORDER: List[str] = '3 4 5 6 7 8 9 10 J Q K A 2'.split()
    SUIT_ORDER: List[Suit] = [Suit.DIAMONDS, Suit.CLUBS, Suit.HEARTS, Suit.SPADES]
    RANK_TO_ORDER: Dict[str, int] = dict((r, i) for i, r in enumerate(RANK_ORDER))
    SUIT_TO_ORDER: Dict[Suit, int] = dict((s, i) for i, s in enumerate(SUIT_ORDER))

    def __repr__(self):
        return f"{self.rank}{self.suit.value}"

    def __gt__(self, other):
        return other.value < self.value

    def __lt__(self, other):
        return self.value < other.value

    def __ge__(self, other):
        return other.value <= self.value

    def __le__(self, other):
        return self.value <= other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    @property
    def value(self):
        rank_val = DeucesCard.RANK_TO_ORDER[self.rank]
        suit_val = DeucesCard.SUIT_TO_ORDER[self.suit]
        return (rank_val * len(DeucesCard.SUIT_ORDER)) + suit_val

    @classmethod
    def from_value(cls, value: int):
        return cls(
            rank=DeucesCard.RANK_ORDER[value // len(DeucesCard.SUIT_ORDER)],
            suit=DeucesCard.SUIT_ORDER[value % len(DeucesCard.SUIT_ORDER)],
        )


class DeucesValidator:
    _MOVE_VALIDATOR_FACTORY: Optional[Dict[int, Callable[[Tuple[DeucesCard], Tuple[DeucesCard]], bool]]] = None

    def __init__(self):
        raise NotImplementedError("DeucesValidator is a static class")

    @staticmethod
    def _validate_one_card_move(against: Tuple[DeucesCard], move: Tuple[DeucesCard]) -> bool:
        return against[0] < move[0]

    @staticmethod
    def _validate_two_card_move(against: Tuple[DeucesCard], move: Tuple[DeucesCard]) -> bool:
        return (
            move[0].rank == move[1].rank and
            max(c.value for c in against) < max(c.value for c in move)
        )

    @staticmethod
    def _validate_three_card_move(against: Tuple[DeucesCard], move: Tuple[DeucesCard]) -> bool:
        return (
            move[0].rank == move[1].rank == move[2].rank and
            against[0].rank < move[0].rank
        )

    @staticmethod
    def _validate_four_card_move(against: Tuple[DeucesCard], move: Tuple[DeucesCard]) -> bool:
        return (
                move[0].rank == move[1].rank == move[2].rank == move[3].rank and
                against[0].rank < move[0].rank
        )

    @staticmethod
    def _validate_five_card_move(against: Tuple[DeucesCard], move: Tuple[DeucesCard]) -> bool:
        # TODO: Type of five card move
        # TODO: Type of five card against
        # Straight
        #   Five consecutive cards
        #   Straight ending on Ace is highest
        #   Straight ending on five is lowest
        #   Straights cannot end on two through four
        # Flush
        #   Five cards of the same suit
        # Full House
        #   A three-of-a-kind and a pair
        # Four of a Kind
        #   A four-of-a-kind and a single card
        # Straight Flush / Royal Flush
        #   Five consecutive cards of the same suit
        #   Royal Flush is a Straight Flush that ends on an Ace

        # TODO: Compare against move
        # Straight
        #   Compare rank of ending card
        #   Ties compare suit
        # Flush
        #   Compare rank of cards unless all cards are equal ranked
        #   Ties compare suit
        # Full House
        #   Compare rank of the three-of-a-kind
        # Four of a Kind
        #   Compare rank of the four-of-a-kind
        # Straight Flush / Royal Flush
        #   See Straight comparisons
        pass

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
    def is_valid_move(against: Tuple[DeucesCard], move: Tuple[DeucesCard]) -> bool:
        move_size: int = len(against)
        if len(move) != move_size or not (0 < move_size <= 5):
            return False
        return DeucesValidator._validate_move(move_size)(against, move)
