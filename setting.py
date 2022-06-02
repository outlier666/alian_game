# 作者：大大大帅逼
# 码龄：一年
# 开发时间：2022/4/2110:16
# 开发人员：Admin
# 文件名称：setting
# 开发工具：PyCharm


class Settings:
    def __init__(self):
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (20, 20, 20)
        self.font_color = (100, 100, 100)
        # 飞船设置
        # 飞船数
        self.ship_limit = 3

        # 外星人设置
        self.alien_speed = 1.0
        self.fleet_drop_speed = 20
        self.fleet_direction = 1

        # 子弹设置
        self.bullet_speed = 0.5
        self.bullets_allowed = 3
        self.bullet_width = 8
        self.bullet_height = 5
        self.bullet_color = (60, 60, 60)

        # 加快游戏节奏的速度
        self.speedup_scale = 1.1
        # 外星人分数的提高速度
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # 初始化随游戏进行而变化的设置
        self.ship_speed = 0.5
        self.bullet_speed = 1.5
        self.alien_speed = 0.1
        # fleet_direction为1表示向右，为-1表示向左。
        self.fleet_direction = -1

        # fleet_direction_y为1表示向下，为-1表示向上
        self.fleet_direction_y = 1

        # 每一个外星人有多少分
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)