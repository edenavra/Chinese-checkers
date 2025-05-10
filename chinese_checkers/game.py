import os
import sys
import datetime
import pygame
import ast
from pygame import Surface
from pygame.event import Event
from typing import Tuple, List, Optional, Union, Set, Dict
from .piece import Piece
from .player import Player
from .board import Board
from .constants import BLACK, SQUARE_SIZE, RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN, WIDTH, HEIGHT

Coordinates = Tuple[int, int]


class Game:
    """
    A class representing a game.
    """

    def __init__(self, win: Surface, log_file: Union[str, None] = None) -> None:
        """
        A constructor for a Game object.
        :param board: A Board object representing the game board.
        """
        self.win = win
        self.board = Board()
        self.players: Dict[str, Player] = {}
        self.num_of_players = 0
        self.num_of_computers = 0
        self.turn: Union[Player,None] = None
        self.__winner: Union[Player,None] = None
        self.selected_piece: Union[Piece,None] = None
        self.valid_moves: Set[Coordinates] = set()
        self.is_valid_move = True
        self.log_file = log_file
        self.is_reloaded: bool = self.ask_if_load_game()

        if not self.is_reloaded:
            self._init_settings()
        else:
            if self.log_file is not None:
                self.load_settings()
                self._reloaded_settings()
                self.load_game()

    def update(self) -> None:
        """
        This function updates the game's screen.
        :return:
        """
        self.board.draw(self.win)
        self.draw_current_player(self.win)
        if not self.is_valid_move:
            self.draw_text(self.win, "Invalid move, please select again.", BLACK, WIDTH // 2, 15 * HEIGHT // 20)
        self.draw_valid_moves(self.valid_moves)
        if self.is_end_game():
            if self.get_winner() is not None:
                self.draw_text(self.win, f"The winner is: {self.get_winner().get_name()}",
                               self.get_winner().get_color(),
                               WIDTH // 2, 16 * HEIGHT // 20)
            self.draw_scores(self.win)
        pygame.display.update()

    def _init_settings(self) -> None:
        """
        This function initializes the settings of a new game.
        :return:
        """
        self.ask_if_log_game()
        if self.log_file is not None:
            with open(self.log_file, "w") as f:
                pass
        self.players_settings_from_user()
        self.add_players()
        self.place_pieces_on_board()
        self.add_targets_to_players()
        self.change_turn()

    def _reloaded_settings(self) -> None:
        """
        This function initializes the settings of a reloaded game.
        :return:
        """
        self.place_pieces_on_board()
        self.add_targets_to_players()
        self.change_turn()

    # These functions are for setting up the game
    def is_int(self, s: str) -> bool:
        """
        Checks if a string can be cast to an integer
        """
        try:
            int(s)
            return True
        except ValueError:
            return False

    def players_settings_from_user(self) -> None:
        """
        This function gets input from the user about the quantities of the players.
        :return:
        """
        counter = 0
        while counter == 0:
            num_of_players = input("Enter the number of players (2,3,4 or 6): ")
            if self.is_int(num_of_players):
                int_num_of_players = int(num_of_players)
                if self.is_valid_num_of_players(int_num_of_players):
                    self.num_of_players = int_num_of_players
                    counter = 1
                else:
                    print("Invalid number of players, please enter a valid number.")
            else:
                print("Invalid number of players, please enter a valid number.")
        counter2 = 0
        while counter2 == 0:
            num_of_computers = input("Enter the number of computers out of all of the players: ")
            if self.is_int(num_of_computers):
                int_num_of_computers = int(num_of_computers)
                if 0 <= int_num_of_computers < self.num_of_players:
                    self.num_of_computers = int_num_of_computers
                    counter2 = 1
            else:
                print("Invalid number of computers, please enter a valid number.")
        if self.log_file is not None:
            self.log_game_settings(self.num_of_players, self.num_of_computers)
        return

    def add_players(self) -> None:
        """
        This function creates and adds the players to the game, according to the user's input.
        """
        colors = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE]
        if self.num_of_players > 0:
            i = 0
            while i < self.num_of_players:
                if i < self.num_of_players - self.num_of_computers:
                    name = input(f"Enter the name of player {i + 1}: ")
                    if name == "" or name.isspace():
                        print("Invalid name, please enter a valid name.")
                        continue
                    color = colors[i]
                    if name not in self.players.keys():
                        player = Player(name, color)
                        self.players[name] = player
                        if self.log_file is not None:
                            self.log_players_info(name, color, False)
                        i += 1
                    else:
                        print("This name is already taken, please enter a different name.")

                else:
                    index = i - (self.num_of_players - self.num_of_computers) + 1
                    self.players[f"Computer {index}"] = Player(f"Computer {index}", colors[i], True)
                    if self.log_file is not None:
                        self.log_players_info(f"Computer {index}", colors[i], True)
                    i += 1
        return

    def is_valid_num_of_players(self, num_of_players: int) -> bool:
        """
        This function checks if the number of players is valid.
        :param num_of_players: An integer representing the number of players.
        :return: True if the number of players is valid, False otherwise.
        """
        return 2 <= num_of_players <= 6 and num_of_players != 5

    def get_num_of_players(self) -> int:
        """
        :return: The number of players in the game.
        """
        return self.num_of_players

    def calculate_first_loc(self) -> List[Coordinates]:
        """
        This function calculates the starting positions of the pieces.
        :return: A list of tuples representing the starting positions.
        """
        first_loc = []
        if self.num_of_players == 6:
            first_loc = [(0, 12), (4, 0), (9, 3), (13, 9), (9, 21), (4, 18)]
        elif self.num_of_players == 4:
            first_loc = [(4, 0), (9, 3), (9, 21), (4, 18)]
        elif self.num_of_players == 3:
            first_loc = [(0, 12), (9, 3), (9, 21)]
        elif self.num_of_players == 2:
            first_loc = [(0, 12), (13, 9)]

        return first_loc

    def calculate_starting_position(self) -> list[list[Coordinates]]:
        """
        This function calculates the starting positions of the pieces of every player
        :return:
        """
        first_loc = self.calculate_first_loc()
        starting_positions = []
        for index, first in enumerate(first_loc):
            player = []
            start_x, start_y = first
            if first in [(4, 0), (4, 18), (13, 9)]:
                for i in range(start_x, start_x + 4):
                    c = i - start_x
                    for j in range(start_y + c, start_y + 7 - c, 2):
                        player.append((i, j))
            else:
                for i in range(start_x, start_x + 4):
                    c = i - start_x
                    for j in range(start_y - c, start_y + c + 2, 2):
                        player.append((i, j))
            starting_positions.append(player)

        return starting_positions

    def convert_start_pos_to_target_pos(self, start_pos: Coordinates) -> Union[Coordinates, None]:
        """
        This function converts the starting position to the target position.
        :param start_pos: A tuple representing the starting position.
        :return: A tuple representing the target position.
        """
        if start_pos == (0, 12):
            return (13, 9)
        if start_pos == (4, 0):
            return (9, 21)
        if start_pos == (9, 3):
            return (4, 18)
        if start_pos == (13, 9):
            return (0, 12)
        if start_pos == (9, 21):
            return (4, 0)
        if start_pos == (4, 18):
            return (9, 3)

    def calculate_target_position(self) -> list[list[Coordinates]]:
        """
        This function calculates the target positions of the pieces of every player
        :return:
        """
        target_positions = []
        for index, first in enumerate(self.calculate_first_loc()):
            player = []
            start_x, start_y = self.convert_start_pos_to_target_pos(first)
            if first not in [(4, 0), (4, 18), (13, 9)]:
                for i in range(start_x, start_x + 4):
                    c = i - start_x
                    for j in range(start_y + c, start_y + 7 - c, 2):
                        player.append((i, j))
            else:
                for i in range(start_x, start_x + 4):
                    c = i - start_x
                    for j in range(start_y - c, start_y + c + 2, 2):
                        player.append((i, j))
            target_positions.append(player)

        return target_positions

    def add_targets_to_players(self) -> None:
        """
        This function adds the target positions to the players.
        """
        target_positions = self.calculate_target_position()
        for player, positions in zip(self.players.values(), target_positions):
            for i, position in enumerate(positions):
                player.add_target_loc(position)

    def place_pieces_on_board(self) -> None:
        """
        This function places the pieces on the board and adds the pieces to the players piece dictionary.
        :param self:
        :return:
        """
        starting_positions = self.calculate_starting_position()
        for player, positions in zip(self.players.values(), starting_positions):
            for i, position in enumerate(positions):
                piece = Piece(player.get_color(), f"{player.get_color()}{i}", position)
                self.board.add_piece(piece)
                player.add_piece(piece)

    def get_board(self) -> Board:
        """
        :return: The board of the game.
        """
        return self.board

    # These functions are for the activ part of the game
    def get_pos_from_mouse(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """
        This function gets the position of the mouse.
        :param pos: the position of the mouse.
        :return: the row and column of the mouse on the board.
        """
        x, y = pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        return (row, col)

    def handle_events(self, event: Union = None) -> None:
        """
        This function handles the events of the game, such as pressing the mouse.
        :param event:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                loc = self.get_pos_from_mouse(pos)
                self.select(loc)

    def select(self, loc: Coordinates) -> bool:
        """
        This function selects a piece on the board and trys to move it to a selected location.
        :param loc: A tuple representing the location of the piece.
        """
        if not self.selected_piece:
            piece = self.board.get_piece(loc)
            if piece is None or piece == 0 or piece == " ":
                self.is_valid_move = False
                return False
            elif piece.get_color() is not None and self.turn is not None and piece.get_color() == self.turn.get_color():
                self.selected_piece = piece
                self.valid_moves = self.board.optional_moves(piece)
                self.is_valid_move = True
                return True  # Piece selection successful
            else:
                self.is_valid_move = False
                return False  # Invalid piece selection, prompt user to select again
        else:
            result = self._move(loc)
            if not result:
                self.is_valid_move = False
                # If the move is invalid, reset the selected piece and valid moves
                self.selected_piece = None
                self.valid_moves = set()
                return False  # Indicate that the move was invalid
            else:
                self.is_valid_move = True
                return True  # Move successful

    def computer_move(self) -> bool:
        """
        This method executes a move for a computer player.
        :return: True if the move is successful, False otherwise.
        """
        self.selected_piece = self.get_current_player().computer_select_piece()
        self.valid_moves = self.board.optional_moves(self.selected_piece)
        if self.valid_moves:
            destination = self.get_current_player().computer_select_destination(self.valid_moves)
            return self._move(destination)
        else:
            return False  # No valid moves available for the computer player

    def _move(self, loc: Coordinates) -> bool:
        """
        This function moves a piece to a selected location.
        :param loc: A tuple representing the location of the destination.
        :return:
        """
        piece = self.board.get_piece(loc)
        cur_piece = self.selected_piece
        if cur_piece is not None:
            cur_loc = cur_piece.get_location()
            if self.selected_piece and piece == 0 and loc in self.valid_moves:
                self.board.move_piece(cur_loc, loc)
                self.get_current_player().move_piece(cur_loc, loc)
                if self.log_file is not None:
                    self.log_turn(self.get_current_player().get_name(), cur_piece.get_id(), cur_loc, loc)
                self.selected_piece = None
                self.change_turn()

                return True
        return False

    def change_turn(self) -> None:
        """
        This function changes the turn of the game.
        """
        self.valid_moves = set()
        player_names = list(self.players.keys())
        if player_names != [] and self.players != {}:
            if self.turn is None:
                self.turn = self.players[player_names[0]]
            else:
                index = player_names.index(self.turn.get_name())
                if index == len(player_names) - 1:
                    self.turn = self.players[player_names[0]]
                else:
                    self.turn = self.players[player_names[index + 1]]


    def get_current_player(self) -> Union[Player, None]:
        """
        :return: The current player of the game.
        """
        return self.turn

    def single_turn(self, event: Union = None) -> bool:
        """
        This function represents a single turn in the game.
        """
        if self.get_current_player().check_if_computer():
            computer_move_result = self.computer_move()
            if computer_move_result:
                # Computer move successful
                self.is_valid_move = True
                return True
            else:
                # Computer move failed
                self.is_valid_move = False
                self.selected_piece = None
                self.valid_moves = set()
                return False
        else:
            self.handle_events(event)
            return True

    def play(self, event: Event = None) -> None:
        """
        The main driver of the Game. Manages the game until completion.
        """
        self.update()
        while self.is_end_game() == False and self.single_turn() == True:
            self.single_turn(event)
            self.update()
        if self.is_end_game():
            self.update_wins_and_losses()
            if self.log_file is not None:
                self.log_game_end("Game Over")
        self.update()

    def get_players(self) -> Dict[str, Union[Player,None]]:
        """
        :return: The players of the game.
        """
        return self.players

    # These functions are for the end of the game
    def is_end_game(self) -> bool:
        """
        This function checks if the game is over.
        :return: True if the game is over, False otherwise.
        """
        for player in self.players.values():
            if player is not None:
                if player.check_if_winner():
                    self.set_winner(player)
                    if self.log_file is not None:
                        self.log_game_end("Game Over")
                    return True
        return False

    def set_winner(self, player: Player) -> None:
        """
        This function sets the winner of the game.
        :param player: The player that won the game.
        """
        self.__winner = player

    def get_winner(self) -> Union[Player, None]:
        """
        :return: The winner of the game.
        """
        return self.__winner

    def update_wins_and_losses(self) -> None:
        """
        This function updates the wins and losses of the players.
        """
        if self.get_winner() == None:
            return
        else:
            for player in self.players.values():
                if player == self.get_winner():
                    player.add_win()
                else:
                    player.add_loss()

    def get_scores(self) -> dict[str, dict[str, int]]:
        """
        :return: A dictionary representing the scores of the players.
        """
        scores = {}
        for player in self.players.values():
            win_lose = {"wins": player.get_number_of_wins(), "losses": player.get_number_of_losses()}
            scores[player.get_name()] = win_lose
        return scores

    # these functions are for drawing

    def draw_current_player(self, win: Surface) -> None:
        """
        This function draws the current player on the screen.
        :param win: the window to draw on.
        :return:
        """
        font = pygame.font.Font(None, 36)
        player_name = f"Current Player: {self.get_current_player().get_name()}"
        player_color = self.get_current_player().get_color()
        text_surface = font.render(player_name, True, player_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (WIDTH // 2, 14 * HEIGHT // 20)
        win.blit(text_surface, text_rect)

    def draw_text(self, win: Surface, text: str, color: Tuple[int, int, int], x: int, y: int) -> None:
        """
        This function draws text on the screen.
        :param win: The window to draw on.
        :param text: The text to draw.
        :param color: The color of the text.
        :param x: The x coordinate of the text.
        :param y: The y coordinate of the text.
        :return:
        """
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        win.blit(text_surface, text_rect)

    def draw_valid_moves(self, moves: Set[Coordinates]) -> None:
        """
        This function draws the valid moves of the selected piece on the screen.
        :param moves:
        :return:
        """
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, CYAN,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 7)

    def draw_scores(self, win: Surface) -> None:
        """
        This function draws the scores of the players on the screen.
        :param win: The window to draw on.
        """
        scores = self.get_scores()
        font = pygame.font.Font(None, 20)
        y = 17 * HEIGHT // 20
        for player, score in scores.items():
            text = f"{player}: {score['wins']} wins, {score['losses']} losses"
            text_surface = font.render(text, True, self.players[player].get_color())
            text_rect = text_surface.get_rect()
            text_rect.center = (WIDTH // 2, y)
            win.blit(text_surface, text_rect)
            y += 25

    # all function below are for the log file

    def ask_if_log_game(self) -> None:
        """
        This function asks the user if they want to log the game.
        :return: True if the user wants to log the game, False otherwise.
        """
        answer = input("Do you want to log the game? (yes/no): ")
        while answer.lower() not in ["yes", "no"]:
            print("Invalid input. Please enter 'yes' or 'no'.")
            answer = input("Do you want to log the game? (yes/no): ")
        if answer.lower() == "yes":
            log_file_name = input("Enter the name of the log file: ")
            self.log_file = log_file_name + ".txt"
        else:
            self.log_file = None

    def ask_if_load_game(self) -> bool:
        """
        This function asks the user if they want to load a game.
        :return: True if the user wants to load a game, False otherwise.
        """
        upload = input("Do you want to upload a previous game? (yes/no): ")
        while upload.lower() != "yes" and upload.lower() != "no":
            print("Invalid input. Please enter 'yes' or 'no'")
            upload = input("Do you want to upload a previous game? (yes/no): ")
        if upload.lower() == "yes":
            file_name = input("Enter the name of the file you want to upload without .txt: ")
            log_file = file_name + ".txt"
            while (not os.path.isfile(log_file) or os.path.getsize(log_file) == 0) and file_name != "new":
                print("The file does not exist or is empty. Please enter a valid file name." + "\n" +
                      "if you want to start a new game enter 'new'")
                file_name = input("Enter the name of the file you want to upload: ")
                if file_name != "new":
                    log_file = file_name + ".txt"
            if file_name != "new":
                if os.path.isfile(log_file) and os.path.getsize(log_file) > 0:
                    with open(log_file, "r") as f:
                        last_line = f.readlines()[-1]
                        if not last_line.endswith("Game Over\n"):
                            answer = input("Do you want to continue the previous game? (yes/no): ")
                            while answer.lower() != "yes" and answer.lower() != "no":
                                print("Invalid input. Please enter 'yes' or 'no'")
                                answer = input("Do you want to continue the previous game? (yes/no): ")
                            if answer.lower() == "yes":
                                self.log_file = log_file
                                return True
                            else:
                                print("Starting a new game.")
                                self.log_file = None
                                return False
                        else:
                            print("The game is over. Please start a new game.")
                            self.log_file = None
                            return False
                else:
                    print("The file does not exist or is empty. Please start a new game.")
                    self.log_file = None
                    return False
            else:
                print("Starting a new game.")
                self.log_file = None
                return False
        else:
            print("Starting a new game.")
            self.log_file = None
            return False

    def log_game_settings(self, number_of_players: int, number_of_computers: int) -> None:
        """
        This function logs the game settings to a text file.
        :param number_of_players: The number of players in the game.
        :param number_of_computers: The number of computers in the game.
        """
        with open(self.log_file, "a") as file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp},Game Settings: +{number_of_players}+{number_of_computers}+Game Settings\n")

    def log_players_info(self, players_name: str, players_color: Tuple[int, int, int], is_computer: bool) -> None:
        """
        This function logs the players' information to a text file.
        :param players_name: The name of the player.
        :param players_color: The color of the player.
        :param is_computer: True if the player is a computer, False otherwise.
        """
        with open(self.log_file, "a") as file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp},Game Settings: +{players_name}+{players_color}+{is_computer}+Players Info\n")

    def log_turn(self, player_name: str, piece_id: str, piece_location: Coordinates, destination: Coordinates) -> None:
        """
        This function logs the current turn of the game and writes it to a text file.
        :param player_name: The name of the player.
        :param piece_id: The id of the piece.
        :param piece_location: The location of the piece.
        :param destination: The destination of the piece.
        """
        with open(self.log_file, "a") as file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp}+{player_name}+{piece_id}+{piece_location}+{destination}+Turn\n")

    def log_game_end(self, msg: str) -> None:
        """
        Log that the game has ended in the log file.
        :param msg: A message to write to the log file.
        """
        with open(self.log_file, "a") as file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp}+{msg}\n")

    def load_settings(self) -> None:
        """
        This function loads the game settings from a log file.
        """
        file_name = self.log_file
        try:
            with open(file_name, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if line.endswith("Game Settings\n"):
                        num_of_players, num_of_computers = self.parse_settings_line(line)
                        self.num_of_players = num_of_players
                        self.num_of_computers = num_of_computers
                    elif line.endswith("Players Info\n"):
                        player_name, player_color, is_computer = self.parse_players_info_line(line)
                        self.players[player_name] = Player(player_name, player_color, is_computer)
        except Exception as e:
            print("An error occurred:", e)

    def parse_settings_line(self, line: str) -> Tuple[int, int]:
        """
        This function parses a setting line from the log file.
        :param line:
        :return:
        """
        components = line.split("+")
        num_of_players = int(components[1])
        num_of_computers = int(components[2])
        return num_of_players, num_of_computers

    def parse_players_info_line(self, line: str) -> tuple[str, Union[tuple[int, int, int], Tuple[int,...]], bool]:
        """
        This function parses a player info line from the log file.
        :param line:
        :return:
        """
        components = line.split("+")
        player_name = components[1]
        color = components[2].replace(" ", "")
        player_colore_tuple = ast.literal_eval(color)
        player_color = tuple(map(int, player_colore_tuple))
        is_computer = components[3].lower() == "true"
        return player_name, player_color, is_computer

    def load_game(self) -> None:
        """
        This function loads a game from a log file.
        """
        file_name = self.log_file
        try:
            with open(file_name, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if line.endswith("Turn\n"):
                        player_name, piece_id, piece_loc, destination = self.parse_log_line(line)
                        self.update_game_state(player_name, piece_loc, destination)
                self.update()
        except Exception as e:
            print("An error occurred:", e)

    def parse_log_line(self, line: str) -> Tuple[str, str, Coordinates, Coordinates]:
        """
        This function parses a turn line from the log file.
        :param line: A line from the log file.
        :return: The player's name, the piece's id, the piece's location, and the destination.
        """
        components = line.split("+")
        player_name = components[1]
        piece_id = components[2]
        piece_loc_tuple = ast.literal_eval(components[3])
        piece_loc = tuple(map(int, piece_loc_tuple))
        destination_tuple = ast.literal_eval(components[4])
        destination = tuple(map(int, destination_tuple))
        return player_name, piece_id, piece_loc, destination

    def update_game_state(self, player_name: str, piece_coords: Coordinates, destination_coords: Coordinates) -> None:
        """
        This function updates the game state based on the log file.
        :param player_name: The name of the player.
        :param piece_coords: The coordinates of the piece to move.
        :param destination_coords: The destination coordinates.
        :return:
        """
        # Retrieve the player object based on the player's name
        player = self.get_player_by_name(player_name)
        self.current_player = player

        # Retrieve the piece object based on its coordinates
        piece = self.board.get_piece_by_coordinates(piece_coords)

        # Move the piece to the new destination
        if piece is not None:
            self.board.move_piece(piece.get_location(), destination_coords)
            self.get_current_player().move_piece(piece_coords, destination_coords)
            self.board.draw(self.win)
            pygame.display.update()

    def get_player_by_name(self, player_name: str) -> Player:
        """
        This function retrieves a player object based on the player's name.
        :param player_name: The name of the player.
        :return: Player object.
        """
        return self.players[player_name]

    # these functions are for testing

    def get_selected_piece(self) -> Union[Piece,None]:
        """
        :return: The selected piece of the game.
        """
        return self.selected_piece

    def set_players(self, players: Dict[str,Player]) -> None:
        """
        :param players: A dictionary representing the players of the game.
        """
        self.players = players
