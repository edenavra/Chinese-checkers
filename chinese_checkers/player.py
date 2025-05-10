import pygame
from pygame import Surface
import random
from typing import Tuple, Optional, Set, Dict, Union
from .piece import Piece

Coordinates = Tuple[int, int]


class Player:
    """
    A class representing a player in the game.
    """

    def __init__(self, name: str, color: Tuple[int, int, int], is_computer: bool = False) -> None:
        """
        A constructor for a Player object.
        :param color: A tuple representing the Player's color in rbg.
        :param name: A string representing the Player's name.
        :param is_computer: A boolean representing if the player is a computer player.
        """
        self.color = color
        self.__pieces: Dict[Coordinates, Piece] = {}
        self.target_locs: Dict[Coordinates, Union[None,Piece,int,str]]= {}
        self.__number_of_wins = 0
        self.__number_of_losses = 0
        self.name = name
        self.is_winner = self.check_if_winner()
        self.is_computer = is_computer

    def get_name(self) -> str:
        """
        :return: The name of this Player.
        """
        return self.name

    def add_win(self) -> None:
        """
        This function adds a win to the player's number of wins.
        """
        self.__number_of_wins += 1

    def add_loss(self) -> None:
        """
        This function adds a loss to the player's number of losses.
        """
        self.__number_of_losses += 1

    def get_number_of_wins(self) -> int:
        """
        :return: The number of wins of this Player.
        """
        return self.__number_of_wins

    def get_number_of_losses(self) -> int:
        """
        :return: The number of losses of this Player.
        """
        return self.__number_of_losses

    def move_piece(self, location: Coordinates, new_loc: Coordinates) -> bool:
        """
        This function moves a piece from one location to another and updated the piece dict and the target dict.
        :param location: The current location of the piece.
        :param new_loc: The new location of the piece.
        :return: True if the move was successful, False otherwise.
        """
        if location not in self.__pieces.keys() or new_loc in self.__pieces.keys():
            return False
        piece = self.__pieces[location]
        self.__pieces.pop(location)
        self.__pieces[new_loc] = piece

        if location in self.target_locs.keys():
            self.target_locs[location] = 0

        if new_loc in self.target_locs.keys():
            self.target_locs[new_loc] = piece
        return True

    def check_if_winner(self) -> bool:
        """
        This function checks if the player has won the game.
        :return: True if the player has won, False otherwise.
        """
        if self.target_locs:
            for piece in self.target_locs.values():
                if piece is None or piece == 0:
                    return False
                else:
                    if piece.get_color() != self.color:
                        return False
            return True
        return False

    def get_color(self) -> Union[None,Tuple[int, int, int]]:
        """
        :return: The color of the Player.
        """
        if self is not None:
            return self.color

    def add_piece(self, piece: Piece) -> None:
        """
        This function adds a piece to the player's pieces list.
        :param piece: A Piece object to add to the player's pieces list.
        """
        self.__pieces[piece.get_location()] = piece

    def get_pieces(self) -> Dict[Coordinates, Piece]:
        """
        :return: A list of the player's pieces.
        """
        return self.__pieces

    def add_target_loc(self, loc: Coordinates) -> None:
        """
        This function adds a target location to the player's target locations.
        :param loc: A tuple representing the target location.
        """
        self.target_locs[loc] = 0

    def get_target_locs(self) -> dict[Coordinates, None]:
        """
        :return: A list of the player's target locations.
        """
        return self.target_locs

    def check_if_computer(self) -> bool:
        """
        :return: True if the player is a computer player, False otherwise.
        """
        return self.is_computer

    def computer_select_piece(self) -> Union[Piece, None]:
        """
        This function selects a random piece from the player's pieces.
        :return: A Piece object representing the selected piece.
        """
        if self.__pieces:
            return random.choice(list(self.__pieces.values()))
        return None

    def computer_select_destination(self, valid_moves: Set[Coordinates]) -> Coordinates:
        """
        This function selects a random destination from the given valid moves.
        :param valid_moves: A set of valid moves.
        :return: A tuple representing the selected destination.
        """
        return random.choice(list(valid_moves))

