from enum import Enum, unique
from typing import List, Tuple

NUM_CARDS = 13


@unique
class Suit(Enum):
    SPADES = 1
    DIAMONDS = 2
    CLUBS = 3
    HEARTS = 4


class Rank(Enum):
    JOKER = 0
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


class Card:
    rank: Rank
    suit: Suit

    def __init__(self, rank: int, suit: Suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit.name}"


class Player:
    purse: int


class Round:
    pot: int
    potIsOpen: int
    usedCards: List[Card]


class Game:
    round: int
    turn: int
    players: List[Player]
    suits = [Suit.SPADES, Suit.DIAMONDS, Suit.CLUBS, Suit.HEARTS]
    ranks = [
        Rank.ACE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE, Rank.SIX,
        Rank.SEVEN, Rank.EIGHT, Rank.NINE, Rank.TEN, Rank.JACK, Rank.QUEEN,
        Rank.KING
    ]
    deck: List[Tuple[Rank, Suit]]

    def __init__(self):
        rounds = []
        players = []
        self.deck = [(rank, suit)
                     for suit in self.suits for rank in self.ranks]
        self.deck.append((Rank.JOKER, Suit.SPADES),
                         (Rank.JOKER, Suit.DIAMONDS))

        while (not self.check_endgame()):
            self.round += 1
            self.turn = 0
            rounds.append(Round())
            for player in players:
                player.purse = 100

    def update(self):
        pass

    def check_endgame(self):
        # TODO: figure this out
        return False
