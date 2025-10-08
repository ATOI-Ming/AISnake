import pygame
import random
import math
import time
from enum import Enum
from typing import List, Tuple
# 简化导入，使用try-except处理
try:
    from config import game_config, get_text, get_theme_colors
except ImportError:
    # 提供默认值
    class DefaultConfig:
        def get(self, key, default=None):
            return default
    game_config = DefaultConfig()
    get_text = lambda key: key
    get_theme_colors = lambda: {}

try:
    from game_stats import game_stats
except ImportError:
    # 提供默认统计对象
    class DefaultStats:
        def start_game(self): pass
        def end_game(self, *args): pass
        def record_move(self): pass
        def record_food_eaten(self, *args): pass
        def check_achievements(self, *args): return []
        def get_all_time_stats(self): return {'highest_score': 0}
    game_stats = DefaultStats()

try:
    from audio_system import audio_system
except ImportError:
    # 提供默认音效对象
    class DefaultAudio:
        def play_eat_sound(self): pass
        def play_game_over_sound(self): pass
        def play_move_sound(self): pass
    audio_system = DefaultAudio()

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Particle:
    """粒子效果类"""
    def __init__(self, x: float, y: float, color: Tuple[int, int, int],
                 velocity: Tuple[float, float], lifetime: float = 1.0):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.uniform(2, 6)

    def update(self, dt: float):
        """更新粒子状态"""
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        self.lifetime -= dt

        # 重力效果
        self.velocity = (self.velocity[0], self.velocity[1] + 200 * dt)

    def is_alive(self) -> bool:
        """检查粒子是否还存活"""
        return self.lifetime > 0

    def get_alpha(self) -> int:
        """获取透明度"""
        return int(255 * (self.lifetime / self.max_lifetime))

class SnakeGame:
    def __init__(self, width: int = None, height: int = None, cell_size: int = None):
        """
        初始化贪吃蛇游戏

        Args:
            width: 游戏窗口宽度（None时使用配置文件）
            height: 游戏窗口高度（None时使用配置文件）
            cell_size: 每个格子的大小（None时使用配置文件）
        """
        # 从配置文件获取参数
        self.width = width or game_config.get("window.width", 800)
        self.height = height or game_config.get("window.height", 600)
        self.cell_size = cell_size or game_config.get("window.cell_size", 20)
        self.grid_width = self.width // self.cell_size
        self.grid_height = self.height // self.cell_size
        
        # 颜色定义（支持主题）
        self.theme_colors = get_theme_colors()
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.DARK_GREEN = (0, 150, 0)
        self.LIGHT_GREEN = self.theme_colors.get("snake_head", (144, 238, 144))
        self.GOLD = (255, 215, 0)
        self.ORANGE = (255, 165, 0)
        self.PURPLE = (128, 0, 128)
        self.CYAN = (0, 255, 255)
        self.GRAY = (128, 128, 128)
        self.DARK_GRAY = (64, 64, 64)
        self.YELLOW = (255, 255, 0)
        
        # 初始化pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("AI Snake - Enhanced Visual Edition")
        self.clock = pygame.time.Clock()

        # 初始化字体（支持中文）
        self.font = self.init_font(36)
        self.small_font = self.init_font(24)
        self.large_font = self.init_font(48)

        # 初始化游戏状态
        self.score = 0
        self.last_score = 0
        self.game_over = False

        # 视觉效果相关
        self.particles = []
        self.food_pulse = 0.0
        self.snake_glow = 0.0
        self.background_stars = self.generate_stars() if game_config.get("visual.enable_stars", True) else []
        self.trail_positions = []
        self.score_animation = 0.0

        # 统计和音效
        self.move_count = 0

        self.reset_game()
    
    def init_font(self, size: int):
        """初始化支持中文的字体"""
        try:
            # 尝试使用系统中文字体
            font_paths = [
                "C:/Windows/Fonts/simhei.ttf",  # 黑体
                "C:/Windows/Fonts/simsun.ttc",  # 宋体
                "C:/Windows/Fonts/msyh.ttc",    # 微软雅黑
                "/System/Library/Fonts/PingFang.ttc",  # macOS
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
            ]

            for font_path in font_paths:
                try:
                    return pygame.font.Font(font_path, size)
                except:
                    continue

            # 如果都失败，使用默认字体
            return pygame.font.Font(None, size)
        except:
            return pygame.font.Font(None, size)

    def generate_stars(self) -> List[Tuple[int, int, int]]:
        """生成背景星星"""
        stars = []
        star_count = game_config.get("visual.star_count", 50)
        for _ in range(star_count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            brightness = random.randint(100, 255)
            stars.append((x, y, brightness))
        return stars

    def reset_game(self):
        """重置游戏状态"""
        # 记录上一局统计
        if hasattr(self, 'snake') and self.score > 0:
            game_stats.end_game(self.score, len(self.snake))

        # 蛇的初始位置（中心）
        center_x = self.grid_width // 2
        center_y = self.grid_height // 2
        self.snake = [(center_x, center_y)]
        self.direction = Direction.RIGHT

        # 生成食物
        self.food = self.generate_food()

        # 游戏状态
        self.last_score = self.score
        self.score = 0
        self.game_over = False
        self.move_count = 0

        # 重置视觉效果
        self.particles.clear()
        self.trail_positions.clear()
        self.score_animation = 0.0

        # 开始新游戏统计
        game_stats.start_game()
        
    def generate_food(self) -> Tuple[int, int]:
        """生成食物位置"""
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def is_valid_position(self, pos: Tuple[int, int]) -> bool:
        """检查位置是否有效（不撞墙，不撞自己）"""
        x, y = pos
        if x < 0 or x >= self.grid_width or y < 0 or y >= self.grid_height:
            return False
        if pos in self.snake:
            return False
        return True
    
    def get_head_position(self) -> Tuple[int, int]:
        """获取蛇头位置"""
        return self.snake[0]
    
    def get_next_position(self, direction: Direction) -> Tuple[int, int]:
        """根据方向获取下一个位置"""
        head_x, head_y = self.get_head_position()
        dx, dy = direction.value
        return (head_x + dx, head_y + dy)
    
    def move(self, direction: Direction) -> bool:
        """
        移动蛇
        
        Args:
            direction: 移动方向
            
        Returns:
            bool: 游戏是否继续
        """
        if self.game_over:
            return False
            
        # 防止蛇反向移动
        if len(self.snake) > 1:
            opposite_direction = {
                Direction.UP: Direction.DOWN,
                Direction.DOWN: Direction.UP,
                Direction.LEFT: Direction.RIGHT,
                Direction.RIGHT: Direction.LEFT
            }
            if direction == opposite_direction.get(self.direction):
                direction = self.direction
        
        self.direction = direction
        next_pos = self.get_next_position(direction)
        
        # 检查碰撞
        if not self.is_valid_position(next_pos):
            self.game_over = True

            # 音效和视觉效果
            audio_system.play_game_over_sound()
            if game_config.get("visual.enable_particles", True):
                self.create_explosion_particles(self.get_head_position())

            return False
        
        # 移动蛇头
        self.snake.insert(0, next_pos)
        self.move_count += 1

        # 记录移动统计
        game_stats.record_move()

        # 播放移动音效（偶尔）
        audio_system.play_move_sound()

        # 检查是否吃到食物
        if next_pos == self.food:
            self.score += 1
            self.score_animation = 1.0  # 触发分数动画

            # 记录统计
            game_stats.record_food_eaten(len(self.snake))

            # 音效和视觉效果
            audio_system.play_eat_sound()
            if game_config.get("visual.enable_particles", True):
                self.create_food_particles(next_pos)

            self.food = self.generate_food()
        else:
            # 没吃到食物，移除蛇尾
            tail_pos = self.snake.pop()
            # 添加尾部轨迹效果
            if game_config.get("visual.enable_trail", True):
                self.trail_positions.append((tail_pos, time.time()))
        
        return True
    
    def get_possible_moves(self) -> List[Direction]:
        """获取所有可能的移动方向"""
        possible_moves = []
        for direction in Direction:
            next_pos = self.get_next_position(direction)
            if self.is_valid_position(next_pos):
                # 防止反向移动
                if len(self.snake) > 1:
                    opposite_direction = {
                        Direction.UP: Direction.DOWN,
                        Direction.DOWN: Direction.UP,
                        Direction.LEFT: Direction.RIGHT,
                        Direction.RIGHT: Direction.LEFT
                    }
                    if direction != opposite_direction.get(self.direction):
                        possible_moves.append(direction)
                else:
                    possible_moves.append(direction)
        return possible_moves

    def create_food_particles(self, pos: Tuple[int, int]):
        """创建食物被吃掉时的粒子效果"""
        x, y = pos
        screen_x = x * self.cell_size + self.cell_size // 2
        screen_y = y * self.cell_size + self.cell_size // 2

        # 创建多个粒子
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            color = random.choice([self.GOLD, self.ORANGE, self.RED, self.YELLOW])
            particle = Particle(screen_x, screen_y, color, velocity, random.uniform(0.5, 1.5))
            self.particles.append(particle)

    def create_explosion_particles(self, pos: Tuple[int, int]):
        """创建爆炸粒子效果（游戏结束时）"""
        x, y = pos
        screen_x = x * self.cell_size + self.cell_size // 2
        screen_y = y * self.cell_size + self.cell_size // 2

        # 创建爆炸粒子
        for _ in range(25):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(100, 300)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            color = random.choice([self.RED, self.ORANGE, self.YELLOW, self.WHITE])
            particle = Particle(screen_x, screen_y, color, velocity, random.uniform(1.0, 2.0))
            self.particles.append(particle)

    def update_particles(self, dt: float):
        """更新所有粒子"""
        self.particles = [p for p in self.particles if p.is_alive()]
        for particle in self.particles:
            particle.update(dt)

    def update_visual_effects(self, dt: float):
        """更新所有视觉效果"""
        # 更新粒子
        self.update_particles(dt)

        # 更新食物脉冲效果
        self.food_pulse += dt * 3

        # 更新蛇的发光效果
        self.snake_glow += dt * 2

        # 更新分数动画
        if self.score_animation > 0:
            self.score_animation -= dt * 2
            if self.score_animation < 0:
                self.score_animation = 0

        # 清理过期的轨迹
        current_time = time.time()
        self.trail_positions = [(pos, t) for pos, t in self.trail_positions
                               if current_time - t < 0.5]
    
    def draw_background(self):
        """绘制背景"""
        # 渐变背景
        for y in range(self.height):
            color_ratio = y / self.height
            r = int(10 * (1 - color_ratio) + 30 * color_ratio)
            g = int(10 * (1 - color_ratio) + 20 * color_ratio)
            b = int(30 * (1 - color_ratio) + 50 * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.width, y))

        # 绘制星星
        for star_x, star_y, brightness in self.background_stars:
            alpha = int(brightness * (0.5 + 0.5 * math.sin(time.time() * 2 + star_x * 0.01)))
            color = (alpha, alpha, alpha)
            pygame.draw.circle(self.screen, color, (star_x, star_y), 1)

    def draw_grid(self):
        """绘制网格"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, self.DARK_GRAY, (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, self.DARK_GRAY, (0, y), (self.width, y))

    def draw_trail(self):
        """绘制蛇的轨迹效果"""
        current_time = time.time()
        for pos, timestamp in self.trail_positions:
            age = current_time - timestamp
            if age < 0.5:
                alpha = int(100 * (1 - age / 0.5))
                x, y = pos
                rect = pygame.Rect(x * self.cell_size + 2, y * self.cell_size + 2,
                                 self.cell_size - 4, self.cell_size - 4)
                # 创建带透明度的表面
                trail_surface = pygame.Surface((self.cell_size - 4, self.cell_size - 4))
                trail_surface.set_alpha(alpha)
                trail_surface.fill(self.CYAN)
                self.screen.blit(trail_surface, rect)

    def draw_snake(self):
        """绘制蛇"""
        for i, segment in enumerate(self.snake):
            x, y = segment
            rect = pygame.Rect(x * self.cell_size, y * self.cell_size,
                             self.cell_size, self.cell_size)

            if i == 0:  # 蛇头
                # 发光效果
                glow_intensity = int(50 + 30 * math.sin(self.snake_glow))
                glow_color = (0, 255 - glow_intensity, 0)

                # 绘制发光外圈
                glow_rect = pygame.Rect(x * self.cell_size - 2, y * self.cell_size - 2,
                                      self.cell_size + 4, self.cell_size + 4)
                pygame.draw.rect(self.screen, glow_color, glow_rect, 2)

                # 绘制蛇头
                pygame.draw.rect(self.screen, self.LIGHT_GREEN, rect)
                pygame.draw.rect(self.screen, self.WHITE, rect, 2)

                # 绘制眼睛
                eye_size = 3
                eye1_pos = (x * self.cell_size + 5, y * self.cell_size + 5)
                eye2_pos = (x * self.cell_size + self.cell_size - 8, y * self.cell_size + 5)
                pygame.draw.circle(self.screen, self.RED, eye1_pos, eye_size)
                pygame.draw.circle(self.screen, self.RED, eye2_pos, eye_size)
            else:  # 蛇身
                # 渐变色蛇身
                segment_ratio = i / len(self.snake)
                r = int(0 + (100 * segment_ratio))
                g = int(200 - (100 * segment_ratio))
                b = int(50 + (100 * segment_ratio))
                body_color = (r, g, b)

                pygame.draw.rect(self.screen, body_color, rect)
                pygame.draw.rect(self.screen, self.WHITE, rect, 1)

    def draw_food(self):
        """绘制食物"""
        food_x, food_y = self.food
        center_x = food_x * self.cell_size + self.cell_size // 2
        center_y = food_y * self.cell_size + self.cell_size // 2

        # 脉冲效果
        pulse_size = int(self.cell_size // 2 + 5 * math.sin(self.food_pulse))

        # 绘制发光圈
        for radius in range(pulse_size + 10, pulse_size, -2):
            alpha = int(100 * (1 - (radius - pulse_size) / 10))
            glow_surface = pygame.Surface((radius * 2, radius * 2))
            glow_surface.set_alpha(alpha)
            pygame.draw.circle(glow_surface, self.ORANGE, (radius, radius), radius)
            self.screen.blit(glow_surface, (center_x - radius, center_y - radius))

        # 绘制食物本体
        pygame.draw.circle(self.screen, self.RED, (center_x, center_y), pulse_size)
        pygame.draw.circle(self.screen, self.GOLD, (center_x, center_y), pulse_size - 2)
        pygame.draw.circle(self.screen, self.WHITE, (center_x, center_y), pulse_size, 2)

    def draw_particles(self):
        """绘制粒子效果"""
        for particle in self.particles:
            if particle.is_alive():
                alpha = particle.get_alpha()
                particle_surface = pygame.Surface((int(particle.size * 2), int(particle.size * 2)))
                particle_surface.set_alpha(alpha)
                pygame.draw.circle(particle_surface, particle.color,
                                 (int(particle.size), int(particle.size)), int(particle.size))
                self.screen.blit(particle_surface,
                               (int(particle.x - particle.size), int(particle.y - particle.size)))

    def draw_ui(self):
        """绘制用户界面"""
        # 绘制分数
        score_color = self.WHITE
        if self.score_animation > 0:
            # 分数动画效果
            score_color = (255, int(255 * (1 - self.score_animation)), int(255 * (1 - self.score_animation)))

        score_text = self.font.render(f"{get_text('score')}: {self.score}", True, score_color)
        self.screen.blit(score_text, (10, 10))

        # 绘制蛇的长度
        length_text = self.small_font.render(f"{get_text('length')}: {len(self.snake)}", True, self.WHITE)
        self.screen.blit(length_text, (10, 50))

        # 绘制最高分
        if self.last_score > 0:
            best_text = self.small_font.render(f"{get_text('last_score')}: {self.last_score}", True, self.GRAY)
            self.screen.blit(best_text, (10, 75))

        # 绘制统计信息
        stats = game_stats.get_all_time_stats()
        if stats["highest_score"] > 0:
            high_score_text = self.small_font.render(f"{get_text('high_score')}: {stats['highest_score']}", True, self.GOLD)
            self.screen.blit(high_score_text, (10, 100))

        # 绘制AI状态指示器
        ai_text = self.small_font.render(get_text("ai_controlling"), True, self.CYAN)
        ai_rect = ai_text.get_rect()
        ai_rect.topright = (self.width - 10, 10)
        self.screen.blit(ai_text, ai_rect)

        # 绘制游戏结束信息
        if self.game_over:
            # 半透明背景
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(128)
            overlay.fill(self.BLACK)
            self.screen.blit(overlay, (0, 0))

            # 游戏结束文本
            game_over_text = self.large_font.render(get_text("game_over"), True, self.RED)
            game_over_rect = game_over_text.get_rect(center=(self.width//2, self.height//2 - 50))
            self.screen.blit(game_over_text, game_over_rect)

            # 最终分数
            final_score_text = self.font.render(f"{get_text('final_score')}: {self.score}", True, self.WHITE)
            final_score_rect = final_score_text.get_rect(center=(self.width//2, self.height//2))
            self.screen.blit(final_score_text, final_score_rect)

            # 重新开始提示
            restart_text = self.small_font.render(get_text("restart_hint"), True, self.GRAY)
            restart_rect = restart_text.get_rect(center=(self.width//2, self.height//2 + 50))
            self.screen.blit(restart_text, restart_rect)

    def draw(self):
        """主绘制方法"""
        # 更新视觉效果
        dt = self.clock.get_time() / 1000.0
        self.update_visual_effects(dt)

        # 绘制所有元素
        self.draw_background()
        self.draw_grid()
        self.draw_trail()
        self.draw_snake()
        self.draw_food()
        self.draw_particles()
        self.draw_ui()

        pygame.display.flip()
    
    def handle_events(self) -> bool:
        """处理pygame事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()
        return True
    
    def get_game_state(self) -> dict:
        """获取游戏状态信息，供AI使用"""
        return {
            'snake': self.snake.copy(),
            'food': self.food,
            'direction': self.direction,
            'score': self.score,
            'game_over': self.game_over,
            'grid_width': self.grid_width,
            'grid_height': self.grid_height
        }
