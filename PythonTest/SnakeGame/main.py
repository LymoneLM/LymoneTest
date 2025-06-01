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

    def update(self, current_time, mode):
        # 根据时间更新蛇的位置
        if current_time - self.last_move_time > self.move_delay:
            self.last_move_time = current_time
            head_x, head_y = self.positions[0]
            dx, dy = self.direction

            if mode == GameMode.ENDLESS:
                new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)
            else:
                new_head = (head_x + dx, head_y + dy)

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
        self.game_state = "id_input"
        self.name_warning = ""
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
        self.player_name = "无名高手"
        self.timed_mode_duration = 180  # 限时模式时长(秒)

        # 分数榜
        self.scoreboard = Scoreboard()

        # 音频
        self.sound_enabled = True
        self.bg_music_enabled = True
        self.sound_volume = 0.5
        self.music_volume = 0.3

        # 加载设置
        self.load_settings()

        # 添加键盘状态跟踪
        self.key_pressed = {}


    @staticmethod
    def load_font(size):
        try:
            font = pygame.font.Font("./MiSans-Normal.ttf", size)
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
                if self.game_state == "id_input":
                    self.handle_id_input_keys(event)
                elif self.game_state == "menu":
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

    def handle_id_input_keys(self, event):
        if event.key == pygame.K_RETURN:
            # 验证ID长度
            name_len = sum(2 if ord(c) > 127 else 1 for c in self.player_name)
            if name_len == 0:
                self.name_warning = "ID不能为空!"
            elif name_len > 14:
                self.name_warning = "ID过长! 最多14字符(汉字算2字符)"
            else:
                self.game_state = "menu"
                self.name_warning = ""
        elif event.key == pygame.K_BACKSPACE:
            self.player_name = self.player_name[:-1]
            self.name_warning = ""

        elif event.unicode and event.unicode.isprintable():
            new_char = event.unicode
            char_len = 2 if ord(new_char) > 127 else 1
            current_len = sum(2 if ord(c) > 127 else 1 for c in self.player_name)

            if current_len + char_len <= 14:
                self.player_name += new_char
                self.name_warning = ""
            else:
                self.name_warning = "ID过长! 最多14字符(汉字算2字符)"

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
            self.snake.update(current_time, self.mode)

            # 更新游戏时间
            self.elapsed_time = (current_time - self.start_time) / 1000.0

            # 限时模式倒计时
            if self.mode == GameMode.TIMED:
                self.timed_mode_time = max(0.0, self.timed_mode_duration - self.elapsed_time)
                if self.timed_mode_time <= 0:
                    self.game_state = "game_over"

            # 更新障碍物(障碍模式)
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
            if (self.mode == GameMode.CLASSIC
                    or self.mode == GameMode.OBSTACLE
                    or self.mode == GameMode.TIMED):
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
                self.save_score()

    def save_score(self):
        self.scoreboard.scores = [
            s for s in self.scoreboard.scores
            if not (s.player_name == self.player_name and s.mode == self.mode.value)
        ]

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

        elif self.game_state == "id_input":
            self.draw_id_input()

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

    def draw_id_input(self):
        self.screen.fill(BACKGROUND)

        title_text = self.title_font.render("请输入玩家ID", True, GREEN)
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 150))

        # 绘制输入框
        input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 250, 300, 50)
        pygame.draw.rect(self.screen, LIGHT_GRAY, input_rect)
        pygame.draw.rect(self.screen, WHITE, input_rect, 2)

        # 绘制输入文本
        text_surface = self.font.render(self.player_name, True, BLACK)
        self.screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))

        # 绘制光标
        if pygame.time.get_ticks() % 1000 < 500:
            cursor_x = input_rect.x + 10 + text_surface.get_width()
            pygame.draw.line(self.screen, BLACK, (cursor_x, input_rect.y + 10),
                             (cursor_x, input_rect.y + 40), 2)

        # 绘制提示
        hint_text = self.font.render("按Enter确认 (ID最多14字符, 汉字算2字符)", True, WHITE)
        self.screen.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2, 320))

        # 绘制警告（如果有）
        if self.name_warning:
            warn_text = self.font.render(self.name_warning, True, RED)
            self.screen.blit(warn_text, (SCREEN_WIDTH // 2 - warn_text.get_width() // 2, 380))

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
        self.screen.blit(mode_text, (50, 80))

        modes = [
            ("0. 全部", None),
            ("1. 经典", GameMode.CLASSIC.value),
            ("2. 无尽", GameMode.ENDLESS.value),
            ("3. 限时", GameMode.TIMED.value),
            ("4. 障碍", GameMode.OBSTACLE.value)
        ]

        button_width = 120
        button_height = 40
        button_margin = 10
        start_x = 50
        start_y = 110

        for i, (name, mode_val) in enumerate(modes):
            x = start_x + i * (button_width + button_margin)

            # 高亮显示当前选择的模式
            is_selected = (self.selected_scoreboard_mode == mode_val or
                           (self.selected_scoreboard_mode is None and mode_val is None))

            button_color = (100, 200, 100) if is_selected else (70, 70, 80)
            pygame.draw.rect(self.screen, button_color, (x, start_y, button_width, button_height))
            pygame.draw.rect(self.screen, LIGHT_GRAY, (x, start_y, button_width, button_height), 2)

            mode_btn = self.font.render(name, True, WHITE)
            self.screen.blit(mode_btn, (x + button_width // 2 - mode_btn.get_width() // 2,
                                        start_y + button_height // 2 - mode_btn.get_height() // 2))

        # 获取当前选择的分数榜
        if self.selected_scoreboard_mode is None:
            scores = self.scoreboard.get_top_scores()
        else:
            scores = self.scoreboard.get_top_scores(self.selected_scoreboard_mode)

        headers = ["排名", "玩家", "分数", "时间", "模式", "日期"]
        y_pos = 160  # 下移以避免重叠

        pygame.draw.rect(self.screen, (50, 50, 60), (40, y_pos - 5, SCREEN_WIDTH - 80, 35))

        col_positions = [50, 150, 270, 390, 490, 610]

        for i, header in enumerate(headers):
            header_text = self.font.render(header, True, BLUE)
            self.screen.blit(header_text, (col_positions[i], y_pos))

        scores = scores[:10]

        # 绘制表格行
        for i, score in enumerate(scores):
            row_color = (60, 60, 70) if i % 2 == 0 else (50, 50, 60)
            pygame.draw.rect(self.screen, row_color, (40, y_pos + 35 + i * 35, SCREEN_WIDTH - 80, 35))

            rank_text = self.small_font.render(f"{i + 1}", True, YELLOW if i == 0 else WHITE)
            self.screen.blit(rank_text, (col_positions[0] + 20, y_pos + 40 + i * 35))

            name = score.player_name
            if len(name) > 10:
                name = name[:7] + "..."
            name_text = self.small_font.render(name, True, WHITE)
            self.screen.blit(name_text, (col_positions[1], y_pos + 40 + i * 35))

            score_text = self.small_font.render(f"{score.score}", True, GREEN)
            self.screen.blit(score_text, (col_positions[2] + 20, y_pos + 40 + i * 35))

            mins = int(score.duration) // 60
            secs = int(score.duration) % 60
            time_str = f"{mins}:{secs:02d}"
            time_text = self.small_font.render(time_str, True, WHITE)
            self.screen.blit(time_text, (col_positions[3] + 10, y_pos + 40 + i * 35))

            # 模式（简化显示）
            mode_str = score.mode
            if "经典" in mode_str:
                mode_str = "经典"
            elif "无尽" in mode_str:
                mode_str = "无尽"
            elif "限时" in mode_str:
                mode_str = "限时"
            elif "障碍" in mode_str:
                mode_str = "障碍"
            mode_text = self.small_font.render(mode_str, True, LIGHT_GRAY)
            self.screen.blit(mode_text, (col_positions[4] + 10, y_pos + 40 + i * 35))

            # 日期（只显示月/日）
            date_text = self.small_font.render(score.date.strftime("%m/%d"), True, WHITE)
            self.screen.blit(date_text, (col_positions[5] + 10, y_pos + 40 + i * 35))

        # 如果没有记录
        if not scores:
            no_scores = self.font.render("暂无记录", True, LIGHT_GRAY)
            self.screen.blit(no_scores, (SCREEN_WIDTH // 2 - no_scores.get_width() // 2, y_pos + 100))

        # 添加提示文本
        hint_text = self.font.render("按0-4选择模式，按ESC返回主菜单", True, LIGHT_GRAY)
        self.screen.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2, SCREEN_HEIGHT - 40))

    def run(self):
        while True:
            self.settings_changed = False
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

# 启动游戏
if __name__ == "__main__":
    game = PixelSnakeGame()
    game.run()