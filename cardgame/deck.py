from .card import Card


class Deck(set):
    @classmethod
    def make_deck(cls, ranks, suits):
        pass

    def __add__(self, other):
        if not isinstance(other, Card):
            raise TypeError("Can only add Cards to a Deck")
        return super.__add__(other)
