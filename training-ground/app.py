import pygame
import sys
import threading
from ai import call_gpt

WIDTH, HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI RPG Game - Choose Topic")
font = pygame.font.SysFont("Arial", 22)
clock = pygame.time.Clock()

input_text = ""
story = ""
ai_response = ""
waiting_for_ai = False
game_started = False
topic_selected = False

def draw_text(surface, text, pos, max_width=760, color=(255,255,255)):
    words = text.split(' ')
    lines = []
    line = ""
    for word in words:
        test_line = line + word + " "
        if font.size(test_line)[0] > max_width:
            lines.append(line)
            line = word + " "
        else:
            line = test_line
    lines.append(line)
    y = pos[1]
    for l in lines:
        rendered = font.render(l, True, color)
        surface.blit(rendered, (pos[0], y))
        y += font.get_height()

def ask_ai(prompt):
    global ai_response
    ai_response = call_gpt(prompt)

def start_game(topic):
    global story, waiting_for_ai, game_started
    intro = f"You are a hero in a {topic} genre. Your adventure begins now.\n"
    story = intro
    waiting_for_ai = True
    game_started = True
    threading.Thread(target=ask_ai, args=(story,)).start()

running = True

while running:
    screen.fill((30,30,30))

    if not topic_selected:
        # Topic selection screen
        draw_text(screen, "Choose the game genre and press Enter (e.g., fantasy, horror, sci-fi, adventure):", (20, 20), color=(255,255,0))
        input_surface = font.render("> " + input_text, True, (255,255,0))
        screen.blit(input_surface, (20, 100))

    else:
        # Game screen
        draw_text(screen, story, (20, 20))
        if ai_response:
            draw_text(screen, "AI: " + ai_response, (20, 300), color=(0, 255, 0))

        input_surface = font.render("You: " + input_text, True, (255,255,0))
        screen.blit(input_surface, (20, 550))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and not waiting_for_ai:
            if event.key == pygame.K_RETURN:
                if not topic_selected:
                    if input_text.strip():
                        topic = input_text.strip()
                        topic_selected = True
                        input_text = ""
                        start_game(topic)
                else:
                    # During the game, send player input to AI
                    story += "\nYou: " + input_text
                    waiting_for_ai = True
                    threading.Thread(target=ask_ai, args=(story,)).start()
                    input_text = ""

            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                if event.unicode.isprintable():
                    input_text += event.unicode

    # When AI response arrives, add it to the story
    if ai_response and waiting_for_ai:
        story += "\nAI: " + ai_response
        ai_response = ""
        waiting_for_ai = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
