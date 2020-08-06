from cardgame import (
    Game,
)

from . import (
    DeucesCard as Card,
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
