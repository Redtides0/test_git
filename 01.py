# -*- encoding:utf-8 -*- 
import pygame
import sys
import random
from pygame.sprite import Sprite
from pygame.sprite import Group
from time import sleep
import pygame.font


class Gamestats:

    def __init__(self):
        self.game_active = True
        self.i = -1
    def reset_stats(self):
        self.score_list = ["1/9 Fighting!", "2/9 Good!", "3/9 Nice!", "4/9 Good job!", "5/9 Brilliant!",
                           "6/9 Excellent!", "7/9 Fantastic!",
                           "8/9 Perfect!", " 9/9 Unbelievable!", ""]
        self.score = self.score_list[self.i]

class Settings:
    def __init__(self):
        # 你好，我是一个来测试上传到github上会不会乱码的注释，hhh
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        self.fps = 60
        # 你好，我是一个来测试 git diff的注释   
        self.alien_width = 20
        self.alien_height = 20
        self.alien_color = (0, 0, 0)
        self.alien_speed = 6
        self.alien_hp = 5        # alien???????????
        # ????????????
        self.enemy_speed = 3

        self.enemy_count = 60

class Scoreboard:
    """????÷????"""

    def __init__(self, ai_set, screen, stats):
        """??????÷??�???????"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_set = ai_set
        self.stats = stats

        # ????÷?????????????????
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # ???????÷????
    def prep_score(self):
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_set.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_board(self):
        """???????????÷?"""
        self.screen.blit(self.score_image, self.score_rect)

class Alien:
    def __init__(self, screen, ai_set):
        self.screen = screen
        picture = pygame.image.load("image/alien.jpg")
        self.image = pygame.transform.scale(picture, (50, 40))
        self.rect = self.image.get_rect()

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    # ?????????????alien?????
    def update(self, ai_set):

        if self.moving_right and self.rect.x < ai_set.screen_width:  # ???alien????????????
            self.rect.x += ai_set.alien_speed
        elif self.moving_left  and self.rect.x > 0:
            self.rect.x -= ai_set.alien_speed
        if self.moving_up and self.rect.top > 0:
            self.rect.y -= ai_set.alien_speed
        elif self.moving_down and self.rect.bottom < ai_set.screen_height:
            self.rect.y += ai_set.alien_speed

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def resurrection(self):
        self.rect.x = 400
        self.rect.y = 200


# ??????????

class Enemy(Sprite):  # ???Sprite
    def __init__(self, screen, ai_set):
        super().__init__()
        self.x = random.randint(20, ai_set.screen_width - 20)
        self.y = random.randint(20, ai_set.screen_height - 20)
        self.score = random.choice([10, 15, 20, 25])
        self.rect = pygame.Rect(self.x, self.y, self.score, self.score)
        self.direct = random.choice(["up", "down", "left", "right"])  # ???????????????н??????

    def update(self, ai_set):
        if self.direct == "right":
            self.rect.x += ai_set.enemy_speed
        elif self.direct == "left":
            self.rect.x -= ai_set.enemy_speed
        elif self.direct == "up":
            self.rect.y -= ai_set.enemy_speed
        elif self.direct == "down":
            self.rect.y += ai_set.enemy_speed


    def draw(self, screen, ai_set):
        pygame.draw.rect(screen, (self.score * 10, self.score * 5, self.score * 5), self.rect)


def run_game():
    pygame.init()
    ai_set = Settings()
    screen = pygame.display.set_mode((ai_set.screen_width, ai_set.screen_height))
    alien = Alien(screen, ai_set)
    stats = Gamestats()
    stats.reset_stats()
    board = Scoreboard(ai_set, screen, stats)
    board.prep_score()
    pygame.display.set_caption("different alien")
    score_count = 0

    hp = ai_set.alien_hp
    points = Group()
    clock = pygame.time.Clock()

    while hp:

        clock.tick(ai_set.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # ????????????????
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    alien.moving_right = True
                if event.key == pygame.K_a:
                    alien.moving_left = True
                if event.key == pygame.K_w:
                    alien.moving_up = True
                if event.key == pygame.K_s:
                    alien.moving_down = True

            # ???????????????
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    alien.moving_right = False
                if event.key == pygame.K_a:
                    alien.moving_left = False
                if event.key == pygame.K_w:
                    alien.moving_up = False
                if event.key == pygame.K_s:
                    alien.moving_down = False
        # ??????????
        if stats.game_active:

            # ????????????????????????????????
            if len(points) == 0:
                enemy_count = ai_set.enemy_count

                for i in range(enemy_count):
                    new_enemy = Enemy(screen, ai_set)
                    disx = new_enemy.rect.centerx - alien.rect.centerx
                    disy = new_enemy.rect.centery - alien.rect.centery
                    distance = (disx ** 2 + disy ** 2) ** 0.5
                    if distance >= 150:
                        points.add(new_enemy)
                stats.i += 1

            screen.fill(ai_set.bg_color)

            # ????alien????
            alien.update(ai_set)
            # alien??enemy?????????
            if pygame.sprite.spritecollideany(alien, points):
                hp -= 1
                if hp == 0:
                    sleep(2)
                sleep(1)
                points.empty()
                stats.i -= 1
                alien.resurrection()

            # ???alien
            alien.blitme()
            stats.reset_stats()
            board.prep_score()
            board.show_board()
            for point in points.sprites():
                point.update(ai_set)
                point.draw(screen, ai_set)
            pygame.display.flip()

            # ?????????????
            if stats.i == 9:
                sys.exit()

            for point in points.copy():
                if point.rect.y < 0 or point.rect.y > ai_set.screen_height or point.rect.x < 0 or point.rect.x > ai_set.screen_width:
                    points.remove(point)


run_game()

