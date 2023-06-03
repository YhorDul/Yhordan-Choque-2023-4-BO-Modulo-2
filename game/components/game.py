
import pygame

from game.utils.constants import BG, FONT_STYLE, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, MENU
from game.components.spaceship import Spaceship
from game.components.enemies.enemy_manager import EnemyManager
from game.components.bullets.bullet_manager import BulletManager
from game.components.enemies.enemy import Enemy
from game.components.menu import Menu
from game.components.power_ups.power_up_manager import PowerUpManager
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 10
        self.x_pos_bg = 0
        self.y_pos_bg = 0
        self.death_count = 0
        self.score = 0
        self.player = Spaceship()
        self.enemy_manager = EnemyManager()
        self.bullet_manager = BulletManager()
        self.enemy = Enemy()
        self.menu = Menu('Press Any Key To Start...', self.screen)
        self.highest_score = 0
        self.power_up_manager = PowerUpManager()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.score = 0
        self.enemy_manager.reset()
        self.bullet_manager.reset()
        self.power_up_manager.reset()
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
        '''pygame.display.quit()
        pygame.quit()'''

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input, self)
        self.enemy_manager.update(self)
        self.bullet_manager.update(self)
        self.power_up_manager.update(self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.enemy_manager.draw(self.screen)
        self.bullet_manager.draw(self.screen)
        self.draw_score()
        self.power_up_manager.draw(self.screen)
        self.draw_power_up_time()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        image_height = image.get_height()
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
        if self.y_pos_bg >= SCREEN_HEIGHT:
            self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
            self.y_pos_bg = 0
        self.y_pos_bg += self.game_speed

    def show_menu(self):
        half_screen_width = SCREEN_WIDTH // 2
        half_screen_height = SCREEN_HEIGHT // 2
        self.menu.reset_screen_color(self.screen)
        
        if self.death_count > 0:
            self.menu.update_message('Game over. Press any key to restart...')
            self.draw_death()
            self.score_obtained()
            self.highest_scores()

        icon = pygame.transform.scale(MENU, (600, 367))
        self.screen.blit(icon, (half_screen_width - 300, half_screen_height - 300))

        shi = pygame.transform.scale(ICON, (80, 150))
        self.screen.blit(shi, (half_screen_width - 50, half_screen_height + 150))

        self.menu.draw(self.screen)
        self.menu.update(self)

    def update_score(self):
        self.score += 1
        if self.score > self.highest_score:
            self.highest_score = self.score

    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (1000, 50)
        self.screen.blit(text, text_rect)

    def update_deaths(self):
        self.death_count += 1

    def draw_death(self):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(f'Deaths: {self.death_count}', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (550, 350)
        self.screen.blit(text, text_rect)
    
    def score_obtained(self):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (550, 400)
        self.screen.blit(text, text_rect)

    def highest_scores(self):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(f'Highest score: {self.highest_score}', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (550, 450)
        self.screen.blit(text, text_rect)

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_time_up - pygame.time.get_ticks()) / 1000, 2)

            if time_to_show >= 0:
                self.menu.draw_power(self.screen, f'{self.player.power_up_type.capitalize()} is enable for {time_to_show} seconds', 540, 50,(255, 255, 255))
            else:
                self.player.has_power_up = False
                self.player.power_up_type = DEFAULT_TYPE
                self.player.set_image()

        



