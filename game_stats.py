# 作者：大大大帅逼
# 码龄：一年
# 开发时间：2022/4/2316:57
# 开发人员：Admin
# 文件名称：GameStats
# 开发工具：PyCharm


class GameStats:
    # 跟踪游戏的统计信息
    def __init__(self, ai_game):
        # 初始化统计信息
        # 让游戏一开始处于非活动状态
        self.game_active = False
        self.settings = ai_game.settings
        self.reset_stats()

        self.high_score = 0
        self.read_high_score()
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def save_high_score(self):
        """将最高分保存在high_score文件中"""
        high_score_str = str(self.high_score)
        filename = 'high_score.txt'
        with open(filename, 'w') as file_object:
            file_object.write(high_score_str)

    def read_high_score(self):
        """
        读取high_score文件中保存的最高得分
        如果没有记录，则最高分为0
        """
        filename = 'high_score.txt'
        try:
            with open(filename) as file_object:
                contents = file_object.read()
                if contents == '':
                    contents = 0
            self.high_score = int(contents)
        except FileNotFoundError:
            self.high_score = 0
