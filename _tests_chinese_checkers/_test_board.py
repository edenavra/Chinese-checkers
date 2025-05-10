import pytest
from chinese_checkers.board import Board
from chinese_checkers.piece import Piece
from chinese_checkers.constants import RED


def test_get_piece(board, location, expected):
    assert board.get_piece(location) == expected, f"expected: {expected}, got: {board.get_piece(location)}"




def test_get_all_pieces_locations(board, expected):
    assert board.get_all_pieces_locations() == expected, f"expected: {expected}, got: {board.get_all_pieces_locations()}"



def test_cell_content(board, location, expected):
    assert board.cell_content(location) == expected, f"expected: {expected}, got: {board.cell_content(location)}"



def test_get_around(board, location, expected):
    assert board.get_around(location) == expected, f"expected: {expected}, got: {board.get_around(location)}"


def test_add_piece(board, piece, expected):
    assert board.add_piece(piece) == expected


def test_optional_moves(board, piece, expected):
    assert board.optional_moves(piece) == expected , f"expected: {expected}, got: {board.optional_moves(piece)}"


def test_move_piece(board, piece_loc, destination, expected):
    assert board.move_piece(piece_loc, destination) == expected, f"expected: {expected}, got: {board.move_piece(piece, destination)}"




def test_get_piece_by_coordinates(board, location, expected):
    assert board.get_piece_by_coordinates(location) == expected, f"expected: {expected}, got: {board.get_piece_by_coordinates(location)}"



def test_board():
    board = Board()
    board2 = Board()
    piece = Piece(RED, str(RED) + "1", (0, 12))
    board2.add_piece(piece)
    piece2 = Piece(RED, str(RED) + "2", (1, 11))
    board2.add_piece(piece2)
    piece3 = Piece(RED, str(RED) + "3", (2, 14))
    board2.add_piece(piece3)
    piece4 = Piece(RED, str(RED) + "4", (10, 12))
    board2.add_piece(piece4)
    piece5 = Piece(RED, str(RED) + "5", (11, 11))
    board2.add_piece(piece5)
    piece6 = Piece(RED, str(RED) + "6", (9, 11))
    board2.add_piece(piece6)
    piece7 = Piece(RED, str(RED) + "7", (4, 24))
    board2.add_piece(piece7)
    piece8 = Piece(RED, str(RED) + "8", (4, 22))
    board2.add_piece(piece8)
    piece9 = Piece(RED, str(RED) + "9", (4, 20))
    board2.add_piece(piece9)
    piece10 = Piece(RED, str(RED) + "10", (5, 23))
    board2.add_piece(piece10)
    piece11 = Piece(RED, str(RED) + "11", (5, 21))
    board2.add_piece(piece11)
    piece12 = Piece(RED, str(RED) + "12", (6, 22))
    board2.add_piece(piece12)
    piece13 = Piece(RED, str(RED) + "13", (6, 4))
    board2.add_piece(piece13)
    piece14 = Piece(RED, str(RED) + "14", (11, 3))
    board2.add_piece(piece14)
    piece15 = Piece(RED, str(RED) + "15", (10, 2))
    board2.add_piece(piece15)

    print(board2)

    test_get_piece(board, (0, 12), 0)
    test_get_piece(board, (10, 12), 0)
    test_get_piece(board2, (11, 11), piece5)
    test_get_piece(board2, (10, 2), piece15)

    test_get_all_pieces_locations(board2,
                                  [(0, 12), (1, 11), (2, 14), (10, 12), (11, 11), (9, 11), (4, 24), (4, 22), (4, 20),
                                   (5, 23), (5, 21), (6, 22), (6, 4), (11, 3), (10, 2)])
    test_get_all_pieces_locations(board, [])

    test_cell_content(board, (0, 12), 0)
    test_cell_content(board, (10, 12), 0)
    test_cell_content(board, (1, 4), None)
    test_cell_content(board2, (11, 11), piece5)
    test_cell_content(board2, (10, 2), piece15)
    test_cell_content(board2, (4, 24), piece7)
    test_cell_content(board2, (4, 12), 0)
    test_cell_content(board2, (0, 0), None)

    test_get_around(board, (2, 12), {(1, 11), (1, 13), (2, 10), (2, 14), (3, 11), (3, 13)})
    test_get_around(board, (0, 12), {(1, 11), (1, 13)})
    test_get_around(board, (0, 0), set())
    test_get_around(board, (10, 12), {(9, 11), (9, 13), (10, 10), (10, 14), (11, 11), (11, 13)})

    test_add_piece(board, Piece(RED, str(RED) + "1", (0, 12)), True)
    test_add_piece(board, Piece(RED, str(RED) + "1", (0, 12)), False)  # same id
    test_add_piece(board, Piece(RED, str(RED) + "2", (0, 12)), False)  # same location
    test_add_piece(board, Piece(RED, str(RED) + "2", (0, 11)), False)  # location out of bounds
    test_add_piece(board, Piece(RED, str(RED) + "2", (16, 12)), True)  # edges
    test_add_piece(board, Piece(RED, str(RED) + "3", (4, 0)), True)  # edges
    test_add_piece(board, Piece(RED, str(RED) + "6", (4, 24)), True)  # edges
    test_add_piece(board, Piece(RED, str(RED) + "7", (12, 0)), True)  # edges
    test_add_piece(board, Piece(RED, str(RED) + "8", (12, 24)), True)  # edges
    test_add_piece(board, Piece(RED, str(RED) + "4", (4, 15)), False)  # not a valid location
    test_add_piece(board, Piece(RED, str(RED) + "5", (20, 14)), False)  # out of range
    test_add_piece(board, Piece(RED, str(RED) + "5", (None)), False)  # not a valid type

    # a piece that hops to mor than 1 direction
    test_optional_moves(board2, piece4, {(10, 10), (10, 14), (12, 10), (11, 13), (8, 10), (9, 13)})
    # a piece at the edge with a hop
    test_optional_moves(board2, piece, {(1, 13), (2, 10)})
    # a piece at the edge 1 neighbor
    test_optional_moves(board2, piece2, {(1, 13), (2, 10), (2, 12)})
    # a piece at the edge no neighbors
    test_optional_moves(board2, piece3, {(1, 13), (2, 12), (3, 13), (3, 15)})
    # a piece with more than 1 hop
    test_optional_moves(board2, piece5, {(11, 9), (11, 13), (12, 10), (12, 12), (10, 10), (9, 13), (9, 9)})
    # the opposite direction of the previous test
    test_optional_moves(board2, piece6, {(9, 9), (9, 13), (10, 10), (11, 13), (11, 9), (8, 10), (8, 12)})
    # no moves
    test_optional_moves(board2, piece7, set())
    # a piece with no hops no neighbors
    test_optional_moves(board2, piece13, {(6, 2), (6, 6), (7, 3), (7, 5), (5, 3), (5, 5)})
    # a piece that hops out of the board
    test_optional_moves(board2, piece14, {(11, 1), (11, 5), (12, 2), (12, 4), (10, 4)})

    test_move_piece(board2, piece4.get_location(), (10, 10), True)
    test_move_piece(board2, piece4.get_location(), (10, 10), False)  # already moved
    test_move_piece(board2, piece4.get_location(), (10, 11), False)  # not a valid move
    test_move_piece(board2, piece4.get_location(), (10, 14), False)  # not a valid move

    test_get_piece_by_coordinates(board2, (0, 12), piece)
    test_get_piece_by_coordinates(board2, (1, 11), piece2)
    test_get_piece_by_coordinates(board2, (2, 14), piece3)

if __name__ == '__main__':
    test_board()



