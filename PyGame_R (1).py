import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
CARD_WIDTH, CARD_HEIGHT = 80, 120
FPS = 60
BUTTON_WIDTH, BUTTON_HEIGHT = 150, 50
END_TURN_BUTTON_WIDTH, END_TURN_BUTTON_HEIGHT = 200, 60

# Colors
GRAY = (195, 195, 195)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Card types
NUMBER_CARD = 0
ROLL_CARD = 1
SWITCH_CARD = 2

class Card:
    def __init__(self, color, value, card_type):
        self.color = color
        self.value = value
        self.type = card_type
        self.rect = pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT)

    def draw(self, screen, x, y):
        self.rect.topleft = (x, y)
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        if self.type == NUMBER_CARD:
            text = font.render(str(self.value), True, BLACK)
        elif self.type == ROLL_CARD:
            text = font.render("Roll", True, BLACK)
        else:  # SWITCH_CARD
            text = font.render("Switch", True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

class Player:
    def __init__(self, name):
        self.name = name
        self.bench = []
        self.bank = []

    def score(self):
        return sum(card.value for card in self.bench + self.bank if card.type == NUMBER_CARD)

class PushGame:
    def __init__(self, player_names):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Push")
        self.clock = pygame.time.Clock()
        self.running = True
        self.players = [Player(name) for name in player_names]
        self.current_player = 0
        self.deck = self.create_deck()
        self.columns = [[], [], []]
        self.direction = 1  # 1 for clockwise, -1 for counterclockwise
        self.switch_pile = []
        self.font = pygame.font.Font(None, 36)
        self.current_card = None
        self.action_phase = True  # True for choosing action, False for placing cards
        self.end_turn_button = pygame.Rect(SCREEN_WIDTH - END_TURN_BUTTON_WIDTH - 50, SCREEN_HEIGHT - END_TURN_BUTTON_HEIGHT - 50, END_TURN_BUTTON_WIDTH, END_TURN_BUTTON_HEIGHT)

    def create_deck(self):
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE]
        deck = [Card(color, number, NUMBER_CARD) for color in colors for number in range(1, 7) for _ in range(3)]
        deck += [Card(GRAY, 0, ROLL_CARD) for _ in range(18)]
        deck += [Card(WHITE, 0, SWITCH_CARD) for _ in range(12)]
        random.shuffle(deck)
        return deck

    def draw_card(self):
        return self.deck.pop() if self.deck else None

    def can_add_to_column(self, card, column):
        if card.type == ROLL_CARD:
            return not any(c.type == ROLL_CARD for c in column)
        return not any(c.color == card.color or c.value == card.value for c in column if c.type == NUMBER_CARD)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.action_phase:
                    if self.end_turn_button.collidepoint(event.pos):
                        self.end_turn()
                    elif self.draw_button.collidepoint(event.pos) and not self.current_card:
                        self.push()
                else:
                    if event.button == 1:  # Left mouse button
                        self.handle_card_placement(event.pos)

    def push(self):
        card = self.draw_card()
        if not card:
            return
        self.current_card = card
        self.action_phase = False

    def handle_card_placement(self, mouse_pos):
        for i, col in enumerate(self.columns):
            col_x = 50 + i * (CARD_WIDTH + 10)
            col_y = 50
            col_rect = pygame.Rect(col_x, col_y, CARD_WIDTH, CARD_HEIGHT)  # Updated to show empty stacks
            if col_rect.collidepoint(mouse_pos):
                if self.can_add_to_column(self.current_card, col):
                    col.append(self.current_card)
                    self.current_card = None
                    self.action_phase = True
                    return
        if self.current_card and self.current_card.type == SWITCH_CARD:
            self.switch_pile.append(self.current_card)
            self.direction *= -1
            self.current_card = None
            self.action_phase = True

    def bank_cards(self):
        player = self.players[self.current_player]
        if player.bench:
            color_to_bank = next((c.color for c in player.bench if c.type == NUMBER_CARD), None)
            if color_to_bank:
                player.bank.extend([c for c in player.bench if c.color == color_to_bank])
                player.bench = [c for c in player.bench if c.color != color_to_bank]
            self.current_player = (self.current_player + self.direction) % len(self.players)
            self.action_phase = True

    def end_turn(self):
        self.current_player = (self.current_player + self.direction) % len(self.players)
        self.action_phase = True
        self.current_card = None  # Ensure no card is held over between turns

    def draw(self):
        self.screen.fill(WHITE)
        # Draw action buttons
        self.bank_button = pygame.Rect(50, SCREEN_HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.draw_button = pygame.Rect(250, SCREEN_HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(self.screen, GREEN, self.bank_button)
        pygame.draw.rect(self.screen, BLUE, self.draw_button)
        bank_text = self.font.render("Bank", True, BLACK)
        draw_text = self.font.render("Draw", True, BLACK)
        self.screen.blit(bank_text, (self.bank_button.x + 20, self.bank_button.y + 10))
        self.screen.blit(draw_text, (self.draw_button.x + 20, self.draw_button.y + 10))
        # Draw end turn button
        pygame.draw.rect(self.screen, RED, self.end_turn_button)
        end_turn_text = self.font.render("End Turn", True, WHITE)
        self.screen.blit(end_turn_text, (self.end_turn_button.x + 20, self.end_turn_button.y + 10))
        # Draw columns, including empty ones
        for i, column in enumerate(self.columns):
            col_x = 50 + i * (CARD_WIDTH + 10)
            col_y = 50
            pygame.draw.rect(self.screen, GRAY, (col_x, col_y, CARD_WIDTH, CARD_HEIGHT), 2)  # Draw empty stack
            for j, card in enumerate(column):
                card.draw(self.screen, col_x, col_y + j * 30)
        # Draw player info
        for i, player in enumerate(self.players):
            y = 400 + i * 100
            text = self.font.render(f"{player.name} (Bench: {len(player.bench)}, Bank: {len(player.bank)})", True, BLACK)
            self.screen.blit(text, (50, y))
            for j, card in enumerate(player.bench):
                card.draw(self.screen, 450 + j * 50, y + 10)
        # Draw current card if any
        if self.current_card:
            self.current_card.draw(self.screen, SCREEN_WIDTH - CARD_WIDTH - 50, SCREEN_HEIGHT // 2 - CARD_HEIGHT // 2)
        pygame.display.flip()

    def run(self):
        while self.running and self.deck:
            self.clock.tick(FPS)
            self.handle_events()
            self.draw()
        # Game over, calculate scores
        scores = [(player.name, player.score()) for player in self.players]
        scores.sort(key=lambda x: x[1], reverse=True)
        # Display final scores
        self.screen.fill(WHITE)
        for i, (name, score) in enumerate(scores):
            text = self.font.render(f"{i + 1}. {name}: {score} points", True, BLACK)
            self.screen.blit(text, (50, 50 + i * 50))
        pygame.display.flip()
        # Wait for a few seconds before quitting
        pygame.time.wait(5000)
        pygame.quit()

if __name__ == "__main__":
    game = PushGame(["Player 1", "Player 2", "Player 3"])
    game.run()