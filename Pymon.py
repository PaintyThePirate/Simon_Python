import pygame
import random

from pygame.constants import MOUSEBUTTONDOWN

pygame.init()
pygame.mixer.init()
#Create screen. Currently using set resolution; may change.
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
#Define Title and Icons
pygame.display.set_caption("Pymon! It's like Simon, but not")
icon = pygame.image.load('img/icon.jpg')
pygame.display.set_icon(icon)
#Define Buttons
b_green = pygame.image.load('img/green_off.png').convert()
b_green_on = pygame.image.load('img/green_on.png').convert()
b_green_rect = b_green.get_rect(center = (((width/2) -100), (height/2)))
b_red = pygame.image.load('img/red_off.png').convert()
b_red_on = pygame.image.load('img/red_on.png').convert()
b_red_rect = b_red.get_rect(center = (((width/2) +100), (height/2)))
b_yellow = pygame.image.load('img/yellow_off.png').convert()
b_yellow_on = pygame.image.load('img/yellow_on.png').convert()
b_yellow_rect = b_yellow.get_rect(center = (((width/2) -100), ((height/2) + 200)))
b_blue = pygame.image.load('img/blue_off.png').convert()
b_blue_on = pygame.image.load('img/blue_on.png').convert()
b_blue_rect = b_blue.get_rect(center = (((width/2) +100), ((height/2) + 200)))
b_start = pygame.image.load('img/start_off.png').convert()
b_start_rect = b_start.get_rect(midbottom = ((width/2), height))
pixel_font = pygame.font.Font('font/Pixeltype.ttf', 300)
menu_surface = pixel_font.render('PYMON', False, 'White')
menu_rect = menu_surface.get_rect(center = ((width/2), (height/2)))
#Define Sounds
s_green = pygame.mixer.Sound ('sfx/green.wav')
s_red = pygame.mixer.Sound ('sfx/red.wav')
s_yellow = pygame.mixer.Sound ('sfx/yellow.wav')
s_blue = pygame.mixer.Sound ('sfx/blue.wav')
s_incorrect = pygame.mixer.Sound ('sfx/x.wav')
#Create clock object and Timer
clock = pygame.time.Clock()

class pymon():
    game_array = []
    score = 0
    high_score = 0
    game_active = False
    has_played = False
    waiting_for_input = False
    current_check = 0

    def draw_score():
        if pymon.game_active == True:
            pixel_font = pygame.font.Font('font/Pixeltype.ttf', 150)
            score_surface = pixel_font.render(f'Score: {pymon.score}', False, 'White')
            score_rect = menu_surface.get_rect(center = (((width/2) + (width/10)), (0+(height/4))))
            screen.blit(score_surface,score_rect)
        elif pymon.has_played == True:
            pixel_font = pygame.font.Font('font/Pixeltype.ttf', 150)
            score_surface = pixel_font.render(f'High Score: {pymon.high_score}', False, 'Yellow')
            score_rect = menu_surface.get_rect(center = ((width/2), (height/4)))
            screen.blit(score_surface,score_rect)

    def generate_sequence():
        pymon.count = 0
        pymon.game_array.append(random.randint(0, 3))

    def draw_buttons():
        #Draw buttons in initial state.
        screen.blit(b_green,b_green_rect)
        screen.blit(b_red,b_red_rect)
        screen.blit(b_yellow,b_yellow_rect)
        screen.blit(b_blue,b_blue_rect)
        pygame.display.update()
            
    def animate_button(button):
        if button == 0:
            button_sound = s_green
            button_flash = b_green_on
            rect = b_green_rect
        elif button == 1:
            button_sound = s_red
            button_flash = b_red_on
            rect = b_red_rect
        elif button == 2:
            button_sound = s_yellow
            button_flash = b_yellow_on
            rect = b_yellow_rect
        else:
            button_sound = s_blue
            button_flash = b_blue_on
            rect = b_blue_rect
    
        button_sound.play()
        for i in range(0, 70):
            screen.blit(button_flash, rect)
            pygame.display.update()
            clock.tick(60)

        pymon.draw_buttons()

    def check_answer(button):
        if button == pymon.game_array[pymon.current_check]:
            pymon.animate_button(button)
            pymon.current_check += 1
            if pymon.current_check == len(pymon.game_array):
                pymon.score += 1
                pymon.current_check = 0
                pymon.waiting_for_input = False
        else:
            s_incorrect.play()
            pymon.has_played = True
            reset_game()

    #Returns values to their original position; Records new high score if there is one.
        def reset_game():
            pymon.game_array = []
            if pymon.high_score < pymon.score:
                pymon.high_score = pymon.score
            pymon.score = 0
            pymon.game_active = False
            pymon.waiting_for_input = False
            pymon.current_check = 0


#Main Game Loop
while True:
    for event in pygame.event.get():
        #Player exits the game.
        if event.type == pygame.QUIT:
            pygame.quit()
            print("Thank you for playing.")
            exit()
        if event.type == MOUSEBUTTONDOWN:
            if pymon.game_active == False:
                if b_start_rect.collidepoint(pygame.mouse.get_pos()) == True:
                    pymon.game_active = True
            else:
                if b_green_rect.collidepoint(pygame.mouse.get_pos()) == True:
                    pymon.check_answer(0)
                elif b_red_rect.collidepoint(pygame.mouse.get_pos()) == True:
                    pymon.check_answer(1)
                elif b_yellow_rect.collidepoint(pygame.mouse.get_pos()) == True:
                    pymon.check_answer(2)
                elif b_blue_rect.collidepoint(pygame.mouse.get_pos()) == True:
                    pymon.check_answer(3)
    #If game not active display menu.
    if pymon.game_active == False:
        screen.fill((0,0,0))
        screen.blit(menu_surface,menu_rect)
        screen.blit(b_start, b_start_rect)
        pymon.draw_score()
    #If Game is Active Do the main game loop.
    else:
        screen.fill((0, 0, 0))
        #Draw Score
        pymon.draw_score()
        #Draw Buttons
        pymon.draw_buttons()
        #Generate sequence and perform demo.
        if pymon.waiting_for_input == False:
            pygame.display.update()
            pygame.time.wait(700)
            pymon.generate_sequence()
            for button in range(0, len(pymon.game_array)):
                pymon.animate_button(pymon.game_array[button])
            pymon.waiting_for_input = True

    pygame.display.update()
    #Impliment FPS limiter. 
    #clock.tick(60)