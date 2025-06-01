import os
import sys
import json
import pygame
import random
import locale
from enum import Enum
from datetime import datetime

# 设置系统编码为UTF-8
locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')

# 初始化pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 60

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 180, 0)
DARK_RED = (180, 0, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
BLUE = (0, 120, 255)
PURPLE = (180, 0, 255)
BACKGROUND = (30, 30, 35)
GRID_COLOR = (50, 50, 55)
UI_BG = (40, 40, 45, 200)


# 游戏模式枚举
class GameMode(Enum):
    CLASSIC = "经典模式"
    ENDLESS = "无尽模式"
    TIMED = "限时挑战"
    OBSTACLE = "障碍模式"


# 难度级别
class Difficulty(Enum):
    EASY = (8, "简单")
    MEDIUM = (12, "中等")
    HARD = (16, "困难")


# 方向向量
DIRECTIONS = {
    pygame.K_w: (0, -1),
    pygame.K_s: (0, 1),
    pygame.K_a: (-1, 0),
    pygame.K_d: (1, 0),
    pygame.K_q: (-1, -1),
    pygame.K_e: (1, -1),
    pygame.K_z: (-1, 1),
    pygame.K_c: (1, 1)
}


# 蛇类
class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # 初始向右移动
        self.score = 0
        self.consecutive_eats = 0
        self.last_move_time = pygame.time.get_ticks()
        self.move_delay = 150  # 移动延迟(毫秒)
        self.alive = True
        self.grow_pending = 2  # 初始长度为3

    def update(self, current_time):
        # 根据时间更新蛇的位置
        if current_time - self.last_move_time > self.move_delay:
            self.last_move_time = current_time
            head_x, head_y = self.positions[0]
            dx, dy = self.direction
            new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)

            # 检查是否撞到自己
            if new_head in self.positions[1:]:
                self.alive = False

            # 添加新头部
            self.positions.insert(0, new_head)

            # 如果不需要增长，移除尾部
            if self.grow_pending > 0:
                self.grow_pending -= 1
            else:
                self.positions.pop()

    def change_direction(self, new_direction):
        # 防止180度转向
        dx, dy = self.direction
        new_dx, new_dy = new_direction

        # 允许八方向移动
        if (dx, dy) != (-new_dx, -new_dy):
            self.direction = new_direction

    def grow(self):
        self.grow_pending += 1
        self.length += 1

    def draw(self, surface):
        # 绘制蛇头
        head_x, head_y = self.positions[0]
        pygame.draw.rect(surface, RED, pygame.Rect(head_x * GRID_SIZE, head_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, DARK_RED, pygame.Rect(head_x * GRID_SIZE, head_y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                         1)

        # 绘制蛇身
        for i, (x, y) in enumerate(self.positions[1:]):
            color_intensity = max(50, 255 - (i * 5))
            body_color = (0, color_intensity, 0)
            pygame.draw.rect(surface, body_color, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, DARK_GREEN, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)


# 食物类
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.is_special = False
        self.spawn_time = 0
        self.spawn()

    def spawn(self, snake_positions=None, obstacles=None):
        if snake_positions is None:
            snake_positions = []
        if obstacles is None:
            obstacles = []

        # 确保食物不会出现在蛇身或障碍物上
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if self.position not in snake_positions and self.position not in obstacles:
                break

        # 随机决定是否为特殊食物(10%概率)
        self.is_special = random.random() < 0.1
        self.color = YELLOW if self.is_special else RED
        self.spawn_time = pygame.time.get_ticks()

    def draw(self, surface):
        x, y = self.position
        pygame.draw.rect(surface, self.color, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # 为特殊食物添加闪光效果
        if self.is_special:
            flash = (pygame.time.get_ticks() // 200) % 2
            if flash:
                pygame.draw.rect(surface, WHITE, pygame.Rect((x + 0.25) * GRID_SIZE, (y + 0.25) * GRID_SIZE,
                                                             GRID_SIZE // 2, GRID_SIZE // 2))


# 障碍物类
class Obstacle:
    def __init__(self):
        self.positions = []
        self.spawn_timer = 0
        self.spawn_delay = 5000  # 每5秒生成一个障碍物

    def update(self, current_time, snake_positions, food_position):
        # 定时生成新障碍物
        if current_time - self.spawn_timer > self.spawn_delay:
            self.spawn_timer = current_time
            self.spawn(snake_positions, food_position)

    def spawn(self, snake_positions, food_position):
        # 在空闲位置生成障碍物
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if (pos not in snake_positions and
                    pos != food_position and
                    pos not in self.positions):
                self.positions.append(pos)
                break

    def draw(self, surface):
        for x, y in self.positions:
            pygame.draw.rect(surface, GRAY, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, LIGHT_GRAY, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)


# 分数记录
class ScoreEntry:
    def __init__(self, player_name, score, duration, mode, date=None):
        self.player_name = player_name
        self.score = score
        self.duration = duration
        self.mode = mode
        self.date = date or datetime.now()

    def to_dict(self):
        return {
            "player_name": self.player_name,
            "score": self.score,
            "duration": self.duration,
            "mode": self.mode,
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S")
        }

    @classmethod
    def from_dict(cls, data):
        date = datetime.strptime(data["date"], "%Y-%m-%d %H:%M:%S")
        return cls(data["player_name"], data["score"], data["duration"], data["mode"], date)


# 分数榜管理
class Scoreboard:
    def __init__(self, filename="scores.json"):
        self.filename = filename
        self.scores = []
        self.load_scores()

    def load_scores(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding='utf-8') as f:
                    data = json.load(f)
                    self.scores = [ScoreEntry.from_dict(entry) for entry in data]
            except:
                self.scores = []
        else:
            self.scores = []

    def save_scores(self):
        data = [score.to_dict() for score in self.scores]
        with open(self.filename, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_score(self, score_entry):
        self.scores.append(score_entry)
        # 排序：分数降序，时间升序
        self.scores.sort(key=lambda x: (-x.score, x.duration))
        # 只保留每个模式的前10名
        self.save_scores()

    def get_top_scores(self, mode=None, count=10):
        if mode:
            filtered = [score for score in self.scores if score.mode == mode]
        else:
            filtered = self.scores
        return filtered[:count]


# 游戏主类
class PixelSnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("像素贪吃蛇")
        self.clock = pygame.time.Clock()

        # 使用支持中文的字体
        self.font = self.load_font(28)
        self.title_font = self.load_font(48)
        self.small_font = self.load_font(24)

        # 游戏状态
        self.game_state = "menu"  # menu, playing, paused, game_over
        self.mode = GameMode.CLASSIC
        self.difficulty = Difficulty.MEDIUM
        self.show_grid = True
        self.selected_scoreboard_mode = None
        self.settings_changed = False

        # 游戏对象
        self.snake = Snake()
        self.food = Food()
        self.obstacles = Obstacle()

        # 游戏数据
        self.start_time = 0
        self.elapsed_time = 0
        self.last_score = 0
        self.player_name = "玩家-Lymone"
        self.timed_mode_duration = 180  # 限时模式时长(秒)

        # 分数榜
        self.scoreboard = Scoreboard()

        # 音频
        self.sound_enabled = True
        self.bg_music_enabled = True
        self.sound_volume = 0.5
        self.music_volume = 0.3

        # 创建一些虚拟分数用于测试
        if not self.scoreboard.scores:
            self._create_dummy_scores()

        # 加载设置
        self.load_settings()

        # 添加键盘状态跟踪
        self.key_pressed = {}


    @staticmethod
    def load_font(size):
        try:
            font = pygame.font.Font("./assets/MiSans-Normal.ttf", size)
            return font
        except:
            return pygame.font.SysFont("Microsoft YaHei", size)

    def _create_dummy_scores(self):
        """
        生成测试榜单数据，仅用于测试
        """
        modes = [GameMode.CLASSIC, GameMode.ENDLESS, GameMode.TIMED, GameMode.OBSTACLE]
        for i in range(15):
            mode = random.choice(modes)
            self.scoreboard.add_score(ScoreEntry(
                f"玩家{i + 1}",
                random.randint(100, 1000),
                random.uniform(60, 600),
                mode.value
            ))

    def reset_game(self):
        self.snake.reset()
        self.snake.move_delay = 150 - (self.difficulty.value[0] * 5)
        self.food.spawn(self.snake.positions, self.obstacles.positions)
        self.obstacles.positions = []
        self.start_time = pygame.time.get_ticks()
        self.elapsed_time = 0
        self.snake.consecutive_eats = 0
        self.last_score = self.snake.score
        self.game_state = "playing"

        # 限时模式设置
        if self.mode == GameMode.TIMED:
            self.timed_mode_time = self.timed_mode_duration

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.game_state == "menu":
                    self.handle_menu_keys(event.key)
                elif self.game_state == "playing":
                    self.handle_playing_keys(event.key)
                elif self.game_state == "paused":
                    self.handle_paused_keys(event.key)
                elif self.game_state == "game_over":
                    self.handle_game_over_keys(event.key)
                elif self.game_state == "settings":
                    self.handle_settings_keys(event.key)
                elif self.game_state == "high_scores":
                    self.handle_high_scores_keys(event.key)

    def handle_menu_keys(self, key):
        if key in [pygame.K_1, pygame.K_KP1]:
            self.mode = GameMode.CLASSIC
            self.reset_game()
        elif key in [pygame.K_2, pygame.K_KP2]:
            self.mode = GameMode.ENDLESS
            self.reset_game()
        elif key in [pygame.K_3, pygame.K_KP3]:
            self.mode = GameMode.TIMED
            self.reset_game()
        elif key in [pygame.K_4, pygame.K_KP4]:
            self.mode = GameMode.OBSTACLE
            self.reset_game()
        elif key == pygame.K_s:
            self.game_state = "settings"
        elif key == pygame.K_h:
            self.game_state = "high_scores"

    def handle_playing_keys(self, key):
        if key in DIRECTIONS:
            self.snake.change_direction(DIRECTIONS[key])
        elif key == pygame.K_SPACE:
            self.game_state = "paused"
        elif key == pygame.K_ESCAPE:
            self.game_state = "menu"

    def handle_paused_keys(self, key):
        if key == pygame.K_SPACE:
            self.game_state = "playing"
        elif key == pygame.K_ESCAPE:
            self.game_state = "menu"

    def handle_game_over_keys(self, key):
        if key == pygame.K_RETURN:
            self.reset_game()
        elif key == pygame.K_ESCAPE:
            self.game_state = "menu"

    def handle_settings_keys(self, key):
        if key in [pygame.K_1, pygame.K_KP1]:
            self.difficulty = Difficulty.EASY
            self.settings_changed = True
            self.save_settings()
        elif key in [pygame.K_2, pygame.K_KP2]:
            self.difficulty = Difficulty.MEDIUM
            self.settings_changed = True
            self.save_settings()
        elif key in [pygame.K_3, pygame.K_KP3]:
            self.difficulty = Difficulty.HARD
            self.settings_changed = True
            self.save_settings()
        elif key == pygame.K_g:
            self.show_grid = not self.show_grid
            self.settings_changed = True
            self.save_settings()
        elif key == pygame.K_ESCAPE:
            self.game_state = "menu"

    def handle_high_scores_keys(self, key):
        if key in [pygame.K_0, pygame.K_KP0]:
            self.selected_scoreboard_mode = None
        elif key in [pygame.K_1, pygame.K_KP1]:
            self.selected_scoreboard_mode = GameMode.CLASSIC.value
        elif key in [pygame.K_2, pygame.K_KP2]:
            self.selected_scoreboard_mode = GameMode.ENDLESS.value
        elif key in [pygame.K_3, pygame.K_KP3]:
            self.selected_scoreboard_mode = GameMode.TIMED.value
        elif key in [pygame.K_4, pygame.K_KP4]:
            self.selected_scoreboard_mode = GameMode.OBSTACLE.value
        elif key == pygame.K_ESCAPE:
            self.game_state = "menu"

    def update(self):
        current_time = pygame.time.get_ticks()

        if self.game_state == "playing":
            # 更新蛇的位置
            self.snake.update(current_time)

            # 更新游戏时间
            self.elapsed_time = (current_time - self.start_time) / 1000.0

            # 限时模式倒计时
            if self.mode == GameMode.TIMED:
                self.timed_mode_time = max(0.0, self.timed_mode_duration - self.elapsed_time)
                if self.timed_mode_time <= 0:
                    self.game_state = "game_over"

            # 更新障碍物(仅在障碍模式)
            if self.mode == GameMode.OBSTACLE:
                self.obstacles.update(current_time, self.snake.positions, self.food.position)

            # 检查是否吃到食物
            if self.snake.positions[0] == self.food.position:
                # 计算得分
                if self.food.is_special:
                    self.snake.score += 50
                else:
                    self.snake.score += 10
                    self.snake.consecutive_eats += 1

                # 连吃奖励
                if self.snake.consecutive_eats >= 5:
                    self.snake.score += 100
                    self.snake.consecutive_eats = 0

                # 蛇增长
                self.snake.grow()

                # 生成新食物
                self.food.spawn(self.snake.positions, self.obstacles.positions)

            # 检查碰撞(经典模式)
            if self.mode == GameMode.CLASSIC:
                head_x, head_y = self.snake.positions[0]
                # 撞墙检测
                if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
                    self.snake.alive = False

                # 障碍物碰撞
                if self.snake.positions[0] in self.obstacles.positions:
                    self.snake.alive = False

            # 检查游戏结束条件
            if not self.snake.alive:
                self.game_state = "game_over"
                # 保存分数
                self.save_score()

    def save_score(self):
        score_entry = ScoreEntry(
            self.player_name,
            self.snake.score,
            self.elapsed_time,
            self.mode.value
        )
        self.scoreboard.add_score(score_entry)

    def save_settings(self):
        settings = {
            "difficulty": self.difficulty.name,
            "show_grid": self.show_grid,
            "sound_volume": self.sound_volume,
            "music_volume": self.music_volume
        }
        with open("settings.json", "w") as f:
            json.dump(settings, f)

    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
                self.difficulty = Difficulty[settings.get("difficulty", "MEDIUM")]
                self.show_grid = settings.get("show_grid", True)
                self.sound_volume = settings.get("sound_volume", 0.5)
                self.music_volume = settings.get("music_volume", 0.3)
        except:
            # 如果文件不存在或读取失败，使用默认设置
            self.difficulty = Difficulty.MEDIUM
            self.show_grid = True
            self.sound_volume = 0.5
            self.music_volume = 0.3

    def draw(self):
        self.screen.fill(BACKGROUND)

        # 绘制网格
        if self.show_grid:
            for x in range(0, SCREEN_WIDTH, GRID_SIZE):
                pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
            for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
                pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

        if self.game_state == "playing" or self.game_state == "paused":
            # 绘制食物
            self.food.draw(self.screen)

            # 绘制障碍物(如果游戏模式允许)
            if self.mode == GameMode.OBSTACLE:
                self.obstacles.draw(self.screen)

            # 绘制蛇
            self.snake.draw(self.screen)

            # 绘制UI
            self.draw_ui()

            # 暂停状态显示
            if self.game_state == "paused":
                self.draw_pause_overlay()

        elif self.game_state == "game_over":
            self.draw_game_over()

        elif self.game_state == "menu":
            self.draw_menu()

        elif self.game_state == "settings":
            self.draw_settings()

        elif self.game_state == "high_scores":
            self.draw_high_scores()

        pygame.display.flip()

    def draw_ui(self):
        # 绘制分数
        score_text = self.font.render(f"分数: {self.snake.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # 绘制时间
        time_text = self.font.render(f"时间: {self.elapsed_time:.1f}s", True, WHITE)
        self.screen.blit(time_text, (10, 40))

        # 绘制模式
        mode_text = self.font.render(f"模式: {self.mode.value}", True, WHITE)
        self.screen.blit(mode_text, (10, 70))

        # 绘制难度
        diff_text = self.font.render(f"难度: {self.difficulty.value[1]}", True, WHITE)
        self.screen.blit(diff_text, (10, 100))

        # 限时模式倒计时
        if self.mode == GameMode.TIMED:
            mins = int(self.timed_mode_time) // 60
            secs = int(self.timed_mode_time) % 60
            time_left = f"{mins:02d}:{secs:02d}"
            timer_text = self.font.render(f"剩余时间: {time_left}", True, YELLOW)
            self.screen.blit(timer_text, (SCREEN_WIDTH - 200, 10))

        # 连吃计数
        if self.snake.consecutive_eats > 0:
            streak_text = self.font.render(f"连吃: {self.snake.consecutive_eats}/5", True, BLUE)
            self.screen.blit(streak_text, (SCREEN_WIDTH - 150, 40))

    def draw_pause_overlay(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        pause_text = self.title_font.render("游戏暂停", True, WHITE)
        self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))

        continue_text = self.font.render("按空格键继续", True, WHITE)
        self.screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

        menu_text = self.font.render("按ESC返回主菜单", True, WHITE)
        self.screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    def draw_game_over(self):
        # 背景
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        # 游戏结束文本
        game_over_text = self.title_font.render("游戏结束!", True, RED)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 100))

        # 分数
        score_text = self.font.render(f"最终分数: {self.snake.score}", True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 180))

        # 时间
        time_text = self.font.render(f"游戏时长: {self.elapsed_time:.1f}秒", True, WHITE)
        self.screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, 220))

        # 模式
        mode_text = self.font.render(f"游戏模式: {self.mode.value}", True, WHITE)
        self.screen.blit(mode_text, (SCREEN_WIDTH // 2 - mode_text.get_width() // 2, 260))

        # 提示
        restart_text = self.font.render("按回车键重新开始", True, GREEN)
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT - 150))

        menu_text = self.font.render("按ESC返回主菜单", True, GREEN)
        self.screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT - 100))

    def draw_menu(self):
        # 标题
        title_y_pos = 30
        title_text = self.title_font.render("像素贪吃蛇", True, GREEN)
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, title_y_pos))

        # 游戏模式选择
        y_pos = 100 + title_y_pos
        mode_text = self.font.render("选择游戏模式:", True, WHITE)
        self.screen.blit(mode_text, (SCREEN_WIDTH // 2 - mode_text.get_width() // 2, y_pos))

        modes = [
            ("1. 经典模式", "撞墙或自碰结束"),
            ("2. 无尽模式", "穿墙设定，只计算自碰死亡"),
            ("3. 限时挑战", "180秒内获得最高分"),
            ("4. 障碍模式", "地图中随机生成障碍物")
        ]

        for i, (title, desc) in enumerate(modes):
            y = y_pos + 50 + i * 60
            title_render = self.font.render(title, True, YELLOW)
            desc_render = self.small_font.render(desc, True, LIGHT_GRAY)

            self.screen.blit(title_render, (SCREEN_WIDTH // 2 - title_render.get_width() // 2, y))
            self.screen.blit(desc_render, (SCREEN_WIDTH // 2 - desc_render.get_width() // 2, y + 30))

        # 其他选项
        settings_text = self.font.render("S - 游戏设置", True, BLUE)
        self.screen.blit(settings_text, (SCREEN_WIDTH // 2 - settings_text.get_width() // 2, SCREEN_HEIGHT - 140))

        scores_text = self.font.render("H - 查看高分榜", True, BLUE)
        self.screen.blit(scores_text, (SCREEN_WIDTH // 2 - scores_text.get_width() // 2, SCREEN_HEIGHT - 100))

        # 当前设置
        setting_info = self.font.render(f"难度: {self.difficulty.value[1]} | 网格: {'开' if self.show_grid else '关'}",
                                        True, LIGHT_GRAY)
        self.screen.blit(setting_info, (SCREEN_WIDTH // 2 - setting_info.get_width() // 2, SCREEN_HEIGHT - 50))

    def draw_settings(self):
        # 背景
        self.screen.fill(BACKGROUND)

        # 标题
        title_text = self.title_font.render("游戏设置", True, BLUE)
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # 难度设置
        diff_text = self.font.render("难度设置(按1-3选择):", True, WHITE)
        self.screen.blit(diff_text, (150, 150))

        difficulties = [
            ("1. 简单", Difficulty.EASY),
            ("2. 中等", Difficulty.MEDIUM),
            ("3. 困难", Difficulty.HARD)
        ]

        for i, (name, diff) in enumerate(difficulties):
            color = GREEN if diff == self.difficulty else LIGHT_GRAY
            diff_btn = self.font.render(name, True, color)
            self.screen.blit(diff_btn, (300 + i * 150, 220))


        # 网格显示
        grid_text = self.font.render("显示网格(按G切换):", True, WHITE)
        self.screen.blit(grid_text, (150, 290))

        grid_status = self.font.render("开" if self.show_grid else "关", True, GREEN if self.show_grid else RED)
        self.screen.blit(grid_status, (400, 290))

        hint_text = self.small_font.render("设置会自动保存，按ESC返回主菜单", True, LIGHT_GRAY)
        self.screen.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2, SCREEN_HEIGHT - 80))

        if self.settings_changed:
            changed_text = self.small_font.render("设置已更新!", True, GREEN)
            self.screen.blit(changed_text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 50))

        # 返回
        back_text = self.font.render("按ESC返回主菜单", True, GREEN)
        self.screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, SCREEN_HEIGHT - 50))

    def draw_high_scores(self):
        # 背景
        self.screen.fill(BACKGROUND)

        # 标题
        title_text = self.title_font.render("高分榜", True, YELLOW)
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 30))

        mode_text = self.font.render("选择模式(按0-4):", True, WHITE)
        self.screen.blit(mode_text, (50, 100))

        modes = [
            ("0. 全部", None),
            ("1. 经典模式", GameMode.CLASSIC.value),
            ("2. 无尽模式", GameMode.ENDLESS.value),
            ("3. 限时挑战", GameMode.TIMED.value),
            ("4. 障碍模式", GameMode.OBSTACLE.value)
        ]

        for i, (name, mode_val) in enumerate(modes):
            # 高亮显示当前选择的模式
            is_selected = (self.selected_scoreboard_mode == mode_val or
                           (self.selected_scoreboard_mode is None and mode_val is None))
            color = YELLOW if is_selected else LIGHT_GRAY
            mode_btn = self.font.render(name, True, color)
            self.screen.blit(mode_btn, (180 + (i % 3) * 250, 100 + (i // 3) * 40))

        # 获取当前选择的分数榜
        if self.selected_scoreboard_mode is None:
            scores = self.scoreboard.get_top_scores()
            mode_display = "全部模式"
        else:
            scores = self.scoreboard.get_top_scores(self.selected_scoreboard_mode)
            mode_display = self.selected_scoreboard_mode

        # 当前模式显示
        current_mode_text = self.font.render(f"当前模式: {mode_display}", True, YELLOW)
        self.screen.blit(current_mode_text, (SCREEN_WIDTH // 2 - current_mode_text.get_width() // 2, 180))

        # 表格标题
        headers = ["排名", "玩家", "分数", "时间", "模式", "日期"]
        y_pos = 150
        for i, header in enumerate(headers):
            header_text = self.font.render(header, True, BLUE)
            self.screen.blit(header_text, (50 + i * 130, y_pos))

        # 分数数据
        scores = self.scoreboard.get_top_scores()
        for i, score in enumerate(scores[:10]):  # 只显示前10名
            y = y_pos + 40 + i * 35
            rank = self.small_font.render(f"{i + 1}", True, WHITE)
            name = self.small_font.render(score.player_name, True, WHITE)
            score_val = self.small_font.render(str(score.score), True, WHITE)
            time_val = self.small_font.render(f"{score.duration:.1f}s", True, WHITE)
            mode_val = self.small_font.render(score.mode, True, WHITE)
            date_val = self.small_font.render(score.date.strftime("%m/%d"), True, WHITE)

            self.screen.blit(rank, (60, y))
            self.screen.blit(name, (180, y))
            self.screen.blit(score_val, (310, y))
            self.screen.blit(time_val, (440, y))
            self.screen.blit(mode_val, (570, y))
            self.screen.blit(date_val, (700, y))

        # 添加提示文本
        hint_text = self.font.render("按0-4选择显示模式，按ESC返回主菜单", True, LIGHT_GRAY)
        self.screen.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2, SCREEN_HEIGHT - 80))

        # 返回
        back_text = self.font.render("按ESC返回主菜单", True, GREEN)
        self.screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, SCREEN_HEIGHT - 50))

    def run(self):
        while True:
            self.settings_changed = False
            self.handle_events()
            if self.game_state == "playing":
                self.update()
            else:
                self.update_game_state()
            self.draw()
            self.clock.tick(FPS)

    def update_game_state(self):
        current_time = pygame.time.get_ticks()
        self.elapsed_time = (current_time - self.start_time) / 1000.0

# 启动游戏
if __name__ == "__main__":
    game = PixelSnakeGame()
    game.run()