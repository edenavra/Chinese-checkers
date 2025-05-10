import pytest
from chinese_checkers.player import Player
from chinese_checkers.constants import RED, GREEN, YELLOW, BLUE
from chinese_checkers.piece import Piece

def test_get_name():
    player = Player("Player1", RED)
    assert "Player1" == player.get_name()
    player2 = Player("Player2", GREEN)
    assert "Player2" == player2.get_name()

def test_add_win():
    player = Player("Player1", RED)
    player.add_win()
    assert 1 == player.get_number_of_wins()
    player.add_win()
    assert 2 == player.get_number_of_wins()

def test_add_loss():
    player = Player("Player1", RED)
    player.add_loss()
    assert 1 == player.get_number_of_losses()
    player.add_loss()
    assert 2 == player.get_number_of_losses()

def test_get_number_of_wins():
    player = Player("Player1", RED)
    assert 0 == player.get_number_of_wins()
    player.add_win()
    assert 1 == player.get_number_of_wins()

def test_get_number_of_losses():
    player = Player("Player1", RED)
    assert 0 == player.get_number_of_losses()
    player.add_loss()
    assert 1 == player.get_number_of_losses()

def test_move_piece():
    player = Player("Player1", RED)
    piece = Piece(RED, str(RED)+"1", (0, 0))
    player.add_piece(piece)
    piece2 = Piece(RED, str(RED)+"2", (0, 1))
    player.add_piece(piece2)
    assert player.move_piece((0,0), (1,1)) == True
    assert player.move_piece((0,0), (0,1)) == False #no piece there
    assert player.move_piece((0,1), (1,1)) == False #already a piece there
    assert player.move_piece((1,1), (1,1)) == False
    assert player.move_piece((1,1), (2,2)) == True
    assert player.move_piece((1,1), (1,2)) == False

def test_check_if_winner():
    player = Player("Player1", RED)
    piece = Piece(RED, str(RED)+"1", (0, 0))
    player.add_piece(piece)
    piece2 = Piece(RED, str(RED)+"2", (0, 1))
    player.add_piece(piece2)
    piece3 = Piece(YELLOW, str(YELLOW)+"3", (0, 2))
    assert player.check_if_winner() == False
    player.target_locs = {(0, 0): piece , (0, 1): piece2, (0, 2):piece3, (0, 3): 0, (0, 4): 0, (0, 5): 0}
    assert player.check_if_winner() == False
    player.target_locs = {(0, 0): piece, (0, 1): piece2}
    assert player.check_if_winner() == True
    player.target_locs = {(0, 0): 0, (0, 1): 0, (0, 2): 0, (0, 3): 0, (0, 4): 0, (0, 5): 0, (0, 6): 0}
    assert player.check_if_winner() == False
    player.target_locs = {(0, 0): piece, (0, 1): piece2, (0, 2): 0, (0, 3): 0, (0, 4): 0, (0, 5): 0}
    assert player.check_if_winner() == False

def test_add_piece():
    player = Player("Player1", RED)
    piece = Piece(RED, str(RED)+"1", (0, 0))
    player.add_piece(piece)
    assert piece in player.get_pieces().values()
    piece2 = Piece(RED, str(RED)+"2", (0, 1))
    player.add_piece(piece2)
    assert piece2 in player.get_pieces().values()
    piece3 = Piece(YELLOW, str(YELLOW)+"3", (0, 2))
    player.add_piece(piece3)
    assert piece3 in player.get_pieces().values()
    piece4 = Piece(BLUE, str(BLUE)+"4", (0, 3))
    player.add_piece(piece4)
    assert piece4 in player.get_pieces().values()

def test_get_pieces():
    player = Player("Player1", RED)
    piece = Piece(RED, str(RED)+"1", (0, 0))
    player.add_piece(piece)
    assert piece in player.get_pieces().values()
    piece2 = Piece(RED, str(RED)+"2", (0, 1))
    player.add_piece(piece2)
    assert piece2 in player.get_pieces().values()
    piece3 = Piece(YELLOW, str(YELLOW)+"3", (0, 2))
    player.add_piece(piece3)
    assert piece3 in player.get_pieces().values()
    piece4 = Piece(BLUE, str(BLUE)+"4", (0, 3))
    player.add_piece(piece4)
    assert piece4 in player.get_pieces().values()

def test_add_target_loc():
    player = Player("Player1", RED)
    player.add_target_loc((0, 0))
    assert (0, 0) in player.get_target_locs().keys()
    player.add_target_loc((0, 1))
    assert (0, 1) in player.get_target_locs().keys()
    player.add_target_loc((0, 2))
    assert (0, 2) in player.get_target_locs().keys()
    player.add_target_loc((0, 3))
    assert (0, 3) in player.get_target_locs().keys()

def test_get_target_locs():
    player = Player("Player1", RED)
    player.add_target_loc((0, 0))
    assert (0, 0) in player.get_target_locs().keys()
    player.add_target_loc((0, 1))
    assert (0, 1) in player.get_target_locs().keys()
    player.add_target_loc((0, 2))
    assert (0, 2) in player.get_target_locs().keys()
    player.add_target_loc((0, 3))
    assert (0, 3) in player.get_target_locs().keys()

def test_check_if_computer():
    player = Player("Player1", RED)
    assert player.check_if_computer() == False
    player2 = Player("Player2", GREEN, True)
    assert player2.check_if_computer() == True

def test_get_color():
    player = Player("Player1", RED)
    assert RED == player.get_color()
    player2 = Player("Player2", GREEN)
    assert GREEN == player2.get_color()

def test_player():
    test_get_name()
    test_add_win()
    test_add_loss()
    test_get_number_of_wins()
    test_get_number_of_losses()
    test_move_piece()
    test_check_if_winner()
    test_add_piece()
    test_get_pieces()
    test_add_target_loc()
    test_get_target_locs()
    test_check_if_computer()
    test_get_color()
    print("All tests passed!")

if __name__ == "__main__":
    test_player()