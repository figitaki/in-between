from enum import Enum, unique
from typing import List, Tuple, Optional
from random import shuffle
import math
import random

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
    """
    Representation of a playing card. A card has a rank and a suit. The rank
    is an instance of the Rank enum, and the suit is an instance of the Suit
    enum. A card may also have an ace_high attribute, which is a boolean
    indicating whether the card should be considered an ace high or low.
    """

    rank: Rank
    suit: Suit
    ace_high: Optional[bool]

    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit
        self.ace_high = None

    def __repr__(self):
        return f"{self.rank.name} of {self.suit.name} {'(high)' if self.rank == Rank.ACE and self.ace_high else ''}"

    def value(self) -> int:
        if self.rank == Rank.ACE and self.ace_high:
            return 14
        else:
            return self.rank.value


Hand = Tuple[Card | None, Card | None]


def calculate_spread(hand: Hand):
    if hand[0] is None or hand[1] is None:
        return 0
    if hand[0].value() > hand[1].value():
        return hand[0].value() - hand[1].value()
    else:
        return hand[1].value() - hand[0].value()


def create_random_array(n, m):
    # Step 1: Create a list of n zeros
    arr = [0] * n
    # Step 2: Randomly choose m unique positions to set to 1
    # Note: random.sample is used to select m unique positions without replacement
    positions = random.sample(range(n), m)

    # Set chosen positions to 1
    for pos in positions:
        arr[pos] = 1
    return arr


class Strategy(Enum):
    MINIMUM = 1
    AGGRESSIVE = 2
    USER = 3
    SCALE = 4
    SMART_LIN = 5
    SMART_EXP = 6
    ALWAYS_BET = 7


class Player:
    """
    Representation of a player in the game. A player has a purse, which is the
    amount of money they have to bet with. A player also has a strategy, which
    determines how they will play the game.
    """

    purse: int
    strategy: Strategy

    def __init__(self, purse: int = 100, strategy: Strategy = Strategy.MINIMUM):
        self.purse = purse
        self.strategy = strategy

    def __repr__(self) -> str:
        return f" Purse: ${self.purse}"

    def decide_ace_high(self, hand: Hand):
        return False

    def decide_bet(self, hand, pot, deck: List[Card]):
        # TODO: be smarter, for now just bet if spread is greater than 6
        spread = calculate_spread(hand)
        # print(f"spread: {spread}, pot: ${pot}, purse: ${self.purse}")
        user_max_bet = min(pot, self.purse)
        match self.strategy:
            case Strategy.ALWAYS_BET:
                return 1
            case Strategy.MINIMUM:
                if spread > 6:
                    return 1
            case Strategy.AGGRESSIVE:
                if spread > 9:
                    return user_max_bet
                if spread > 6:
                    return min(pot, self.purse // 2)
            case Strategy.SCALE:
                return user_max_bet * (spread // 14) if spread > 6 else 0
            case Strategy.SMART_LIN:
                outcomes = 0
                low: int = min(hand[0].value(), hand[1].value())
                high: int = max(hand[1].value(), hand[0].value())
                for card in deck:
                    if card.rank == Rank.JOKER:
                        # because jokers are only min_bet we can ignore
                        continue
                    if card.value() == low or card.value() == high:
                        outcomes -= 2
                    if card.value() > low and card.value() < high:
                        outcomes += 1
                    else:
                        outcomes -= 1
                # range is [-2, 1]
                normalizedOutcome = outcomes / \
                    len(deck) if len(deck) > 0 else 0
                bet = math.floor(
                    user_max_bet * normalizedOutcome if normalizedOutcome > 0 else 0
                )
                return bet
            case Strategy.SMART_EXP:
                outcomes = 0
                low: int = min(hand[0].value(), hand[1].value())
                high: int = max(hand[1].value(), hand[0].value())
                for card in deck:
                    if card.rank == Rank.JOKER:
                        # because jokers are only min_bet we can ignore
                        continue
                    if card.value() == low or card.value() == high:
                        outcomes -= 2
                    if card.value() > low and card.value() < high:
                        outcomes += 1
                    else:
                        outcomes -= 1
                # range is [-2, 1]
                normalizedOutcome = outcomes / \
                    len(deck) if len(deck) > 0 else 0
                bet = math.floor(
                    user_max_bet * (normalizedOutcome**0.5)
                    if normalizedOutcome > 0
                    else 0
                )
                return bet
            case Strategy.USER:
                bet = input("Enter bet amount: ")
                if bet == "":
                    return None
                return int(bet)


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
        Rank.ACE,
        Rank.TWO,
        Rank.THREE,
        Rank.FOUR,
        Rank.FIVE,
        Rank.SIX,
        Rank.SEVEN,
        Rank.EIGHT,
        Rank.NINE,
        Rank.TEN,
        Rank.JACK,
        Rank.QUEEN,
        Rank.KING,
    ]
    deck: List[Card]
    min_bet: int
    pot: int

    def __init__(self, num_players: int = 4):
        self.round = 0
        self.players = [
            Player(100, Strategy.AGGRESSIVE if index %
                   2 == 0 else Strategy.MINIMUM)
            for index in range(num_players)
        ]
        self.min_bet = 1
        self.pot = 0
        self.turn = 0
        self.shuffle_deck()

    def __repr__(self) -> str:
        return f"""
            Pot: ${self.pot}
            Round  # : {self.round}
            Turn: {self.turn}
            Players: {self.players}
            Remaining Cards: {self.deck.__len__()}
            Min Bet: {self.min_bet}"""

    def play(self, num_rounds: int):
        for _ in range(num_rounds):
            self.update()

    def shuffle_deck(self):
        self.deck = [Card(rank, suit)
                     for suit in self.suits for rank in self.ranks]
        self.deck.append(Card(Rank.JOKER, Suit.SPADES))
        self.deck.append(Card(Rank.JOKER, Suit.DIAMONDS))
        shuffle(self.deck)

    def update(self):
        self.round += 1
        self.turn = 0
        self.shuffle_deck()

        for player in self.players:
            # ante up
            self.transfer(player, -self.min_bet)

        while not self.check_endgame():
            for player in self.players:
                self.take_turn(player)
                if self.check_endgame():
                    return
                self.turn += 1
                # print(self)
                # _ = input("Press enter to continue")

    def check_endgame(self):
        if self.pot == 0:
            return True
        if self.pot > 100:
            split = self.pot // len(self.players)
            remainder = self.pot % len(self.players)
            random = create_random_array(len(self.players), remainder)
            for i, player in enumerate(self.players):
                self.transfer(player, split + random[i])
            return True
        else:
            return False

    def transfer(self, player: Player, amount: int):
        player.purse += amount
        self.pot -= amount

    def take_turn(self, player: Player, first_card: Optional[Card] = None):
        hand = (first_card, None)
        in_between = None

        def deal_card():
            if len(self.deck) == 0:
                # print("Deck is empty! Shuffling...")
                self.shuffle_deck()
            card = self.deck.pop()
            # print(f"Dealt: {card}")

            if card.rank == Rank.JOKER:
                # player loses automatically, pays min_bet
                self.transfer(player, -self.min_bet)
                return
            if hand[0] and card.rank == hand[0].rank:
                self.take_turn(player, card)
                card = deal_card()
                return card
            elif card.rank == Rank.ACE:
                card.ace_high = player.decide_ace_high(hand)
            return card

        # deal first card
        if first_card is None:
            card = deal_card()
            if card is None:
                return
            else:
                hand = (card, None)

        # deal second card
        card_two = deal_card()
        if card_two is None:
            return

        hand = (hand[0], card_two)
        bet = player.decide_bet(hand, self.pot, self.deck)
        if bet is not None:
            in_between = deal_card()
            if in_between is None:
                return

            low: int = min(hand[0].value(), hand[1].value())
            high: int = max(hand[0].value(), hand[1].value())
            in_between_val: int = in_between.value()
            if in_between_val == low or in_between_val == high:
                self.transfer(player, -2 * bet)
            elif in_between_val > low and in_between_val < high:
                self.transfer(player, bet)
            else:
                self.transfer(player, -bet)
