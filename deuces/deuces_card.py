from cardgame import Card
from cardgame.card import (Rank, Suit)

from typing import (
    Dict,
    List,
)


class DeucesCard(Card):
    RANK_ORDER: List[Rank] = list(
        map(lambda r: Rank(r), '3 4 5 6 7 8 9 T J Q K A 2'.split()))
    SUIT_ORDER: List[Suit] = [
        Suit.DIAMONDS, Suit.CLUBS, Suit.HEARTS, Suit.SPADES]
    RANK_TO_ORDER: Dict[Rank, int] = dict(
        (r, i) for i, r in enumerate(RANK_ORDER))
    SUIT_TO_ORDER: Dict[Suit, int] = dict(
        (s, i) for i, s in enumerate(SUIT_ORDER))

    def __init__(self, rank, suit):
        if rank not in DeucesCard.RANK_TO_ORDER.keys():
            raise TypeError('expected rank to be type string')
        if suit not in DeucesCard.SUIT_TO_ORDER.keys():
            raise TypeError('expected suit to be type Suit')
        super().__init__(rank, suit)

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

