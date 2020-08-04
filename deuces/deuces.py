
from typing import (
    Callable,
    Dict,
    List,
    Set,
)

from .cardgame import (
    Deck,
    Game,
)

from .deuces_utility import (
    DeucesCard as Card,
    DeucesUtility as util,
)



class Deuces(Game):
    def __init__(self):
        pass

    @staticmethod
    def card_value(c: Card):
        return c.rank*c.suit + c.suit

    @staticmethod
    def compare(a: Card, b: Card):
        pass
