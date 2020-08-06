import functools

from collections import defaultdict
from typing import (
    Dict,
    List,
    Tuple,
)

from cardgame.card import (Rank, Suit)
from deuces import DeucesCard
from deuces.validators.combos import ComboType


class FiveCard(ComboType):
    @classmethod
    @functools.lru_cache()
    def from_hand(cls, cards: Tuple[DeucesCard]):
        # Straight
        #   Five consecutive cards
        #   Straight ending on Ace is highest
        #   Straight ending on five is lowest
        #   Straights cannot end on two through four

        # Flush
        #   Five cards of the same suit

        # Straight Flush / Royal Flush
        #   Five consecutive cards of the same suit
        #   Royal Flush is a Straight Flush that ends on an Ace
        rank_hist = defaultdict(int)
        suit_hist = defaultdict(int)
        combo_repeated_rank = None
        for card in cards:
            rank_hist[card.rank] += 1
            suit_hist[card.suit] += 1
            if rank_hist[card.rank] >= 3:
                combo_repeated_rank = card.rank
        max_rank_repeats = max(rank_hist.values())
        max_suit_repeats = max(suit_hist.values())

        # Four of a Kind, Full House
        if combo_repeated_rank is not None:
            if max_rank_repeats == 4:
                return FourOfAKind(rank_ix=DeucesCard.RANK_TO_ORDER[combo_repeated_rank])
            if max_rank_repeats == 3:
                if min(rank_hist.values()) == 2:
                    return FullHouse(rank_ix=DeucesCard.RANK_TO_ORDER[combo_repeated_rank])
                else:
                    return InvalidFiveCard()

        # Straight, Flush, Straight Flush / Royal Flush
        else:
            is_straight = False
            is_flush = (max_suit_repeats == 5)
            suit_ix = None
            end_rank_ix = None
            end_rank_suit_ix = None

            sorted_cards = list(sorted(cards, key=lambda c: c.value))
            rank_ixs = list(sorted(cards, key=lambda c: DeucesCard.RANK_TO_ORDER[c.rank]))
            # ILLEGAL: 8 9 10 11 12 - ends on a Rank.TWO (12)
            # LEGAL: 0 1 2 11 12 - ends on a Rank.FIVE (2)
            # LEGAL: 0 1 2 3 12 - ends on a Rank.SIX (3)
            for c in sorted_cards:
                pass

            if is_flush:
                # TODO: Do I want cards[0] or cards[-1]
                suit_ix = DeucesCard.SUIT_TO_ORDER[cards[0].suit]
                end_rank_ix = DeucesCard.RANK_TO_ORDER[sorted_cards[0].rank]

            # Generate remaining FiveCard Combos
            if is_flush and is_straight:
                return StraightFlush(end_rank_ix=end_rank_ix, suit_ix=suit_ix)
            if is_flush:
                return Flush(suit_ix=suit_ix, end_rank_ix=end_rank_ix)
            elif is_straight:
                return Straight(end_rank_ix=end_rank_ix, end_rank_suit_ix=end_rank_suit_ix)
            else:
                return InvalidFiveCard()

    def __lt__(self, other):
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
        self_combo_ix = FIVE_CARD_COMBO_TO_ORDER[self.__class__]
        other_combo_ix = FIVE_CARD_COMBO_TO_ORDER[other.__class__]
        if self_combo_ix != other_combo_ix:
            return self_combo_ix < other_combo_ix
        # Dataclasses are constructed so that when compared against themselves,
        #   they will properly order themselves.
        return self < other


class InvalidFiveCard(FiveCard):
    pass


class Straight(FiveCard):
    # Compare the end card's rank
    end_rank_ix: int
    # Then compare the tie's suit
    end_rank_suit_ix: int


class Flush(FiveCard):
    # Compare the suit
    suit_ix: int
    # Then compare the tie's end card's rank
    end_rank_ix: int


class FullHouse(FiveCard):
    # Compare the three-of-a-kind's rank
    rank_ix: int


class FourOfAKind(FiveCard):
    # Compare the four-of-a-kind's rank
    rank_ix: int


class StraightFlush(FiveCard):
    # Compare the end card's rank
    end_rank_ix: int
    # Then compare the tie's suit
    suit_ix: int


FIVE_CARD_COMBO_ORDER: List[FiveCard] = [InvalidFiveCard, Straight, Flush, FullHouse, FourOfAKind, StraightFlush]
FIVE_CARD_COMBO_TO_ORDER: Dict[FiveCard, int] = dict((f, i) for i, f in enumerate(FIVE_CARD_COMBO_ORDER))

