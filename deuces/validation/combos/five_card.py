import functools

from collections import defaultdict
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
)

from cardgame.card import (Rank, Suit)
from deuces import DeucesCard
from deuces.validation.combos import ComboType


class FiveCard(ComboType):
    @classmethod
    # @functools.lru_cache()
    def from_hand(cls, cards: Tuple[DeucesCard]):
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
        # Straight Flush / Royal Flush
        #   Five consecutive cards of the same suit
        #   Royal Flush is a Straight Flush that ends on an Ace

        sorted_cards = list(sorted(cards, key=lambda c: c.value))
        unique_ranks = set(c.rank for c in cards)

        if len(unique_ranks) == 2:
            # Get middle card of a sorted combo
            # e.g. 7 is always the majority card when there are two unique ranks
            # 3 3 [7] 7 7 - Full House on 7
            # 3 7 [7] 7 7 - Four of a Kind on 7
            # 7 7 [7] 7 K - Four of a Kind on 7
            # 7 7 [7] K K - Full House on 7
            majority_card_rank_ix = DeucesCard.RANK_TO_ORDER[sorted_cards[2].rank]
            # Four of a Kind
            if sorted_cards[1] == sorted_cards[2] == sorted_cards[3]:
                return FourOfAKind(rank_ix=majority_card_rank_ix)
            # Full House
            else:
                return FullHouse(rank_ix=majority_card_rank_ix)
        elif len(unique_ranks) == 5:
            is_flush = (cards[0] == cards[1] == cards[2] == cards[3] == cards[4])
            straight = (StraightFlush if is_flush else Straight).from_sorted_cards(sorted_cards)
            if straight:
                return straight
            elif is_flush:
                return Flush(
                    suit_ix=DeucesCard.SUIT_TO_ORDER[sorted_cards[-1].suit],
                    end_rank_ix=DeucesCard.RANK_TO_ORDER[sorted_cards[-1].rank],
                )
            else:
                return InvalidFiveCard()
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
    # LEGAL:   7  8  9  10 11 - ends on a Rank.ACE (11)
    # ILLEGAL: 8  9  10 11 12 - ends on a Rank.TWO (12)
    # ILLEGAL: 0  9  10 11 12 - ends on a Rank.THREE (0)
    # ILLEGAL: 0  1  10 11 12 - ends on a Rank.FOUR (1)
    # LEGAL:   0  1  2  11 12 - ends on a Rank.FIVE (2)
    # LEGAL:   0  1  2  3  12 - ends on a Rank.SIX (3)
    # LEGAL:   0  1  2  3  4  - ends on a Rank.SEVEN (4)
    VALID_STRAIGHTS_TO_END_RANK: Dict[str, Rank] = {
        '3 4 5 A 2': Rank.FIVE,
        '3 4 5 6 2': Rank.SIX,
        '3 4 5 6 7': Rank.SEVEN,
        '4 5 6 7 8': Rank.EIGHT,
        '5 6 7 8 9': Rank.NINE,
        '6 7 8 9 T': Rank.TEN,
        '7 8 9 T J': Rank.JACK,
        '8 9 T J Q': Rank.QUEEN,
        '9 T J Q K': Rank.KING,
        'T J Q K A': Rank.ACE
    }
    VALID_STRAIGHTS_TO_END_RANK_POS: Dict[str, int] = {
        '3 4 5 A 2': 2,
        '3 4 5 6 2': 3,
        '3 4 5 6 7': 4,
        '4 5 6 7 8': 4,
        '5 6 7 8 9': 4,
        '6 7 8 9 T': 4,
        '7 8 9 T J': 4,
        '8 9 T J Q': 4,
        '9 T J Q K': 4,
        'T J Q K A': 4,
    }

    @classmethod
    def from_sorted_cards(cls, sorted_cards: Tuple[DeucesCard]) -> Optional:
        serialized_cards = ' '.join(c.rank.value for c in sorted_cards)
        end_rank_pos = Straight.VALID_STRAIGHTS_TO_END_RANK_POS.get(serialized_cards)
        if end_rank_pos:
            end_card = sorted_cards[end_rank_pos]
            return cls(
                end_rank_ix=DeucesCard.RANK_TO_ORDER[end_card.rank],
                end_rank_suit_ix=DeucesCard.SUIT_TO_ORDER[end_card.suit]
            )
        else:
            return None


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


class StraightFlush(Straight):
    pass


FIVE_CARD_COMBO_ORDER: List[FiveCard] = [InvalidFiveCard, Straight, Flush, FullHouse, FourOfAKind, StraightFlush]
FIVE_CARD_COMBO_TO_ORDER: Dict[FiveCard, int] = dict((f, i) for i, f in enumerate(FIVE_CARD_COMBO_ORDER))

