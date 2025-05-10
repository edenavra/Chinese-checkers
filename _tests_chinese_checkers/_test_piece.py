from chinese_checkers.piece import Piece
from chinese_checkers.constants import SQUARE_SIZE, GREEN, YELLOW
import pytest

def test_get_id():
    piece = Piece(GREEN, str(GREEN)+"1", (0, 0))
    assert str(GREEN)+"1" == piece.get_id()
    piece2 = Piece(YELLOW, str(YELLOW)+"34", (0, 12))
    assert str(YELLOW)+"34" == piece2.get_id()

def test_get_location():
    piece = Piece(GREEN, str(GREEN)+"1", (0, 0))
    assert (0,0) == piece.get_location()
    piece2 = Piece(YELLOW, str(YELLOW)+"34", (0, 12))
    assert (0,12) == piece2.get_location()

def test_get_color():
    piece = Piece(GREEN, str(GREEN)+"1", (0, 0))
    assert GREEN == piece.get_color()
    piece2 = Piece(YELLOW, str(YELLOW)+"34", (0, 12))
    assert YELLOW == piece2.get_color()

def test_move():
    piece = Piece(GREEN, str(GREEN)+"1", (0, 0))
    piece.move((1, 1))
    assert (1, 1) == piece.get_location()
    piece2 = Piece(YELLOW, str(YELLOW)+"34", (0, 12))
    piece2.move((23, 1))
    assert (23, 1) == piece2.get_location()

def test_calc_pos():
    piece = Piece(GREEN, str(GREEN)+"1", (0, 0))
    piece.calc_pos()
    assert SQUARE_SIZE//2 == piece.x
    assert SQUARE_SIZE//2 == piece.y
    piece2 = Piece(YELLOW, str(YELLOW)+"34", (0, 12))
    piece2.calc_pos()
    assert SQUARE_SIZE//2 == piece2.y
    assert SQUARE_SIZE*12 + SQUARE_SIZE//2 == piece2.x

def test_piece():
    test_get_id()
    test_get_location()
    test_get_color()
    test_move()
    test_calc_pos()
    print("All tests passed!")

if __name__ == "__main__":
    test_piece()