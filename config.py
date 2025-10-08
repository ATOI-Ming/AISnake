#!/usr/bin/env python3
"""
游戏配置文件
包含所有可调节的游戏参数和设置
"""

import os
import json
from typing import Dict, Any

class GameConfig:
    """游戏配置管理类"""
    
    def __init__(self, config_file: str = "game_config.json"):
        self.config_file = config_file
        self.default_config = {
            # 游戏窗口设置
            "window": {
                "width": 800,
                "height": 600,
                "title": "AI Snake - Enhanced Visual Edition",
                "cell_size": 20
            },
            
            # 游戏性能设置
            "performance": {
                "fps": 10,
                "auto_restart_delay": 3.0,
                "particle_limit": 100
            },
            
            # 视觉效果设置
            "visual": {
                "enable_particles": True,
                "enable_trail": True,
                "enable_glow": True,
                "enable_stars": True,
                "star_count": 50,
                "enable_grid": True
            },
            
            # AI设置
            "ai": {
                "algorithm": "astar",  # astar, greedy, random
                "difficulty": "normal",  # easy, normal, hard
                "think_time": 0.0  # AI思考延迟（秒）
            },
            
            # 颜色主题
            "colors": {
                "theme": "default",  # default, dark, neon, retro
                "snake_head": [144, 238, 144],
                "snake_body": [0, 200, 50],
                "food": [255, 0, 0],
                "background": [10, 10, 30]
            },
            
            # 音效设置
            "audio": {
                "enable_sound": True,
                "master_volume": 0.7,
                "sfx_volume": 0.8,
                "music_volume": 0.5
            },
            
            # 统计设置
            "stats": {
                "save_stats": True,
                "stats_file": "game_stats.json"
            },
            
            # 语言设置
            "language": {
                "current": "zh_CN",  # zh_CN, en_US
                "auto_detect": True
            }
        }
        
        # 确保配置目录存在
        config_dir = os.path.dirname(self.config_file) if os.path.dirname(self.config_file) else '.'
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        self.config = self.load_config()

        # 确保配置文件存在
        if not os.path.exists(self.config_file):
            self.save_config()
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if not content:  # 文件为空
                        print("配置文件为空，使用默认配置")
                        return self.default_config.copy()
                    loaded_config = json.loads(content)
                # 合并默认配置和加载的配置
                return self.merge_config(self.default_config, loaded_config)
            except (json.JSONDecodeError, Exception) as e:
                print(f"加载配置文件失败: {e}，使用默认配置")
                return self.default_config.copy()
        else:
            # 创建默认配置文件
            print("配置文件不存在，创建默认配置")
            return self.default_config.copy()
    
    def save_config(self):
        """保存配置文件"""
        try:
            # 确保有配置数据
            if not hasattr(self, 'config') or not self.config:
                self.config = self.default_config.copy()

            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            print(f"配置已保存到: {self.config_file}")
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def merge_config(self, default: Dict, loaded: Dict) -> Dict:
        """合并配置，确保所有默认键都存在"""
        result = default.copy()
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self.merge_config(result[key], value)
            else:
                result[key] = value
        return result
    
    def get(self, path: str, default=None):
        """获取配置值，支持点号路径如 'window.width'"""
        keys = path.split('.')
        value = self.config
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, path: str, value):
        """设置配置值"""
        keys = path.split('.')
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value
        self.save_config()
    
    def reset_to_default(self):
        """重置为默认配置"""
        self.config = self.default_config.copy()
        self.save_config()

# 全局配置实例
game_config = GameConfig()

# 语言配置
LANGUAGES = {
    "zh_CN": {
        "score": "分数",
        "length": "长度",
        "last_score": "上次得分",
        "ai_controlling": "AI控制中...",
        "game_over": "游戏结束!",
        "final_score": "最终得分",
        "restart_hint": "按 R 重新开始 | ESC 退出",
        "paused": "暂停中 - 按SPACE继续",
        "high_score": "最高分",
        "games_played": "游戏次数",
        "average_score": "平均分数"
    },
    "en_US": {
        "score": "Score",
        "length": "Length",
        "last_score": "Last Score",
        "ai_controlling": "AI Controlling...",
        "game_over": "Game Over!",
        "final_score": "Final Score",
        "restart_hint": "Press R to Restart | ESC to Exit",
        "paused": "Paused - Press SPACE to Continue",
        "high_score": "High Score",
        "games_played": "Games Played",
        "average_score": "Average Score"
    }
}

def get_text(key: str) -> str:
    """获取当前语言的文本"""
    current_lang = game_config.get("language.current", "zh_CN")
    return LANGUAGES.get(current_lang, LANGUAGES["zh_CN"]).get(key, key)

# 颜色主题
COLOR_THEMES = {
    "default": {
        "snake_head": (144, 238, 144),
        "snake_body": (0, 200, 50),
        "food": (255, 0, 0),
        "background": (10, 10, 30),
        "ui_text": (255, 255, 255)
    },
    "dark": {
        "snake_head": (100, 100, 100),
        "snake_body": (50, 50, 50),
        "food": (200, 0, 0),
        "background": (0, 0, 0),
        "ui_text": (200, 200, 200)
    },
    "neon": {
        "snake_head": (0, 255, 255),
        "snake_body": (255, 0, 255),
        "food": (255, 255, 0),
        "background": (20, 0, 40),
        "ui_text": (0, 255, 255)
    },
    "retro": {
        "snake_head": (0, 255, 0),
        "snake_body": (0, 200, 0),
        "food": (255, 255, 0),
        "background": (0, 50, 0),
        "ui_text": (0, 255, 0)
    }
}

def get_theme_colors(theme_name: str = None) -> Dict[str, tuple]:
    """获取主题颜色"""
    if theme_name is None:
        theme_name = game_config.get("colors.theme", "default")
    return COLOR_THEMES.get(theme_name, COLOR_THEMES["default"])
