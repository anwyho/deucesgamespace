from enum import Enum
from dataclasses import (
    dataclass,
)


class Suit(Enum):
    DIAMONDS = '♢'
    CLUBS    = '♣'
    HEARTS   = '♡'
    SPADES   = '♠'


class Rank(Enum):
    ACE   = 'A'
    TWO   = '2'
    THREE = '3'
    FOUR  = '4'
    FIVE  = '5'
    SIX   = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE  = '9'
    TEN   = 'T'
    JACK  = 'J'
    QUEEN = 'Q'
    KING  = 'K'


@dataclass
class Card:
    # __slots__ = ['rank', 'suit']
    rank: Rank
    suit: Suit

    def __repr__(self):
        return f"{self.rank.value}{self.suit.value}"

