import pygame
from pygame import Surface
from typing import Tuple, List, Optional, Set, Union
from .piece import Piece
from .constants import BLACK, WHITE, ROWS, COLS, SQUARE_SIZE

Coordinates = Tuple[int, int]


class Board:
    """
    The Board class represents the game board
    """

    def __init__(self) -> None:
        """
        A constructor for a Board object.
        """
        self.__graphic_board: list[list[Union[int, Piece, str]]] = []
        self.create_board()
        self.valid_cells = self.cell_list()
        self.pieces: dict[Coordinates, Piece] = {}

    def create_board(self) -> None:
        """
        this function creates the graphic board of the game in the shape of the star of david
        """
        max_width = 13  # Width of the widest row
        board_len = 17  # Number of rows
        for i in range(board_len):
            if i < 4:
                num_spaces_before = (max_width - (i + 1)) // 2
                num_spaces_after = max_width - num_spaces_before - (i + 1)
            elif i == 4 or i == 12:
                num_spaces_before = 0
                num_spaces_after = 0
            elif 4 < i < 8:
                num_spaces_before = (max_width - (board_len - i)) // 2
                num_spaces_after = max_width - num_spaces_before - (board_len - i)
            elif 8 <= i < 12:
                num_spaces_before = (max_width - (i + 1)) // 2
                num_spaces_after = max_width - num_spaces_before - (i + 1)
            else:
                num_spaces_before = (max_width - (board_len - i)) // 2
                num_spaces_after = max_width - num_spaces_before - (board_len - i)
            self.__graphic_board.append([])
            if i % 2 != 0:
                self.__graphic_board[i].append(" ")
            for j in range(max_width):
                if j < num_spaces_before or j >= max_width - num_spaces_after:
                    self.__graphic_board[i].append(" ")
                else:
                    self.__graphic_board[i].append(0)
                if j < max_width - 1:
                    self.__graphic_board[i].append(" ")

    def draw_board(self, win: Surface) -> None:
        """
        This function draws the board on the screen.
        :param win: The window to draw the board on.
        """
        win.fill(WHITE)
        for row in range(ROWS):
            for col in range(len(self.__graphic_board[row])):
                if self.__graphic_board[row][col] == " ":
                    pygame.draw.rect(win, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    pygame.draw.rect(win, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw(self, win: Surface) -> None:
        """
        This function draws the board on the screen with the pieces.
        :param win: the window to draw the board on.
        :return:
        """
        self.draw_board(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.__graphic_board[row][col]
                if piece != 0 and piece != " " and type(piece) == Piece:
                    piece.draw(win)

    def __str__(self) -> str:
        """
        This function is called when a board object is to be printed.
        :return: A string representing the current status of the board.
        """
        header = "     " + ''.join([chr(j + ord('A')) + ' ' for j in range(len(self.__graphic_board[0]))])
        sep = 10 * ' '
        str_2_print = header + sep + '\n'
        for row in range(len(self.__graphic_board)):
            numbers = str(row + 1)
            if len(numbers) == 1:
                numbers = numbers + " "
            str_2_print += numbers + "   " + " ".join(map(str, self.__graphic_board[row])).center(13 * 2 - 1) + "\n"
        return str_2_print

    def cell_content(self, coordinates: Coordinates) -> Union[Piece, int, None]:
        """
        Checks if the given coordinates are empty.
        :param coordinates: tuple of (row, col) of the coordinates to check.
        :return: The name of the piece in "coordinates", 0 if it's empty, None if the cell is not in the game.
        """
        if coordinates[0] < 0 or coordinates[0] >= len(self.__graphic_board) or coordinates[1] < 0 or coordinates[
            1] >= len(self.__graphic_board[0]):
            return
        if self.__graphic_board[coordinates[0]][coordinates[1]] == " ":
            return
        else:
            return self.__graphic_board[coordinates[0]][coordinates[1]]

    def cell_list(self) -> List[Coordinates]:
        """
        This function returns the coordinates of game cells in this board.
        :return: list of coordinates.
        """
        cell_l = []
        for i, row in enumerate(self.__graphic_board):
            for j in range(len(row)):
                if self.cell_content((i, j)) is not None:
                    cell_l.append((i, j))
        return cell_l

    def add_piece(self, piece: Piece) -> bool:
        """
    #     Adds a piece to the board.
    #     :param piece: piece object to add.
    #     :return: True upon success, False if failed.
    #     """
        if piece.get_location() not in self.pieces.keys():
            if piece.get_location() in self.valid_cells:
                if self.cell_content(piece.get_location()) == 0:
                    self.__graphic_board[piece.get_location()[0]][piece.get_location()[1]] = piece
                    self.pieces[piece.get_location()] = piece
                    return True
        return False

    def get_around(self, location: Coordinates) -> Set[Coordinates]:
        """
        This function returns the coordinates of the cells around the given location.
        :param location:
        :return: set of coordinates.
        """
        x = location[0]
        y = location[1]
        around: Set[Coordinates] = set()
        all_cells = self.valid_cells
        if (x, y) not in all_cells:
            return around
        surrounding = {(x - 1, y - 1), (x - 1, y + 1), (x, y - 2), (x, y + 2), (x + 1, y - 1), (x + 1, y + 1)}
        for cord in surrounding:
            if cord in all_cells:
                around.add(cord)
        return around

    def optional_moves(self, piece: Union[Piece,None]) -> Set[Coordinates]:
        """
        This function returns the optional moves for a given piece.
        :param piece:
        :return: set of coordinates.
        """
        moves: Set[Coordinates] = set()
        if piece != None:
            x = piece.get_location()[0]
            y = piece.get_location()[1]
            around = self.get_around((x, y))

            filled = set()
            if around == set():
                return moves
            for cord in around:
                if self.cell_content(cord) == 0:
                    moves.add(cord)
                else:
                    filled.add(cord)
            if len(list(moves)) == 6:
                return moves
            else:
                for cord in filled:
                    a = cord[0] + (cord[0] - x)
                    b = cord[1] + (cord[1] - y)
                    prev = cord
                    moves.update(self.hops((a, b), prev))
        return moves

    def hops(self, cord: Coordinates, prev: Coordinates, visited: Union[Set[Coordinates],None] = None) -> Set[Coordinates]:
        """
        This function returns the possible hops from a given location.
        :param cord: the location to hop from.
        :param prev: the previous location.
        :param visited: set of visited locations.
        :return: set of coordinates.
        """
        if visited is None:
            visited = set()
        moves: Set[Coordinates] = set()
        a = cord[0]
        b = cord[1]
        if self.cell_content((a, b)) != 0 or (a, b) in visited:
            return moves
        else:
            visited.add((a, b))
            moves.add((a, b))
            around = self.get_around((a, b))
            if prev in around:
                around.remove(prev)
            for c in around:
                if self.cell_content(c) != 0:
                    x = c[0] + (c[0] - a)
                    y = c[1] + (c[1] - b)
                    prev = c
                    moves.update(self.hops((x, y), prev, visited))
        return moves

    def get_all_pieces_locations(self) -> List[Coordinates]:
        """
        This function returns the locations of all the pieces in the board.
        :return: list of coordinates.
        """
        return [piece.get_location() for piece in self.pieces.values()]

    def get_piece(self, location: Coordinates) -> Union[Piece, int, str, None]:
        """
        This function returns the piece in the given location.
        :param location: the location of the piece.
        :return: piece object.
        """
        if location in self.cell_list():
            return self.__graphic_board[location[0]][location[1]]

    def move_piece(self, piece_loc: Coordinates, destination: Coordinates) -> bool:
        """
        This function moves a piece from one location to another.
        :param piece_loc: the location of the piece to move.
        :param destination: the destination location.
        :return: True upon success, False if failed.
        """
        # print(piece_loc, destination)
        if piece_loc in self.get_all_pieces_locations() and piece_loc in self.pieces:
            piece = self.pieces[piece_loc]
            if destination in self.optional_moves(piece):
                current_loc = piece.get_location()
                if current_loc is not None and destination is not None:
                    # move the piece in the graphic board
                    self.__graphic_board[current_loc[0]][current_loc[1]] = 0
                    self.__graphic_board[destination[0]][destination[1]] = piece
                    # change the location of the piece in the piece object
                    piece.move(destination)
                    # change the location of the piece in the pieces dictionary
                    self.pieces.pop(piece_loc)
                    self.pieces[destination] = piece

                    return True
        return False

    def get_graphic_board(self) -> List[List[str]]:
        """
        This function returns the graphic board of the game.
        """
        return self.__graphic_board

    def get_piece_by_coordinates(self, piece_coords: Coordinates) -> Optional[Piece]:
        """
        This function returns the piece in the given coordinates.
        :param piece_coords:
        :return: piece object.
        """
        return self.pieces[piece_coords]