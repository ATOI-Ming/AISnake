import heapq
import random
import time
from typing import List, Tuple, Optional, Set
from snake_game import SnakeGame, Direction
from config import game_config

class AIController:
    def __init__(self, game: SnakeGame):
        """
        AI控制器初始化

        Args:
            game: 贪吃蛇游戏实例
        """
        self.game = game
        self.algorithm = game_config.get("ai.algorithm", "astar")
        self.difficulty = game_config.get("ai.difficulty", "normal")
        self.think_time = game_config.get("ai.think_time", 0.0)
        self.last_think_time = 0
    
    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """计算曼哈顿距离"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def a_star_pathfinding(self, start: Tuple[int, int], goal: Tuple[int, int], 
                          obstacles: Set[Tuple[int, int]]) -> Optional[List[Tuple[int, int]]]:
        """
        A*寻路算法
        
        Args:
            start: 起始位置
            goal: 目标位置
            obstacles: 障碍物位置集合
            
        Returns:
            路径列表，如果无法到达则返回None
        """
        if start == goal:
            return [start]
        
        # 优先队列：(f_score, g_score, position, path)
        open_set = [(0, 0, start, [start])]
        closed_set = set()
        
        while open_set:
            _, g_score, current, path = heapq.heappop(open_set)
            
            if current in closed_set:
                continue
                
            closed_set.add(current)
            
            if current == goal:
                return path
            
            # 检查四个方向
            for direction in Direction:
                dx, dy = direction.value
                next_pos = (current[0] + dx, current[1] + dy)
                
                # 检查边界
                if (next_pos[0] < 0 or next_pos[0] >= self.game.grid_width or
                    next_pos[1] < 0 or next_pos[1] >= self.game.grid_height):
                    continue
                
                # 检查障碍物
                if next_pos in obstacles or next_pos in closed_set:
                    continue
                
                new_g_score = g_score + 1
                h_score = self.manhattan_distance(next_pos, goal)
                new_f_score = new_g_score + h_score
                
                new_path = path + [next_pos]
                heapq.heappush(open_set, (new_f_score, new_g_score, next_pos, new_path))
        
        return None
    
    def is_safe_move(self, direction: Direction) -> bool:
        """
        检查移动是否安全
        
        Args:
            direction: 移动方向
            
        Returns:
            bool: 是否安全
        """
        next_pos = self.game.get_next_position(direction)
        return self.game.is_valid_position(next_pos)
    
    def get_safe_directions(self) -> List[Direction]:
        """获取所有安全的移动方向"""
        safe_directions = []
        for direction in Direction:
            if self.is_safe_move(direction):
                # 防止反向移动
                if len(self.game.snake) > 1:
                    opposite_direction = {
                        Direction.UP: Direction.DOWN,
                        Direction.DOWN: Direction.UP,
                        Direction.LEFT: Direction.RIGHT,
                        Direction.RIGHT: Direction.LEFT
                    }
                    if direction != opposite_direction.get(self.game.direction):
                        safe_directions.append(direction)
                else:
                    safe_directions.append(direction)
        return safe_directions
    
    def simulate_move(self, direction: Direction) -> int:
        """
        模拟移动并返回可达空间大小
        
        Args:
            direction: 移动方向
            
        Returns:
            可达空间大小
        """
        next_pos = self.game.get_next_position(direction)
        if not self.game.is_valid_position(next_pos):
            return 0
        
        # 创建临时蛇身（模拟移动后的状态）
        temp_snake = [next_pos] + self.game.snake[:-1]
        if next_pos == self.game.food:
            temp_snake = [next_pos] + self.game.snake  # 吃到食物，不移除尾部
        
        # 使用BFS计算可达空间
        visited = set(temp_snake)
        queue = [next_pos]
        reachable_count = 0
        
        while queue:
            current = queue.pop(0)
            for direction_check in Direction:
                dx, dy = direction_check.value
                neighbor = (current[0] + dx, current[1] + dy)
                
                if (0 <= neighbor[0] < self.game.grid_width and
                    0 <= neighbor[1] < self.game.grid_height and
                    neighbor not in visited):
                    visited.add(neighbor)
                    queue.append(neighbor)
                    reachable_count += 1
        
        return reachable_count
    
    def greedy_strategy(self) -> Direction:
        """贪心策略：总是朝食物方向移动"""
        safe_directions = self.get_safe_directions()
        if not safe_directions:
            return self.game.direction

        food_pos = self.game.food

        # 计算到食物的距离
        best_direction = None
        min_distance = float('inf')

        for direction in safe_directions:
            next_pos = self.game.get_next_position(direction)
            distance = self.manhattan_distance(next_pos, food_pos)
            if distance < min_distance:
                min_distance = distance
                best_direction = direction

        return best_direction or safe_directions[0]

    def random_strategy(self) -> Direction:
        """随机策略：随机选择安全方向"""
        safe_directions = self.get_safe_directions()
        return random.choice(safe_directions) if safe_directions else self.game.direction

    def defensive_strategy(self) -> Direction:
        """防御策略：优先考虑安全性"""
        safe_directions = self.get_safe_directions()
        if not safe_directions:
            return self.game.direction

        # 选择可达空间最大的方向
        best_direction = None
        max_space = -1

        for direction in safe_directions:
            space = self.simulate_move(direction)
            if space > max_space:
                max_space = space
                best_direction = direction

        return best_direction or safe_directions[0]

    def get_best_direction(self) -> Direction:
        """
        获取最佳移动方向

        Returns:
            最佳移动方向
        """
        if self.game.game_over:
            return self.game.direction

        # AI思考延迟
        current_time = time.time()
        if current_time - self.last_think_time < self.think_time:
            return self.game.direction
        self.last_think_time = current_time

        # 根据配置选择AI策略
        if self.algorithm == "greedy":
            return self.greedy_strategy()
        elif self.algorithm == "random":
            return self.random_strategy()
        elif self.algorithm == "defensive":
            return self.defensive_strategy()
        else:  # default: astar
            return self.astar_strategy()

    def astar_strategy(self) -> Direction:
        """A*策略：使用A*算法寻路"""
        head_pos = self.game.get_head_position()
        food_pos = self.game.food

        # 获取安全方向
        safe_directions = self.get_safe_directions()

        if not safe_directions:
            return self.game.direction

        # 创建障碍物集合（蛇身，但不包括尾部，因为移动时尾部会移动）
        obstacles = set(self.game.snake[:-1])

        # 尝试使用A*算法找到食物
        path = self.a_star_pathfinding(head_pos, food_pos, obstacles)

        if path and len(path) > 1:
            # 找到路径，获取下一步方向
            next_pos = path[1]
            for direction in Direction:
                if self.game.get_next_position(direction) == next_pos:
                    if direction in safe_directions:
                        # 额外检查：确保这个移动不会让蛇困住自己
                        reachable_space = self.simulate_move(direction)
                        if reachable_space >= len(self.game.snake):
                            return direction

        # 如果A*失败或路径不安全，使用防御策略
        return self.defensive_strategy()
    
    def get_direction_towards_food(self) -> Optional[Direction]:
        """
        获取朝向食物的方向（简单策略）
        
        Returns:
            朝向食物的方向，如果无法确定则返回None
        """
        head_x, head_y = self.game.get_head_position()
        food_x, food_y = self.game.food
        
        # 优先选择距离食物更近的方向
        directions_priority = []
        
        if food_x > head_x:
            directions_priority.append(Direction.RIGHT)
        elif food_x < head_x:
            directions_priority.append(Direction.LEFT)
            
        if food_y > head_y:
            directions_priority.append(Direction.DOWN)
        elif food_y < head_y:
            directions_priority.append(Direction.UP)
        
        # 检查这些方向是否安全
        safe_directions = self.get_safe_directions()
        
        for direction in directions_priority:
            if direction in safe_directions:
                return direction
        
        return None
