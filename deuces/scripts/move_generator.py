import os
import sys

from typing import (
    Iterable,
    Tuple,
)

from deuces import (
    DeucesCard,
)


VALID_STRAIGHTS_RANK_IXS = [
    (0, 1, 2, 11, 12),
    (0, 1, 2, 3, 12),
    (0, 1, 2, 3, 4),
    (1, 2, 3, 4, 5),
    (2, 3, 4, 5, 6),
    (3, 4, 5, 6, 7),
    (4, 5, 6, 7, 8),
    (5, 6, 7, 8, 9),
    (6, 7, 8, 9, 10),
    (7, 8, 9, 10, 11),
]


def generate_all_singles(skip_rank_ix: int = -1) -> Iterable[Tuple[DeucesCard]]:
    rs = DeucesCard.RANK_ORDER if skip_rank_ix == -1 else (
            DeucesCard.RANK_ORDER[:skip_rank_ix] + DeucesCard.RANK_ORDER[skip_rank_ix+1:])
    for r in rs:
        for s in DeucesCard.SUIT_ORDER:
            yield DeucesCard(r, s),  # returns tuple


def generate_all_twos(skip_rank_ix: int = -1) -> Iterable[Tuple[DeucesCard]]:
    rs = DeucesCard.RANK_ORDER if skip_rank_ix == -1 else (
        DeucesCard.RANK_ORDER[:skip_rank_ix] + DeucesCard.RANK_ORDER[skip_rank_ix+1:])
    for r in rs:
        for s0_ix, s0 in enumerate(DeucesCard.SUIT_ORDER):
            s1_ss = DeucesCard.SUIT_ORDER[s0_ix+1:]
            for s1 in s1_ss:
                yield DeucesCard(r, s0), DeucesCard(r, s1)


def generate_all_threes(skip_rank_ix: int = -1) -> Iterable[Tuple[DeucesCard]]:
    rs = DeucesCard.RANK_ORDER if skip_rank_ix == -1 else (
            DeucesCard.RANK_ORDER[:skip_rank_ix] + DeucesCard.RANK_ORDER[skip_rank_ix+1:])
    s0_ss = DeucesCard.SUIT_ORDER
    for r in rs:
        for s0_ix, s0 in enumerate(s0_ss):
            s1_ss = DeucesCard.SUIT_ORDER[s0_ix+1:]
            for s1_ix, s1 in enumerate(s1_ss, start=s0_ix+1):
                s2_ss = DeucesCard.SUIT_ORDER[s1_ix+1:]
                for s2 in s2_ss:
                    yield DeucesCard(r, s0), DeucesCard(r, s1), DeucesCard(r, s2)


def generate_all_fours() -> Iterable[Tuple[DeucesCard]]:
    for r in DeucesCard.RANK_ORDER:
        yield tuple(DeucesCard(r, s) for s in DeucesCard.SUIT_ORDER)


def generate_all_combos() -> Iterable[Tuple[DeucesCard]]:
    for group in _generate_straights():
        yield group
    for group in _generate_flushes():
        yield group
    for group in _generate_full_house():
        yield group
    for group in _generate_four_of_a_kind():
        yield group
    for group in _generate_straight_flush():
        yield group


def _generate_straights(include_straight_flushes=False) -> Iterable[Tuple[DeucesCard]]:
    for vs_ixs in VALID_STRAIGHTS_RANK_IXS:
        for s0 in DeucesCard.SUIT_ORDER:
            for s1 in DeucesCard.SUIT_ORDER:
                for s2 in DeucesCard.SUIT_ORDER:
                    for s3 in DeucesCard.SUIT_ORDER:
                        for s4 in DeucesCard.SUIT_ORDER:
                            if (
                                include_straight_flushes or
                                not s0 == s1 == s2 == s3 == s4
                            ):
                                yield (
                                    DeucesCard(DeucesCard.RANK_ORDER[r], s)
                                    for r, s in zip(vs_ixs, (s4, s3, s2, s1, s0))
                                )


def _generate_flushes(include_straight_flushes=False) -> Iterable[Tuple[DeucesCard]]:
    r0_rs = DeucesCard.RANK_ORDER[4:]  # possible end cards
    for s in DeucesCard.SUIT_ORDER:
        for r0_ix, r0 in enumerate(r0_rs, start=4):
            r1_rs = DeucesCard.RANK_ORDER[3:r0_ix]  # start at lowest possible card and go up to previous card's index
            for r1_ix, r1 in enumerate(r1_rs, start=3):
                r2_rs = DeucesCard.RANK_ORDER[2:r1_ix]
                for r2_ix, r2 in enumerate(r2_rs, start=2):
                    r3_rs = DeucesCard.RANK_ORDER[1:r2_ix]
                    for r3_ix, r3 in enumerate(r3_rs, start=1):
                        r4_rs = DeucesCard.RANK_ORDER[:r3_ix]
                        for r4_ix, r4 in enumerate(r4_rs):
                            if (
                                include_straight_flushes or
                                not (  # a straight
                                    (
                                        r0_ix == (r1_ix+1) == (r2_ix+2) == (r3_ix+3) == (r4_ix+4) and
                                        r0_ix != 12
                                    ) or
                                    (r0_ix, r1_ix, r2_ix, r3_ix, r4_ix) in [(12, 11, 2, 1, 0), (12, 3, 2, 1, 0)]
                                )
                            ):
                                yield (
                                    DeucesCard(r4, s),
                                    DeucesCard(r3, s),
                                    DeucesCard(r2, s),
                                    DeucesCard(r1, s),
                                    DeucesCard(r0, s),
                                )


def _generate_full_house() -> Iterable[Tuple[DeucesCard]]:
    triples = generate_all_threes()
    for triple in triples:
        pairs = generate_all_twos(skip_rank_ix=DeucesCard.RANK_TO_ORDER[triple[0].rank])
        for pair in pairs:
            yield tuple(sorted([*triple, *pair]))


def _generate_four_of_a_kind() -> Iterable[Tuple[DeucesCard]]:
    for foak_r_ix, foak_r in enumerate(DeucesCard.RANK_ORDER):
        single_rs = DeucesCard.RANK_ORDER[:foak_r_ix] + DeucesCard.RANK_ORDER[foak_r_ix+1:]
        for single_r in single_rs:
            for single_s in DeucesCard.SUIT_ORDER:
                yield tuple(sorted(
                    [DeucesCard(foak_r, foak_s) for foak_s in DeucesCard.SUIT_ORDER] +
                    [DeucesCard(single_r, single_s)]
                ))


def _generate_straight_flush() -> Iterable[Tuple[DeucesCard]]:
    for vs_ixs in VALID_STRAIGHTS_RANK_IXS:
        for s in DeucesCard.SUIT_ORDER:
            yield (DeucesCard(DeucesCard.RANK_ORDER[r], s) for r in vs_ixs)


def write_all_possible_moves(directory='.'):
    move_generators = {
        '1s': generate_all_singles,
        '2s': generate_all_twos,
        '3s': generate_all_threes,
        '4s': generate_all_fours,
        '5s': generate_all_combos,
        'st': _generate_straights,
        'fl': _generate_flushes,
        'fh': _generate_full_house,
        'fk': _generate_four_of_a_kind,
        'sf': _generate_straight_flush,
    }
    for group_type, generator in move_generators.items():
        filename = os.path.join(directory, f'{group_type}.csv')
        with open(filename, 'w') as f:
            for group in generator():
                f.write(','.join(str(c) for c in group) + '\n')


if __name__ == '__main__':
    write_directory = sys.argv[1] if len(sys.argv) > 1 else os.path.join('..', 'data', 'moves')
    write_all_possible_moves(directory=write_directory)
