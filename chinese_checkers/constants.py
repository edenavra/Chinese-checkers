import pygame
import sys

WIDTH = 800
HEIGHT = 800

ROWS = 17
COLS = 25

SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)
BROWN = (165, 42, 42)
TURQUOISE = (64, 224, 208)
GREY = (128, 128, 128)

COLOR_MAP = {(255, 255, 255): "white", (0, 0, 0): "black", (255, 0, 0): "red", (0, 255, 0): "green",
             (0, 0, 255): "blue", (255, 255, 0): "yellow", (255, 165, 0): "orange", (128, 0, 128): "purple",
             (0, 255, 255): "cyan", (255, 192, 203): "pink", (165, 42, 42): "brown", (64, 224, 208): "turquoise",
             (128, 128, 128): "grey"}

