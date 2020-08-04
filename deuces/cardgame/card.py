from enum import Enum
from dataclasses import (
    dataclass,
)


class Suit(Enum):
    DIAMONDS = '♢'
    CLUBS = '♣'
    HEARTS = '♡'
    SPADES = '♠'


@dataclass
class Card:
    __slots__ = ['rank', 'suit']
    rank: str
    suit: Suit
