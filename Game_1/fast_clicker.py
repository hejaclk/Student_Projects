"""
Fast Clicker game (Pygame).
Click the card that shows "CLICK". Score 5 points within 11 seconds to win.
Source: ENG M6L5 – The Fast Clicker game, Part 3.
"""

# =============================================================================
# IMPORTS AND WINDOW SETUP
# =============================================================================
# pygame: graphics, window, events. time: measure elapsed seconds for the game.
import pygame
import time
pygame.init()

# Create the program window: 500x500 pixels, light cyan background.
back = (200, 255, 255)  # background color (R, G, B)
mw = pygame.display.set_mode((500, 500))  # main window
mw.fill(back)
clock = pygame.time.Clock()  # controls frame rate (e.g. 40 FPS later)


# =============================================================================
# AREA CLASS – RECTANGLES ON SCREEN
# =============================================================================
# Base class for any rectangular region: position, size, color. Used for
# drawing and for hit-testing (e.g. "did the user click inside this rectangle?").
class Area():
  def __init__(self, x=0, y=0, width=10, height=10, color=None):
      self.rect = pygame.Rect(x, y, width, height)  # rectangle for position/size
      self.fill_color = color

  def color(self, new_color):
      self.fill_color = new_color

  def fill(self):
      """Draw a filled rectangle on the main window."""
      pygame.draw.rect(mw, self.fill_color, self.rect)

  def outline(self, frame_color, thickness):
      """Draw only the outline (border) of the rectangle."""
      pygame.draw.rect(mw, frame_color, self.rect, thickness)

  def collidepoint(self, x, y):
      """Return True if the point (x, y) is inside this rectangle (for click detection)."""
      return self.rect.collidepoint(x, y)


# =============================================================================
# LABEL CLASS – RECTANGLE WITH TEXT
# =============================================================================
# Extends Area: same rectangle + text rendered with a font. Used for "Time:",
# "Count:", the timer, the score, the cards' "CLICK" text, and win/lose messages.
class Label(Area):
  def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
      """Prepare the text image (Verdana font). Call before draw()."""
      self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)

  def draw(self, shift_x=0, shift_y=0):
      """Draw the filled rectangle, then the text on top (with optional offset)."""
      self.fill()
      mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


# =============================================================================
# COLORS AND GAME CONSTANTS
# =============================================================================
RED = (255, 0, 0)
GREEN = (0, 255, 51)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 100)
BLUE = (80, 80, 255)
LIGHT_GREEN = (200, 255, 200)   # used for "You won!!!" screen
LIGHT_RED = (250, 128, 114)    # used for "Time's up!!!" screen

cards = []       # list of the four clickable card Labels
num_cards = 4
x = 70           # starting x position for the first card; then +100 per card

# Time tracking: start_time = game start; cur_time = last time we updated the timer display.
start_time = time.time()
cur_time = start_time


# =============================================================================
# GAME INTERFACE – TIME AND SCORE LABELS
# =============================================================================
# Static labels ("Time:", "Count:") and the values that change (timer, score).
# They are drawn every frame (or updated when score/time changes).

time_text = Label(0, 0, 50, 50, back)
time_text.set_text('Time:', 40, DARK_BLUE)
time_text.draw(20, 20)

timer = Label(50, 55, 50, 40, back)  # shows elapsed seconds (0, 1, 2, ...)
timer.set_text('0', 40, DARK_BLUE)
timer.draw(0, 0)

score_text = Label(380, 0, 50, 50, back)
score_text.set_text('Count:', 45, DARK_BLUE)
score_text.draw(20, 20)

score = Label(430, 55, 50, 40, back)  # shows current points
score.set_text('0', 40, DARK_BLUE)
score.draw(0, 0)


# =============================================================================
# CREATE THE FOUR CLICKABLE CARDS
# =============================================================================
# Each card is a Label: yellow rectangle, blue outline, "CLICK" text. Only one
# card will show "CLICK" at a time; the player must click that card to score.
for i in range(num_cards):
  new_card = Label(x, 170, 70, 100, YELLOW)
  new_card.outline(BLUE, 10)
  new_card.set_text('CLICK', 26)
  cards.append(new_card)
  x = x + 100

wait = 0    # countdown: when 0, we pick a new random card to show "CLICK"
points = 0  # current score (correct click +1, wrong click -1)
from random import randint


# =============================================================================
# MAIN GAME LOOP
# =============================================================================
# Each iteration: draw cards, handle mouse clicks, check win/lose, update timer, refresh screen.
while True:

  # --- Drawing cards and which one shows "CLICK" ---
  # Every 20 ticks we choose a new random card (1..4) to display "CLICK"; others show only color.
  if wait == 0:
      wait = 20  # keep current "CLICK" card for 20 ticks
      click = randint(1, num_cards)  # which card (1-based) shows "CLICK"
      for i in range(num_cards):
          cards[i].color(YELLOW)
          if (i + 1) == click:
              cards[i].draw(10, 40)  # draw card with "CLICK" text
          else:
              cards[i].fill()        # draw card without text
  else:
      wait -= 1

  # --- Handling mouse clicks on cards ---
  # Left click: find which card was clicked. If it's the one with "CLICK", +1 point (green);
  # otherwise -1 point (red). Then update the score display.
  for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
          x, y = event.pos
          for i in range(num_cards):
              if cards[i].collidepoint(x, y):
                  if i + 1 == click:   # clicked the card that shows "CLICK"
                      cards[i].color(GREEN)
                      points += 1
                  else:               # clicked a wrong card
                      cards[i].color(RED)
                      points -= 1
                  cards[i].fill()
                  score.set_text(str(points), 40, DARK_BLUE)
                  score.draw(0, 0)

  # --- Winning and losing conditions ---
  new_time = time.time()

  # Lose: 11 seconds have passed since start.
  if new_time - start_time >= 11:
       win = Label(0, 0, 500, 500, LIGHT_RED)
       win.set_text("Time's up!!!", 60, DARK_BLUE)
       win.draw(110, 180)
       break

  # Update the on-screen timer every full second (so the player sees 0, 1, 2, ...).
  if int(new_time) - int(cur_time) == 1:
       timer.set_text(str(int(new_time - start_time)), 40, DARK_BLUE)
       timer.draw(0, 0)
       cur_time = new_time

  # Win: reached 5 or more points. Show "You won!!!" and completion time.
  if points >= 5:
       win = Label(0, 0, 500, 500, LIGHT_GREEN)
       win.set_text("You won!!!", 60, DARK_BLUE)
       win.draw(140, 180)
       resul_time = Label(90, 230, 250, 250, LIGHT_GREEN)
       resul_time.set_text("Completion time: " + str(int(new_time - start_time)) + " sec", 40, DARK_BLUE)
       resul_time.draw(0, 0)
       break

  pygame.display.update()
  clock.tick(40)  # cap at 40 frames per second

# Final refresh so the win/lose screen stays visible after the loop exits.
pygame.display.update()
