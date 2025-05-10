import pytest
import unittest
from unittest.mock import patch
from chinese_checkers.game import Game
from chinese_checkers.constants import WIDTH, HEIGHT, RED, GREEN
import pygame

mock_win = pygame.display.set_mode((WIDTH, HEIGHT))
class TestGameInitialization(unittest.TestCase):


    @patch('builtins.input', side_effect=["no", "no", "2", "1", "Player1"])
    def test_game_init_add_players(self, mock_input):
        game = Game(mock_win)  # Assuming mock_win is provided
        # Add assertions to verify the initialization behavior
        assert game.num_of_players == 2
        assert game.num_of_computers == 1

        assert game.players == {"Player1": game.get_player_by_name("Player1"), "Computer 1": game.get_player_by_name("Computer 1")}
        assert game.calculate_first_loc() == [(0, 12), (13, 9)]
        assert game.calculate_starting_position() == [[(0, 12),(1, 11),(1, 13),(2, 10),(2, 12),(2, 14),(3, 9),(3, 11),(3, 13),(3, 15)],
                            [(13, 9),(13, 11),(13, 13),(13, 15),(14, 10),(14, 12),(14, 14),(15, 11),(15, 13),(16, 12)]]
        assert game.calculate_target_position() == [[(13, 9),(13, 11),(13, 13),(13, 15),(14, 10),(14, 12),(14, 14),(15, 11),(15, 13),(16, 12)],
                                        [(0, 12),(1, 11),(1, 13),(2, 10),(2, 12),(2, 14),(3, 9),(3, 11),(3, 13),(3, 15)]]
        game.add_targets_to_players()
        assert ({"Player1": game.get_player_by_name("Player1").get_target_locs(),
                "Computer 1": game.get_player_by_name("Computer 1").get_target_locs()}
                == {"Player1": {(13, 9): 0 ,(13, 11): 0,(13, 13): 0,(13, 15): 0,(14, 10): 0,(14, 12): 0,(14, 14): 0,(15, 11): 0,(15, 13): 0,(16, 12): 0},
                    "Computer 1": {(0, 12): 0,(1, 11): 0,(1, 13): 0,(2, 10): 0,(2, 12): 0,(2, 14): 0,(3, 9): 0,(3, 11): 0,(3, 13): 0,(3, 15): 0}})
        game.place_pieces_on_board()
        assert game.board.get_piece((0, 12)).get_location() == (0, 12)
        assert game.board.get_piece((0, 12)).get_color() == RED
        assert game.board.get_piece((13, 9)).get_location() == (13, 9)
        assert game.board.get_piece((13, 9)).get_color() == GREEN
        player1_pieces = game.get_player_by_name("Player1").get_pieces()
        assert player1_pieces[(1, 11)].get_location() == (1, 11)
        assert player1_pieces[(1, 11)].get_color() == RED
        computer1_pieces = game.get_player_by_name("Computer 1").get_pieces()
        assert computer1_pieces[(14, 10)].get_location() == (14, 10)
        assert computer1_pieces[(14, 10)].get_color() == GREEN


if __name__ == '__main__':
    unittest.main()