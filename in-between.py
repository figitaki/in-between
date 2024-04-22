from enum import Enum, unique
from typing import List

NUM_CARDS = 13


@unique
class Suit(Enum):
    SPADES = 1
    DIAMONDS = 2
    CLUBS = 3
    HEARTS = 4


class Card:
    suit: Suit
    number: int


class Deck:
    cards: List[Card]
    number: int


class Player:
    purse: int


class Round:
    pot: int
    potIsOpen: int
    usedCards: List[Card]


class Game:
    rounds: List[Round]
    players: List[Player]

    def __init__(self):
        rounds = []
        players = []
