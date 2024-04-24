import unittest
from in_between import Game, Suit, Card, Rank


class InBetweenSimulationTest(unittest.TestCase):
    def test_game_creation(self):
        # TODO: setup game
        game = Game()
        self.assertEqual(game.round, 0)
        self.assertEqual(len(game.players), 4)
        self.assertEqual(game.min_bet, 1)

    def test_game_shuffle_deck(self):
        game = Game()
        game.shuffle_deck()
        self.assertEqual(len(game.deck), 54)

    def test_joker(self):
        game = Game()
        game.deck = [Card(Suit.DIAMONDS, Rank.JOKER)]
        game.take_turn(game.players[0])
        self.assertEqual(game.players[0].purse, 99)
        self.assertEqual(game.pot, 1)


if __name__ == '__main__':
    unittest.main()
