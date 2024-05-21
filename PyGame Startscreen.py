import pygame
import sys
# Initialize Pygame
pygame.init()
# Set up the display
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simple Pygame GUI")
# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
# Set up fonts
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 36)
# Render the title
title_text = font.render('Simple GUI', True, black)
title_rect = title_text.get_rect(center=(width // 2, height // 4))
# Define buttons
button1_rect = pygame.Rect(width // 4, height // 2, width // 4, height // 10)
button2_rect = pygame.Rect(width // 2, height // 2, width // 4, height // 10)
button1_text = button_font.render('Button 1', True, white)
button2_text = button_font.render('Button 2', True, white)
button1_text_rect = button1_text.get_rect(center=button1_rect.center)
button2_text_rect = button2_text.get_rect(center=button2_rect.center)
# Main loop
running = True
while running:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()
       elif event.type == pygame.MOUSEBUTTONDOWN:
           if button1_rect.collidepoint(event.pos):
               print("Button 1 clicked!")
           elif button2_rect.collidepoint(event.pos):
               print("Button 2 clicked!")
   # Fill the screen with white
   screen.fill(white)
   # Draw the title
   screen.blit(title_text, title_rect)
   # Draw the buttons
   pygame.draw.rect(screen, blue, button1_rect)
   pygame.draw.rect(screen, blue, button2_rect)
   screen.blit(button1_text, button1_text_rect)
   screen.blit(button2_text, button2_text_rect)
   # Update the display
   pygame.display.flip()