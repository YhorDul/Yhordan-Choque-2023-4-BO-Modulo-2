import pygame
from pygame.sprite import Sprite
from game.utils.constants import SPACESHIP, SCREEN_WIDTH, SCREEN_HEIGHT
from game.components.bullets.bullet import Bullet



class Spaceship(Sprite):

    SHIP_WIDTH = 40
    SHIP_HEIGHT = 60
    X_POS = (SCREEN_WIDTH // 2) - SHIP_WIDTH
    Y_POS = 500
    SHIP_SPEED = 10

    def __init__(self):
        self.image = SPACESHIP
        self.image = pygame.transform.scale(self.image, (self.SHIP_WIDTH, self.SHIP_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.type = 'player'
        self.shooting = 0

    def update(self, user_input, game):
        if user_input[pygame.K_LEFT] or user_input[pygame.K_a]:
            self.move_left()
        elif user_input[pygame.K_RIGHT] or user_input[pygame.K_d]:
            self.move_right()
        elif user_input[pygame.K_UP] or user_input[pygame.K_w]:
            self.move_up()
        elif user_input[pygame.K_DOWN] or user_input[pygame.K_s]:
            self.move_down()
        elif user_input[pygame.K_1]:
            self.shoot(game.bullet_manager)

    def move_left(self):
        if self.rect.left > 0:
            self.rect.x -= self.SHIP_SPEED
        else:
            self.rect.x = SCREEN_WIDTH - self.SHIP_WIDTH  

    def move_right(self):
        if self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.SHIP_SPEED
        else:
            self.rect.x = 0

    def move_up(self):
        if self.rect.y > SCREEN_HEIGHT // 2 :
            self.rect.y -= self.SHIP_SPEED

    def move_down(self):
        if self.rect.y < SCREEN_HEIGHT - self.SHIP_HEIGHT:
            self.rect.y += self.SHIP_SPEED    

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def shoot(self, bullet_manager):
        if self.shooting <= 500:
            self.shooting += 1
            bullet = Bullet(self)
            bullet_manager.add_bullet_ship(bullet)

