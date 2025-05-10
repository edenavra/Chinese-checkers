import os.path
import pygame
import sys
from chinese_checkers.constants import WIDTH, HEIGHT
from chinese_checkers.game import Game


def main() -> None:


    run = True
    clock = pygame.time.Clock()

    game = Game(WIN)

    while run:
        clock.tick(FPS)
        play_again = True
        while play_again:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    if game.log_file is not None:
                        game.log_game_end("Quit Game")
                else:
                    game.play(event)  # Pass the event to the game to handle
                    if game.is_end_game():
                        counter = 0
                        answer = ""
                        while counter < 1:
                            answer = input("Do you want to play again? (y/n): ")
                            if answer.lower() != "y" and answer.lower() != "n":
                                print("Invalid input. Please enter 'y' or 'n'")
                                continue
                            else:
                                counter += 1
                        if answer.lower() == "y":
                            game = Game(WIN)
                            play_again = True
                        elif answer.lower() == "n":
                            play_again = False
                            run = False
                            break
                        break

            game.update()  # Update the game state and draw the board

    pygame.quit()
    sys.exit()

def help() -> None:
    """
    This function prints the help message for the user, that contains the rules of the game.
    """
    print("Welcome to Chinese Checkers!" + "\n" +
            "The game is played on a star-shaped board with 121 spaces." + "\n" +
            "The you can play with 2, 3, 4, or 6 players." + "\n" +
            "Each player starts with 10 pieces placed in one of the corners of the star." + "\n" +
            "The goal of the game is to move all your pieces to the opposite corner of the star." + "\n" +
            "Players take turns moving one piece at a time." + "\n" +
            "A piece can move to an adjacent space or jump over other pieces." + "\n" +
            "Choose the piece that you want to move,"+ "\n" +
            "and the computer will mark the valid spaces that you can move the piece to." + "\n" +
            "The game ends when one player moves all their pieces to the opposite corner." + "\n" +
            "The player that moves all their pieces to the opposite corner wins the game." + "\n" +
            "You can choose to play a new game or upload a previous game by uploading a log file." + "\n" +
            "Good luck and have fun playing Chinese Checkers!")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            help()
            print("To run the game, please run the main.py file without any arguments, or press the run button.")
    else:
        pygame.init()
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chinese Checkers")

        FPS = 60

        main()

