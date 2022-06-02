# 作者：大大大帅逼
# 码龄：一年
# 开发时间：2022/4/219:55
# 开发人员：Admin
# 文件名称：alien_invasion
# 开发工具：PyCharm


import sys
from time import sleep
import pygame
from setting import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard
from star import Star
from random import randint

# 主类
class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.end_game = False
        self.stars = pygame.sprite.Group()
        self._create_starry()

        self._create_fleet()
        self.play_button = Button(self, "Play")
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        # self.bg_color = (230, 230, 230)

    def run_game(self):
        while not self.end_game:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        # 响应按键和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """
        :param mouse_pos:
        :return:
        """
        # 在玩家单机Play按钮时开始新游戏
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # 重置游戏设置
            self.settings.initialize_dynamic_settings()
            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)
            # 重置游戏统计信息
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人并入飞船居中
            self._create_fleet()
            self.ship.center_ship()

    def _check_keydown_events(self, event):
        """
        :param event:
        :return:
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_top = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_bottom = True
        elif event.key == pygame.K_q:
            self._end_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """

        :param event:
        :return:
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_top = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_bottom = False

    def _fire_bullet(self):
        """
        发射子弹，在允许的子弹数量内添加
        :return:
        """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """
        更新子弹的状态
        :return:
        """
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)
        # print(len(self.bullets))
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """
        响应子弹和外星人发生碰撞
        :return:
        """
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        # 与外星人碰撞的子弹都是字典collisions中的一个键，而与每颗子弹相关的值都是一个列表，包含该子弹击中的外星人
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            # 删除现有的子弹并创建一群新的外星人,增加游戏难度
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()

    def _update_screen(self):
        """
        更新屏幕信息
        :return:
        """
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.stars.draw(self.screen)
        # 显示得分
        self.sb.show_score()

        # 如果游戏处于非活动状态，就显示Play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()
        # print(len(self.aliens))

    def _create_fleet(self):
        """
        创建外星人群
        :return:
        """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_y = self.settings.screen_width - (2 * alien_width)
        number_aliens_y = available_space_y // (3 * alien_width)

        # 计算屏幕可容纳多少行外星人。
        ship_height = self.ship.rect.height
        available_space_x = (self.settings.screen_height -
                             alien_height + ship_height)
        number_rows = available_space_x // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_y):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """
        创建单个外星人
        :param alien_number:
        :param row_number:
        :return:
        """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.y = alien.rect.height + 2 * alien.rect.height * row_number
        alien.rect.y = alien.y
        alien.rect.x = self.settings.screen_width - (2 * alien_width * alien_number) - 3 * alien_width

        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """
        判定外星人群与边界接触
        :return:
        """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """
        改变外星人群的移动方向
        :return:
        """
        for alien in self.aliens.sprites():
            alien.rect.x -= self.settings.fleet_drop_speed
        self.settings.fleet_direction_y *= -1

    def _update_aliens(self):
        """
        更新外星人状态
        :return:
        """
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # self._check_aliens_bottom()

    def _ship_hit(self):
        """
        响应飞船被外星人撞到
        :return:
        """
        if self.stats.ships_left > 0:
            # 飞船存活数减一并更新记分牌
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _create_starry(self):
        """
        创建星群
        :return:
        """
        # 创建一个星星并计算一行可容纳多少个星星
        star = Star(self)
        star_width, star_height = star.rect.size
        # 屏幕x方向左右各预留一个星星宽度
        self.availiable_space_x = self.screen.get_rect().width - (2 * star_width)
        # 星星的间距为星星宽度的4倍
        number_stars_x = self.availiable_space_x // (5 * star_width) + 1

        # 计算屏幕可容纳多少行星星
        # 屏幕y方向上下各预留一个星星宽度
        self.availiable_space_y = self.screen.get_rect().height - (2 * star_height)
        # 星星的间距为星星高度的4倍
        number_rows = self.availiable_space_y // (5 * star_height) + 1

        # 创建星群
        for row_number in range(number_rows):
            for star_number in range(number_stars_x):
                self._create_star(star_number, row_number)

    def _create_star(self, star_number, row_number):
        """
        创建一个星星并将其加入到当前行
        :param star_number:
        :param row_number:
        :return:
        """
        star = Star(self)
        star.rect.x = randint(0, self.availiable_space_x)
        star.rect.y = randint(0, self.availiable_space_y)

        self.stars.add(star)

    def _end_game(self):
        """
        保存最高分数记录并关闭游戏
        :return:
        """
        self.stats.save_high_score()
        self.end_game = True


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
