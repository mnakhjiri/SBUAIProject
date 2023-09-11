import os
import pickle
from view.colors import *
from view.fonts import *
from model.logic import *
import pygame

with open("./QLearning/q_table.pkl", "rb") as f:
    q_table = pickle.load(f)


class Button:
    def __init__(self, x, y, width, height, color, button_arg=0, text='', action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action
        self.button_arg = button_arg

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        if self.text != '':
            text_surface = default_font.render(self.text, True, WHITE)
            text_rect = text_surface.get_rect()
            text_rect.center = self.rect.center
            surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.action:
                self.action(self.button_arg)


class GameBoard:
    def __init__(self, width=780, height=650, display_caption="Connect 4", fps=60, first_turn=1,
                 game_type="ClientVSClient", game_started=False):
        self.logo = None
        self.board_image = None
        self.black_image = None
        self.red_image = None
        self.font = None
        self.window = None
        self.prune = True
        self.depth = 4
        self.game_type = game_type
        self.width = width
        self.game_started = game_started
        self.height = height
        self.display_caption = display_caption
        self.fps = fps
        self.font = default_font
        self.empty_board = np.array([[0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0]])

        self.board_state = self.empty_board.copy()
        self.global_turn = first_turn
        self.player_win = 0
        self.buttons = self.create_buttons()
        self.initialize_game()
        self.load_images()

    def initialize_game(self):
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.display_caption)

    def load_images(self):
        self.red_image = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'red.png')), (75, 75))
        self.black_image = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'black.png')), (75, 75))
        self.board_image = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'board.png')), (780, 650))
        self.logo = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'Logo.png')), (300, 175))

    def button_action(self, col):
        i = 0
        for cell in self.board_state[col]:
            if cell == 0:
                self.board_state[col][i] = self.global_turn
                if self.game_type == "ClientVSClient":
                    if self.global_turn == 1:
                        if check_win(self.board_state) != 0:
                            break
                        self.global_turn = 2
                    elif self.global_turn == 2:
                        self.global_turn = 1
                elif self.game_type == "QLearning":
                    if check_win(self.board_state) != 0:
                        break
                    row = 0
                    for i in range(len(self.board_state[col])):
                        if self.board_state[col][i] == 0:
                            row = i - 1
                            break
                    for i in np.argsort(q_table[col][row])[::-1]:
                        if drop_piece(self.board_state, 2, i):
                            break
                else:
                    if self.global_turn == 1:
                        if check_win(self.board_state) != 0:
                            break
                        col, value = minimax(self.board_state.copy(), depth=self.depth)
                        drop_piece(self.board_state, 2, col)
                break
            i += 1

    def create_buttons(self):
        buttons = []
        pos = 0
        for i in range(7):
            if i == 0:
                buttons.append(
                    Button(0, 0, 77 + 92, 592, GREEN, text='Click Me', button_arg=i, action=self.button_action))
                pos = 77 + 92 + 1
            else:
                buttons.append(Button(pos, 0, 77, 592, GREEN, text='Click Me', button_arg=i, action=self.button_action))
                pos = pos + 92 + 1
        return buttons

    def draw__reset_button(self, x, y, width, height, radius, label):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        button_rect = pygame.Rect(x, y, width, height)
        if button_rect.collidepoint(mouse_pos) and mouse_click[0]:
            self.board_state = self.empty_board.copy()
            self.global_turn = 1
            self.player_win = 0
            return True

        self.draw_button(height, label, radius, width, x, y)

        return False

    def draw_button(self, height, label, radius, width, x, y):
        pygame.draw.rect(self.window, BLUE, (x, y + radius, width, height - 2 * radius))
        pygame.draw.rect(self.window, BLUE, (x + radius, y, width - 2 * radius, height))
        pygame.draw.circle(self.window, BLUE, (x + radius, y + radius), radius)
        pygame.draw.circle(self.window, BLUE, (x + width - radius, y + radius), radius)
        pygame.draw.circle(self.window, BLUE, (x + radius, y + height - radius), radius)
        pygame.draw.circle(self.window, BLUE, (x + width - radius, y + height - radius), radius)
        text = default_font.render(label, True, WHITE)
        text_rect = text.get_rect(center=(x + width / 2, y + height / 2))
        self.window.blit(text, text_rect)

    def draw_menu_button(self, x, y, width, height, radius, label, action, depth=4):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        button_rect = pygame.Rect(x, y, width, height)
        if button_rect.collidepoint(mouse_pos) and mouse_click[0]:
            self.game_type = action
            self.depth = depth
            if self.game_started:
                self.board_state = self.empty_board.copy()
            self.game_started = not self.game_started
            return True

        self.draw_button(height, label, radius, width, x, y)

        return False

    def finish_game(self, txt, won=0):
        text_surface = alert_font.render(txt, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (self.width // 2, self.height // 2)
        if won == 1:
            bg = (0, 0, 0, 128)
        elif won == 2:
            bg = (255, 0, 0, 128)
        else:
            bg = (255, 255, 0, 128)
        transparent_surface = pygame.Surface((text_rect.width + 100, text_rect.height + 100), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, bg, (0, 0, text_rect.width + 100, text_rect.height + 100),
                         border_radius=10)

        bordered_surface = pygame.Surface((text_rect.width + 2, text_rect.height + 2), pygame.SRCALPHA)
        bordered_surface.blit(text_surface, (1, 1))
        bordered_surface.blit(text_surface, (-1, -1))
        bordered_surface.blit(text_surface, (1, -1))
        bordered_surface.blit(text_surface, (-1, 1))
        bordered_surface.blit(text_surface, (0, 0))

        self.window.blit(transparent_surface, (text_rect.left - 50, text_rect.top - 50))
        self.window.blit(bordered_surface, (text_rect.left, text_rect.top))

    def draw_window(self):
        if not self.game_started:
            self.board_state = self.empty_board.copy()
            self.global_turn = 1
            self.player_win = 0
            self.window.fill(L_BLUE)
            self.window.blit(self.logo, (250, 50))
            self.draw_menu_button(270, 220, 250, 50, 25, "Two players", "ClientVSClient")
            self.draw_menu_button(270, 290, 250, 50, 25, "Play with AI (Easy)", "ClientVSAI", 1)
            self.draw_menu_button(270, 360, 250, 50, 25, "Play with AI (Hard)", "ClientVSAI", 4)
            self.draw_menu_button(270, 430, 250, 50, 25, "QLearning", "QLearning", 4)
            pygame.display.update()
            return
        result_array = []
        cell = check_win(self.board_state)
        if cell != 0 and cell is not None:
            self.player_win = cell
            result_array = get_result_array(self.board_state)
        if self.player_win == 0 and np.any(self.board_state == 0):
            for button in self.buttons:
                button.draw(self.window)
        self.window.fill(WHITE)
        self.window.blit(self.board_image, (0, 0))

        initial_pos = [77, 34]
        if self.draw__reset_button(180, 590, 200, 50, 10, "Reset Board"):
            pass
        if self.draw_menu_button(420, 590, 200, 50, 10, "Menu", "ClientVSClient"):
            pass
        j = 0
        for col in self.board_state:
            initial_pos[1] = 34
            i = 5
            for cell in col[::-1]:
                if cell == 1:
                    self.window.blit(self.black_image, (initial_pos[0], initial_pos[1]))
                elif cell == 2:
                    self.window.blit(self.red_image, (initial_pos[0], initial_pos[1]))
                if (i, j) in result_array:
                    font = pygame.font.Font(None, 50)
                    text = font.render("W", True, WHITE)
                    text_rect = text.get_rect(center=(initial_pos[0] + 40, initial_pos[1] + 40))
                    self.window.blit(text, text_rect)

                initial_pos[1] += 92
                i -= 1
            initial_pos[0] += 92
            j += 1
        if self.player_win != 0:
            self.finish_game(txt=f"Player {self.player_win} won", won=self.player_win)
        elif not np.any(self.board_state == 0):
            self.finish_game(txt=f"Draw")
        pygame.display.update()
