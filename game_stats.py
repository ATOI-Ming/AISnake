#!/usr/bin/env python3
"""
游戏统计系统
记录和分析游戏数据
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any
from config import game_config

class GameStats:
    """游戏统计管理类"""
    
    def __init__(self, stats_file: str = None):
        if stats_file is None:
            stats_file = game_config.get("stats.stats_file", "game_stats.json")
        
        self.stats_file = stats_file
        self.current_session = {
            "start_time": time.time(),
            "games_played": 0,
            "total_score": 0,
            "best_score": 0,
            "total_food_eaten": 0,
            "total_moves": 0,
            "game_times": []
        }
        
        self.all_time_stats = self.load_stats()
        
    def load_stats(self) -> Dict[str, Any]:
        """加载历史统计数据"""
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "total_games": 0,
                "total_score": 0,
                "highest_score": 0,
                "total_food_eaten": 0,
                "total_play_time": 0.0,
                "average_score": 0.0,
                "games_by_date": {},
                "score_history": [],
                "achievements": []
            }
    
    def save_stats(self):
        """保存统计数据"""
        if not game_config.get("stats.save_stats", True):
            return
            
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.all_time_stats, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"保存统计数据失败: {e}")
    
    def start_game(self):
        """开始新游戏"""
        self.current_game = {
            "start_time": time.time(),
            "moves": 0,
            "food_eaten": 0,
            "max_length": 1
        }
    
    def end_game(self, final_score: int, snake_length: int):
        """结束游戏并记录统计"""
        if not hasattr(self, 'current_game'):
            return
            
        game_duration = time.time() - self.current_game["start_time"]
        
        # 更新当前会话统计
        self.current_session["games_played"] += 1
        self.current_session["total_score"] += final_score
        self.current_session["best_score"] = max(self.current_session["best_score"], final_score)
        self.current_session["total_food_eaten"] += final_score  # 分数等于吃的食物数
        self.current_session["total_moves"] += self.current_game["moves"]
        self.current_session["game_times"].append(game_duration)
        
        # 更新历史统计
        self.all_time_stats["total_games"] += 1
        self.all_time_stats["total_score"] += final_score
        self.all_time_stats["highest_score"] = max(self.all_time_stats["highest_score"], final_score)
        self.all_time_stats["total_food_eaten"] += final_score
        self.all_time_stats["total_play_time"] += game_duration
        
        # 计算平均分
        if self.all_time_stats["total_games"] > 0:
            self.all_time_stats["average_score"] = self.all_time_stats["total_score"] / self.all_time_stats["total_games"]
        
        # 记录分数历史
        self.all_time_stats["score_history"].append({
            "score": final_score,
            "length": snake_length,
            "duration": game_duration,
            "timestamp": datetime.now().isoformat(),
            "moves": self.current_game["moves"]
        })
        
        # 限制历史记录数量
        if len(self.all_time_stats["score_history"]) > 1000:
            self.all_time_stats["score_history"] = self.all_time_stats["score_history"][-1000:]
        
        # 按日期统计
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in self.all_time_stats["games_by_date"]:
            self.all_time_stats["games_by_date"][today] = {
                "games": 0,
                "total_score": 0,
                "best_score": 0
            }
        
        daily_stats = self.all_time_stats["games_by_date"][today]
        daily_stats["games"] += 1
        daily_stats["total_score"] += final_score
        daily_stats["best_score"] = max(daily_stats["best_score"], final_score)
        
        # 检查成就
        self.check_achievements(final_score, snake_length)
        
        # 保存统计
        self.save_stats()
    
    def record_move(self):
        """记录一次移动"""
        if hasattr(self, 'current_game'):
            self.current_game["moves"] += 1
    
    def record_food_eaten(self, snake_length: int):
        """记录吃到食物"""
        if hasattr(self, 'current_game'):
            self.current_game["food_eaten"] += 1
            self.current_game["max_length"] = max(self.current_game["max_length"], snake_length)
    
    def check_achievements(self, score: int, length: int):
        """检查成就"""
        achievements = []
        
        # 分数成就
        score_milestones = [10, 25, 50, 100, 200, 500]
        for milestone in score_milestones:
            if score >= milestone:
                achievement = f"score_{milestone}"
                if achievement not in self.all_time_stats["achievements"]:
                    achievements.append(f"达成成就: 得分{milestone}分!")
                    self.all_time_stats["achievements"].append(achievement)
        
        # 长度成就
        length_milestones = [10, 20, 50, 100]
        for milestone in length_milestones:
            if length >= milestone:
                achievement = f"length_{milestone}"
                if achievement not in self.all_time_stats["achievements"]:
                    achievements.append(f"达成成就: 蛇长度{milestone}!")
                    self.all_time_stats["achievements"].append(achievement)
        
        # 游戏次数成就
        games_milestones = [10, 50, 100, 500, 1000]
        for milestone in games_milestones:
            if self.all_time_stats["total_games"] >= milestone:
                achievement = f"games_{milestone}"
                if achievement not in self.all_time_stats["achievements"]:
                    achievements.append(f"达成成就: 游戏{milestone}次!")
                    self.all_time_stats["achievements"].append(achievement)
        
        return achievements
    
    def get_session_stats(self) -> Dict[str, Any]:
        """获取当前会话统计"""
        session_time = time.time() - self.current_session["start_time"]
        avg_score = 0
        if self.current_session["games_played"] > 0:
            avg_score = self.current_session["total_score"] / self.current_session["games_played"]
        
        return {
            "session_time": session_time,
            "games_played": self.current_session["games_played"],
            "best_score": self.current_session["best_score"],
            "average_score": avg_score,
            "total_food_eaten": self.current_session["total_food_eaten"]
        }
    
    def get_all_time_stats(self) -> Dict[str, Any]:
        """获取历史统计"""
        return self.all_time_stats.copy()
    
    def get_recent_scores(self, count: int = 10) -> List[Dict]:
        """获取最近的分数记录"""
        return self.all_time_stats["score_history"][-count:]
    
    def get_best_scores(self, count: int = 10) -> List[Dict]:
        """获取最高分记录"""
        sorted_scores = sorted(
            self.all_time_stats["score_history"],
            key=lambda x: x["score"],
            reverse=True
        )
        return sorted_scores[:count]
    
    def reset_stats(self):
        """重置所有统计数据"""
        self.all_time_stats = {
            "total_games": 0,
            "total_score": 0,
            "highest_score": 0,
            "total_food_eaten": 0,
            "total_play_time": 0.0,
            "average_score": 0.0,
            "games_by_date": {},
            "score_history": [],
            "achievements": []
        }
        self.save_stats()
        print("统计数据已重置")

# 全局统计实例
game_stats = GameStats()
