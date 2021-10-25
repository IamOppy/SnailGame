import pygame
import os
from random import randint
class Game:
    pygame.init()

    WIDTH = 800
    HEIGHT = 400
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    NAME_OF_DISPLAY = pygame.display.set_caption('Snail Game')
    CLOCK = pygame.time.Clock() #SET FRAMERATE
    FONT_ = pygame.font.Font(os.path.join('BuildingBlocks/FONT', 'Pixeltype.ttf'), 50)

    INTRO_TEXT = FONT_.render('PIXEL RUNNER', False, (64, 64 ,64))
    INTRO_TEXT_RECT = INTRO_TEXT.get_rect(center = (400, 50))

    #GAME OVER TEXT
    GAME_START_TEXT = FONT_.render("PRESS SPACE TO START", False, (64, 64 ,64))
    GAME_START_RECT = GAME_START_TEXT.get_rect(center = (400, 350))\

    SKY_SURFACE = pygame.image.load('BuildingBlocks/Sky.png').convert_alpha()
    GROUND_SURFACE = pygame.image.load(os.path.join('BuildingBlocks', 'ground.png')).convert_alpha()


    SNAIL_SURFACE = pygame.image.load(os.path.join("BuildingBlocks/snail", 'snail1.png')).convert_alpha()
    SNAIL_RECT = SNAIL_SURFACE.get_rect(bottomright=(600, 300))

    PLAYER_SURFACE1 = pygame.image.load(os.path.join('BuildingBlocks/Players', 'player_walk_1.png')).convert_alpha()
    PLAYER_RECT1 = PLAYER_SURFACE1.get_rect(midbottom=(80, 300))

    PLAYER_STAND_SURF = pygame.image.load(os.path.join('BuildingBlocks/Players', 'player_stand.png')).convert_alpha()
    PLAYER_STAND_SURF = pygame.transform.scale(PLAYER_STAND_SURF, (200, 200))
    PLAYER_STAND_RECT = PLAYER_STAND_SURF.get_rect(center = (400, 200))

    #TIMER
    OBSTACLE_TIMER = pygame.USEREVENT + 1
    pygame.time.set_timer(OBSTACLE_TIMER, 900)

    PLAYER_GRAVITY = 0
    START_TIME = 0
    SCORE = 0
    snail_x_pos = 600  # HORIZONTAL LINE
    snail_y_pos = 250  # VERTICAL LINE
    OBSTACLE_RECT_LIST = []
    def __init__(self):
        self.GAME_STATE = False



    def display_score(self):
        current_time = int(pygame.time.get_ticks() / 1000)  - self.START_TIME
        score_surface = self.FONT_.render(f'{current_time}', False, (64, 64, 64))
        score_rect = score_surface.get_rect(center=(400, 50))
        self.SCREEN.blit(score_surface, score_rect)
        return current_time

    def OBSTACLE_MOVEMENT(self, OBSTACLE_RECT_LIST):
        print(OBSTACLE_RECT_LIST)
        if self.OBSTACLE_RECT_LIST:
            for obs_rect in self.OBSTACLE_RECT_LIST:
                obs_rect.x -= 5
                self.SCREEN.blit(self.SNAIL_SURFACE, obs_rect)
            self.OBSTACLE_RECT_LIST = [obs for obs in self.OBSTACLE_RECT_LIST if obs.x > 0]
            return self.OBSTACLE_RECT_LIST
        else:
            return []


    def main_loop(self):

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if self.GAME_STATE:
                    if event.type == pygame.MOUSEMOTION:  # FIRST OPTION TO GET MOUSE POS
                        if self.PLAYER_RECT1.collidepoint(event.pos):
                            pass
                    if event.type == pygame.MOUSEBUTTONDOWN:  # CHECK IF MOUSE BUTTON BEING CLICKED
                        # if PLAYER_RECT1.collidepoint(event.pos):
                        self.PLAYER_GRAVITY -= 20

                    else:
                        if event.type == pygame.KEYDOWN:  # FIRST OPTION: CHECK KEY INPUT INSIDE EVENT LOOP (IDEAL METHOD)
                            if event.key == pygame.K_j and self.PLAYER_RECT1.bottom >= 300:
                                self.PLAYER_GRAVITY = -20
                    
                if event.type == self.OBSTACLE_TIMER and self.GAME_STATE:
                     self.OBSTACLE_RECT_LIST.append(self.SNAIL_SURFACE.get_rect(bottomright= (randint(900, 1100), 300)))

                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.GAME_STATE = True
                        self.SNAIL_RECT.left = 800
                        self.START_TIME = int(pygame.time.get_ticks() / 1000)

            if self.GAME_STATE:
                # ATTACHING SURFACES TO SCREEN/DISPLAY

                self.SCREEN.blit(self.SKY_SURFACE, (0, 0))
                self.SCREEN.blit(self.GROUND_SURFACE, (0, 300))  # FLOOR
                # SCREEN.blit(TEXT_SURFACE, TEXT_SURFACE_RECT)
                # pygame.draw.rect(SCREEN, 'Black', SCORE_SURFACE_RECT)
                # pygame.draw.rect(SCREEN, 'Black', SCORE_SURFACE_RECT,20)
                # pygame.draw.line(SCREEN, 'GOLD', (0,0), pygame.mouse.get_pos(), 10)
                pygame.draw.ellipse(self.SCREEN, 'GOLD', pygame.Rect(50, 200, 100, 100))
                self.SCORE = self.display_score()
                self.SNAIL_RECT.left -= 2
                if self.SNAIL_RECT.left <= 0: self.SNAIL_RECT.left += self.WIDTH  # MOVE ALONG HORIZONTAL LINE

                self.OBSTACLE_RECT_LIST = self.OBSTACLE_MOVEMENT(self.OBSTACLE_RECT_LIST)

                # PLAYER
                self.SCREEN.blit(self.PLAYER_SURFACE1, self.PLAYER_RECT1)
                self.PLAYER_GRAVITY += 1
                self.PLAYER_RECT1.y += self.PLAYER_GRAVITY
                if self.PLAYER_RECT1.bottom > 300: self.PLAYER_RECT1.bottom = 300  # CHECK IF PLAYER GOES DOWN HEIGHT OF SCREEN WHEN FALLING.
                if self.PLAYER_RECT1.top < 0: self.PLAYER_RECT1.bottom += 20  # CHECK IF PLAYER GOES OVER HEIGHT OF SCREEN WHEN JUMPING

                self.SCREEN.blit(self.SNAIL_SURFACE, self.SNAIL_RECT)



                # COLLISION
                if self.SNAIL_RECT.colliderect(self.PLAYER_RECT1):
                    self.GAME_STATE = False
            else:
                self.SCREEN.fill((94, 129, 162))
                self.SCREEN.blit(self.PLAYER_STAND_SURF, self.PLAYER_STAND_RECT)
                SCORE_MESSAGE = self.FONT_.render(f'YOUR SCORE: {self.SCORE}', False, (64, 64 ,64))
                SCORE_MESSAGE_RECT = SCORE_MESSAGE.get_rect(center = (400, 330))
                self.SCREEN.blit(self.INTRO_TEXT, self.INTRO_TEXT_RECT)

                if self.SCORE == 0:
                    self.SCREEN.blit(self.GAME_START_TEXT, self.GAME_START_RECT)
                else:
                    self.SCREEN.blit(SCORE_MESSAGE, SCORE_MESSAGE_RECT)

            pygame.display.update()

            self.CLOCK.tick(60)

if __name__ == '__main__':
    ins = Game()
    ins.main_loop()

