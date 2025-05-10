import pygame
from pygame import Surface
from typing import Tuple, Union
from .constants import SQUARE_SIZE, COLOR_MAP

Coordinates = Tuple[int, int]


class Piece:
    """
    This class represents a piece in the game.
    """
    PADDING = 5
    OUTLINE = 1

    def __init__(self, color: Tuple[int, int, int], id_: str, location: Coordinates) -> None:
        """
        A constructor for a Piece object.
        :param id_: A string representing the Piece's id, the id is the color + the number of the piece.
        :param location: A tuple representing the Piece's head location (row,col).
        :param color: A tuple representing the Piece's color in rbg.
        """
        self.color = color
        self.__id = id_
        self.location = location
        self.x = 0
        self.y = 0
        self.calc_pos()

    def get_id(self) -> str:
        """
        :return: The id of this Piece.
        """
        return self.__id

    def get_location(self) -> Coordinates:
        """
        :return: The coordinates the Piece is in.
        """
        return self.location

    def get_color(self) -> Union[None,Tuple[int, int, int]]:
        """
        :return: The color of the Piece.
        """
        if self is not None:
            return self.color

    def move(self, destination: Coordinates) -> None:
        """
        This function moves the Piece to a new location.
        :param destination: A tuple representing the new location (row,col).
        """
        self.location = destination
        self.calc_pos()

    def calc_pos(self) -> None:
        """
        This function calculates the position of the Piece for drawing.
        :return:
        """
        if self.location:
            self.x = SQUARE_SIZE * self.location[1] + SQUARE_SIZE // 2
            self.y = SQUARE_SIZE * self.location[0] + SQUARE_SIZE // 2

    def draw(self, win: Surface) -> None:
        """
        This function draws the Piece on the screen.
        :param win: the screen to draw the Piece on.
        :return:
        """
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, (128, 128, 128), (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)

    def __str__(self) -> str:
        """
        This function is called when a Piece object is to be printed.
        :return:
        """
        return COLOR_MAP[self.color][0]
