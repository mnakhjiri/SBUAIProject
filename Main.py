import pygame

pygame.init()

from view import Board

FPS = 60

game_board = Board.GameBoard()


def main():
    clock = pygame.time.Clock()

    run = True
    while run:
        # frame rate
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if game_board.game_started:
                if game_board.player_win == 0:
                    for button in game_board.buttons:
                        button.handle_event(event)

        # updating window
        game_board.draw_window()

    pygame.quit()


if __name__ == "__main__":
    main()
